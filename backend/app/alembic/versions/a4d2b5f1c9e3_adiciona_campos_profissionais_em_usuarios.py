"""adiciona_campos_profissionais_em_usuarios

Revision ID: a4d2b5f1c9e3
Revises: 1eb6ce8b3384
Create Date: 2026-04-13 10:40:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a4d2b5f1c9e3"
down_revision = "1eb6ce8b3384"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("usuarios", sa.Column("registro_profissional", sa.String(length=60), nullable=True))
    op.add_column("usuarios", sa.Column("especialidade_principal", sa.String(length=120), nullable=True))
    op.add_column("usuarios", sa.Column("instituicao", sa.String(length=120), nullable=True))
    op.add_column("usuarios", sa.Column("universidade", sa.String(length=120), nullable=True))
    op.add_column("usuarios", sa.Column("ano_formacao", sa.Integer(), nullable=True))
    op.add_column("usuarios", sa.Column("residencia_medica", sa.String(length=120), nullable=True))
    op.add_column("usuarios", sa.Column("especializacoes", sa.JSON(), nullable=True))


def downgrade():
    op.drop_column("usuarios", "especializacoes")
    op.drop_column("usuarios", "residencia_medica")
    op.drop_column("usuarios", "ano_formacao")
    op.drop_column("usuarios", "universidade")
    op.drop_column("usuarios", "instituicao")
    op.drop_column("usuarios", "especialidade_principal")
    op.drop_column("usuarios", "registro_profissional")
