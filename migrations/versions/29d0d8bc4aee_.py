"""empty message

Revision ID: 29d0d8bc4aee
Revises: 
Create Date: 2019-12-04 11:40:21.842737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d0d8bc4aee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=18), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=100), nullable=False),
    sa.Column('brand', sa.String(length=20), nullable=False),
    sa.Column('picture_file', sa.String(length=20), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(precision=2), nullable=False),
    sa.Column('php_rate', sa.Float(precision=2), nullable=True),
    sa.Column('order_details', sa.String(length=200), nullable=True),
    sa.Column('url', sa.String(length=2048), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Float(precision=2), nullable=False),
    sa.Column('balance', sa.String(length=10), nullable=True),
    sa.Column('shipping_fee', sa.Integer(), nullable=True),
    sa.Column('order_status', sa.String(length=10), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cart_id')
    )
    op.create_table('shipment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tracking_number', sa.String(), nullable=True),
    sa.Column('estimated_date', sa.Date(), nullable=True),
    sa.Column('picture1', sa.String(length=25), nullable=True),
    sa.Column('picture2', sa.String(length=25), nullable=True),
    sa.Column('picture3', sa.String(length=25), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shipment')
    op.drop_table('order')
    op.drop_table('cart')
    op.drop_table('user')
    # ### end Alembic commands ###
