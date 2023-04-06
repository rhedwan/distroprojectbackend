"""name column added with length

Revision ID: bee210102c9f
Revises: 0e2a7c77707d
Create Date: 2023-04-04 11:41:13.650406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bee210102c9f'
down_revision = '0e2a7c77707d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('name', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'name')
    # ### end Alembic commands ###