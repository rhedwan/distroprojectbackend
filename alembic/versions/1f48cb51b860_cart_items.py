"""cart_items

Revision ID: 1f48cb51b860
Revises: 3961f2467c39
Create Date: 2023-04-02 01:07:48.409420

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1f48cb51b860'
down_revision = '3961f2467c39'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart_items',
    sa.Column('pkid', sa.Integer(), nullable=False),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('checkout_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['checkout_id'], ['cart.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('pkid'),
    sa.UniqueConstraint('id')
    )
    op.add_column('cart', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'created_at')
    op.drop_table('cart_items')
    # ### end Alembic commands ###