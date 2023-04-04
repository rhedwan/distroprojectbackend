"""transaction table corrections

Revision ID: 3d8f4116fd14
Revises: d613475cd2d5
Create Date: 2023-03-29 17:33:04.907436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d8f4116fd14'
down_revision = 'd613475cd2d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('transaction_id', 'transaction', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('transaction_id', 'transaction', type_='unique')
    # ### end Alembic commands ###