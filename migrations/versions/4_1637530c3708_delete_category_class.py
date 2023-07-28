"""delete category class

Revision ID: 1637530c3708
Revises: b92c9493ac0b
Create Date: 2023-07-27 09:26:15.080342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1637530c3708'
down_revision = 'b92c9493ac0b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_category_id', table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='category_pkey')
    )
    op.create_index('ix_category_id', 'category', ['id'], unique=False)
    # ### end Alembic commands ###