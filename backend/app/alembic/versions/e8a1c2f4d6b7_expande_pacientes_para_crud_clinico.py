"""expande pacientes para crud clinico

Revision ID: e8a1c2f4d6b7
Revises: b7c1e4a2d9f0
Create Date: 2026-04-14 19:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "e8a1c2f4d6b7"
down_revision = "b7c1e4a2d9f0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pacientes", sa.Column("genero", sa.String(length=45), nullable=True))
    op.add_column("pacientes", sa.Column("rua", sa.String(length=255), nullable=True))
    op.add_column("pacientes", sa.Column("numero", sa.String(length=45), nullable=True))
    op.add_column("pacientes", sa.Column("complemento", sa.String(length=255), nullable=True))
    op.add_column("pacientes", sa.Column("cidade", sa.String(length=120), nullable=True))
    op.add_column("pacientes", sa.Column("estado", sa.String(length=45), nullable=True))
    op.add_column("pacientes", sa.Column("cep", sa.String(length=20), nullable=True))
    op.add_column("pacientes", sa.Column("dados_clinicos", sa.Text(), nullable=True))
    op.add_column("pacientes", sa.Column("tipo_sanguineo", sa.String(length=10), nullable=True))
    op.add_column("pacientes", sa.Column("ultimo_exame", sa.String(length=255), nullable=True))
    op.add_column("pacientes", sa.Column("alergias", sa.Text(), nullable=True))
    op.add_column("pacientes", sa.Column("medicamentos", sa.Text(), nullable=True))
    op.add_column("pacientes", sa.Column("historico_medico", sa.Text(), nullable=True))
    op.add_column("pacientes", sa.Column("observacoes", sa.Text(), nullable=True))
    op.add_column("pacientes", sa.Column("contato_emergencia_nome", sa.String(length=255), nullable=True))
    op.add_column("pacientes", sa.Column("contato_emergencia_parentesco", sa.String(length=120), nullable=True))
    op.add_column("pacientes", sa.Column("contato_emergencia_telefone", sa.String(length=45), nullable=True))

    op.alter_column("pacientes", "rg", existing_type=sa.String(length=45), nullable=True)
    op.alter_column("pacientes", "data_cadastro", existing_type=sa.String(length=45), nullable=True)
    op.alter_column("pacientes", "endereco", existing_type=sa.String(length=45), nullable=True)
    op.alter_column("pacientes", "plano_saude", existing_type=sa.Boolean(), nullable=True)


def downgrade():
    op.alter_column("pacientes", "plano_saude", existing_type=sa.Boolean(), nullable=False)
    op.alter_column("pacientes", "endereco", existing_type=sa.String(length=45), nullable=False)
    op.alter_column("pacientes", "data_cadastro", existing_type=sa.String(length=45), nullable=False)
    op.alter_column("pacientes", "rg", existing_type=sa.String(length=45), nullable=False)

    op.drop_column("pacientes", "contato_emergencia_telefone")
    op.drop_column("pacientes", "contato_emergencia_parentesco")
    op.drop_column("pacientes", "contato_emergencia_nome")
    op.drop_column("pacientes", "observacoes")
    op.drop_column("pacientes", "historico_medico")
    op.drop_column("pacientes", "medicamentos")
    op.drop_column("pacientes", "alergias")
    op.drop_column("pacientes", "ultimo_exame")
    op.drop_column("pacientes", "tipo_sanguineo")
    op.drop_column("pacientes", "dados_clinicos")
    op.drop_column("pacientes", "cep")
    op.drop_column("pacientes", "estado")
    op.drop_column("pacientes", "cidade")
    op.drop_column("pacientes", "complemento")
    op.drop_column("pacientes", "numero")
    op.drop_column("pacientes", "rua")
    op.drop_column("pacientes", "genero")
