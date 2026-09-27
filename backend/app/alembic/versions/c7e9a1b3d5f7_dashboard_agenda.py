"""Dados persistentes para agenda do dashboard."""

import sqlalchemy as sa
from alembic import op

revision = "c7e9a1b3d5f7"
down_revision = "b6d8f0a2c4e6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "consultas", sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "consultas",
        sa.Column("status", sa.String(10), nullable=False, server_default="waiting"),
    )
    op.add_column("consultas", sa.Column("observacoes", sa.Text(), nullable=True))
    op.alter_column(
        "consultas", "secretaria_id", existing_type=sa.Integer(), nullable=True
    )
    op.create_check_constraint(
        "ck_consultas_status",
        "consultas",
        "status IN ('waiting','confirmed','cancelled')",
    )


def downgrade():
    op.drop_constraint("ck_consultas_status", "consultas", type_="check")
    for name in ("observacoes", "status", "starts_at"):
        op.drop_column("consultas", name)
    # Mantém secretaria_id opcional para preservar consultas de superusuários.
