"""cria_catalogos_de_exames_e_medicamentos

Revision ID: b7c1e4a2d9f0
Revises: a4d2b5f1c9e3
Create Date: 2026-04-14 12:25:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b7c1e4a2d9f0"
down_revision = "a4d2b5f1c9e3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "catalogo_exames",
        sa.Column("exame_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("categoria", sa.String(length=30), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("preco", sa.Numeric(10, 2), nullable=False),
        sa.Column("preparacao", sa.Text(), nullable=True),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("exame_id"),
        sa.UniqueConstraint("nome"),
    )
    op.create_index(op.f("ix_catalogo_exames_exame_id"), "catalogo_exames", ["exame_id"], unique=False)

    op.create_table(
        "catalogo_medicamentos",
        sa.Column("medicamento_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("principio_ativo", sa.String(length=120), nullable=False),
        sa.Column("dosagem", sa.String(length=60), nullable=False),
        sa.Column("forma_farmaceutica", sa.String(length=30), nullable=False),
        sa.Column("fabricante", sa.String(length=120), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("contraindicacoes", sa.Text(), nullable=True),
        sa.Column("efeitos_colaterais", sa.Text(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("medicamento_id"),
        sa.UniqueConstraint("nome"),
    )
    op.create_index(
        op.f("ix_catalogo_medicamentos_medicamento_id"),
        "catalogo_medicamentos",
        ["medicamento_id"],
        unique=False,
    )


def downgrade():
    op.drop_index(op.f("ix_catalogo_medicamentos_medicamento_id"), table_name="catalogo_medicamentos")
    op.drop_table("catalogo_medicamentos")
    op.drop_index(op.f("ix_catalogo_exames_exame_id"), table_name="catalogo_exames")
    op.drop_table("catalogo_exames")
