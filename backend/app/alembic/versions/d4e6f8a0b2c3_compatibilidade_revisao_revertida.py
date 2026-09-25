"""Mantém a cadeia de bancos que aplicaram a revisão posteriormente revertida.

Não recria agenda, dashboard ou colposcopia. Bancos já migrados preservam seus
objetos; bancos novos não precisam desses objetos para a integração de citologia.
"""

revision = "d4e6f8a0b2c3"
down_revision = "c2d4e6f8a0b1"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
