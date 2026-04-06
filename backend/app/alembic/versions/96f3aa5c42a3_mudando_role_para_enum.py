"""mudando role para enum

Revision ID: 96f3aa5c42a3
Revises: 6ecb7ab6d383
Create Date: 2026-04-06 12:38:04.978836

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '96f3aa5c42a3'
down_revision = '6ecb7ab6d383'
branch_labels = None
depends_on = None


def upgrade():
    # Cria o ENUM no banco
    user_role_enum = sa.Enum(
        'USER', 'SUPERUSER', 'ADMIN', 'SECRETARIA', 'MEDICO',
        name='userrole'
    )
    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.execute("UPDATE usuarios SET role = UPPER(role)")

    # Converter a coluna para ENUM
    op.alter_column(
        'usuarios',
        'role',
        existing_type=sa.VARCHAR(length=15),
        type_=user_role_enum,
        postgresql_using="role::userrole"
    )


def downgrade():
    # Voltar para VARCHAR
    op.alter_column(
        'usuarios',
        'role',
        existing_type=sa.Enum(name='userrole'),
        type_=sa.VARCHAR(length=15),
    )

    # Dropar o ENUM
    user_role_enum = sa.Enum(
        'USER', 'SUPERUSER', 'ADMIN', 'SECRETARIA', 'MEDICO',
        name='userrole'
    )
    user_role_enum.drop(op.get_bind(), checkfirst=True)