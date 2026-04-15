"""cria historico exames e medicamentos do paciente

Revision ID: f1a2b3c4d5e6
Revises: e8a1c2f4d6b7
Create Date: 2026-04-14 20:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "f1a2b3c4d5e6"
down_revision = "e8a1c2f4d6b7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "paciente_historicos_clinicos",
        sa.Column("historico_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("paciente_id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=255), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("data_registro", sa.String(length=30), nullable=False),
        sa.ForeignKeyConstraint(["paciente_id"], ["pacientes.paciente_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("historico_id"),
    )
    op.create_index(
        op.f("ix_paciente_historicos_clinicos_historico_id"),
        "paciente_historicos_clinicos",
        ["historico_id"],
        unique=False,
    )

    op.create_table(
        "paciente_exames",
        sa.Column("paciente_exame_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("paciente_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("data_exame", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=False),
        sa.Column("resultado", sa.Text(), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column("pdf_nome", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["paciente_id"], ["pacientes.paciente_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("paciente_exame_id"),
    )
    op.create_index(
        op.f("ix_paciente_exames_paciente_exame_id"),
        "paciente_exames",
        ["paciente_exame_id"],
        unique=False,
    )

    op.create_table(
        "paciente_medicamentos",
        sa.Column("paciente_medicamento_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("paciente_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("dosagem", sa.String(length=120), nullable=True),
        sa.Column("periodo", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["paciente_id"], ["pacientes.paciente_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("paciente_medicamento_id"),
    )
    op.create_index(
        op.f("ix_paciente_medicamentos_paciente_medicamento_id"),
        "paciente_medicamentos",
        ["paciente_medicamento_id"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f("ix_paciente_medicamentos_paciente_medicamento_id"),
        table_name="paciente_medicamentos",
    )
    op.drop_table("paciente_medicamentos")
    op.drop_index(op.f("ix_paciente_exames_paciente_exame_id"), table_name="paciente_exames")
    op.drop_table("paciente_exames")
    op.drop_index(
        op.f("ix_paciente_historicos_clinicos_historico_id"),
        table_name="paciente_historicos_clinicos",
    )
    op.drop_table("paciente_historicos_clinicos")
