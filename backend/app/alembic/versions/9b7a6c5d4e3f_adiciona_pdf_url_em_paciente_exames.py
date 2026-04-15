"""adiciona pdf_url em paciente exames

Revision ID: 9b7a6c5d4e3f
Revises: f1a2b3c4d5e6
Create Date: 2026-04-14 22:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "9b7a6c5d4e3f"
down_revision = "f1a2b3c4d5e6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("paciente_exames", sa.Column("pdf_url", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("paciente_exames", "pdf_url")
