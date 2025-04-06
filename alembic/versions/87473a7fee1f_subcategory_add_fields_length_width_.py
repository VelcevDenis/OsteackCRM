"""SubCategory add fields length, width, height, price_per_piece

Revision ID: 87473a7fee1f
Revises: 9749f259d4e8
Create Date: 2025-03-31 21:30:59.742320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '87473a7fee1f'
down_revision: Union[str, None] = '9749f259d4e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add new columns to the sub_categories table
    op.add_column('sub_categories', sa.Column('length', sa.Integer(), nullable=False))
    op.add_column('sub_categories', sa.Column('width', sa.Integer(), nullable=False))
    op.add_column('sub_categories', sa.Column('height', sa.Integer(), nullable=False))
    op.add_column('sub_categories', sa.Column('price_per_piece', sa.Float(), nullable=False, server_default='0'))

def downgrade():
    # Remove the columns if rolling back
    op.drop_column('sub_categories', 'length')
    op.drop_column('sub_categories', 'width')
    op.drop_column('sub_categories', 'height')
    op.drop_column('sub_categories', 'price_per_piece')