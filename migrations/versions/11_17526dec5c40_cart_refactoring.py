"""cart refactoring

Revision ID: 17526dec5c40
Revises: c3bcdfed1316
Create Date: 2023-07-29 16:16:24.241283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17526dec5c40'
down_revision = 'c3bcdfed1316'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('is_done', sa.Boolean(),default=False, nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'is_done')
    # ### end Alembic commands ###
