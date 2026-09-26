"""Normaliza CPF e registra metadados de pacientes no banco."""
from alembic import op
import sqlalchemy as sa

revision = 'b6d8f0a2c4e6'
down_revision = 'a5c7e9f1b3d5'
branch_labels = None
depends_on = None


def upgrade():
    # Não inventa datas históricas: registros anteriores permanecem com NULL.
    op.add_column('pacientes', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('pacientes', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    for name in ('created_at', 'updated_at'):
        op.alter_column('pacientes', name, server_default=sa.text('CURRENT_TIMESTAMP'))
    op.add_column('pacientes', sa.Column('status', sa.String(8), nullable=False, server_default='active'))
    op.create_check_constraint('ck_pacientes_status', 'pacientes', "status IN ('active', 'inactive')")
    op.execute("UPDATE pacientes SET cpf = regexp_replace(cpf, '[^0-9]', '', 'g') WHERE cpf ~ '^[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}-[0-9]{2}$'")
    op.execute("CREATE UNIQUE INDEX uq_pacientes_cpf_normalizado ON pacientes ((regexp_replace(cpf, '[^0-9]', '', 'g')))")
    op.execute('''CREATE FUNCTION pacientes_update_timestamp() RETURNS trigger AS $$
    BEGIN
        NEW.created_at := OLD.created_at;
        NEW.updated_at := clock_timestamp();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql''')
    op.execute('''CREATE TRIGGER pacientes_update_timestamp BEFORE UPDATE ON pacientes
    FOR EACH ROW EXECUTE FUNCTION pacientes_update_timestamp()''')


def downgrade():
    op.execute('DROP TRIGGER pacientes_update_timestamp ON pacientes')
    op.execute('DROP FUNCTION pacientes_update_timestamp()')
    op.drop_index('uq_pacientes_cpf_normalizado', table_name='pacientes')
    op.drop_constraint('ck_pacientes_status', 'pacientes', type_='check')
    for name in ('status', 'updated_at', 'created_at'):
        op.drop_column('pacientes', name)
