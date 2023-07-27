"""cart refactoring

Revision ID: 9ec06252ce53
Revises: b93b75eab492
Create Date: 2023-07-27 13:59:02.546913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ec06252ce53'
down_revision = 'b93b75eab492'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'is_ordered',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('cart', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('cart_item', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('cart_item', 'item_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart_item', 'item_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('cart_item', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('cart', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('cart', 'is_ordered',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
