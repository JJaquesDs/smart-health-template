"""Rastreia tarefas de IA e permite URLs/nomes de imagem completos."""

from alembic import op
import sqlalchemy as sa

revision = "a5c7e9f1b3d5"
down_revision = "d4e6f8a0b2c3"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "exames_imagem",
        "link_imagem",
        existing_type=sa.String(45),
        type_=sa.String(255),
    )
    op.alter_column(
        "exames_imagem", "descricao", existing_type=sa.String(45), type_=sa.Text()
    )
    op.alter_column(
        "uploads_exame_imagem",
        "titulo",
        existing_type=sa.String(45),
        type_=sa.String(255),
        existing_nullable=False,
    )
    op.add_column("exames_imagem", sa.Column("task_id", sa.String(36), nullable=True))
    op.create_index(
        "ix_exames_imagem_task_id", "exames_imagem", ["task_id"], unique=True
    )
    op.add_column(
        "exames_imagem",
        sa.Column(
            "usuario_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.usuario_id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.add_column(
        "exames_imagem",
        sa.Column(
            "paciente_id",
            sa.Integer(),
            sa.ForeignKey("pacientes.paciente_id", ondelete="SET NULL"),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("exames_imagem", "paciente_id")
    op.drop_column("exames_imagem", "usuario_id")
    op.drop_index("ix_exames_imagem_task_id", table_name="exames_imagem")
    op.drop_column("exames_imagem", "task_id")
    # Não reduz campos de texto: isso poderia truncar dados já salvos.
