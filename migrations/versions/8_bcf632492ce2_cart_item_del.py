"""cart_item del

Revision ID: bcf632492ce2
Revises: 9ec06252ce53
Create Date: 2023-07-27 15:03:54.381670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcf632492ce2'
down_revision = '9ec06252ce53'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_item', sa.Column('cart_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'cart_item', 'cart', ['cart_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart_item', type_='foreignkey')
    op.drop_column('cart_item', 'cart_id')
    # ### end Alembic commands ###
