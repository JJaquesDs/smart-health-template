"""alter-tabelas-especialidade-medicos

Revision ID: 7dca82a41257
Revises: fb1f83cf26ab
Create Date: 2026-04-09 00:44:14.878090

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '7dca82a41257'
down_revision = 'fb1f83cf26ab'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Remover FK antiga
    op.drop_constraint('medicos_area_id_fkey', 'medicos', type_='foreignkey')

    # 2. Remover coluna antiga
    op.drop_column('medicos', 'esp_id')

    # 3. Agora sim pode remover a tabela
    op.drop_index(op.f('ix_areas_area_id'), table_name='areas')
    op.drop_table('areas')

    # 4. Criar nova tabela
    op.create_table(
        'especialidades',
        sa.Column('esp_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('titulo', sa.String(length=45), nullable=False),
        sa.Column('status', sa.String(length=45), nullable=False),
        sa.PrimaryKeyConstraint('esp_id'),
        sa.UniqueConstraint('titulo')
    )
    op.create_index(op.f('ix_especialidades_esp_id'), 'especialidades', ['esp_id'], unique=False)

    # 5. Criar nova coluna em medicos
    op.add_column('medicos', sa.Column('esp_id', sa.Integer(), nullable=False))

    # 6. Criar nova FK
    op.create_foreign_key(
        'medicos_esp_id_fkey',
        'medicos',
        'especialidades',
        ['esp_id'],
        ['esp_id']
    )
