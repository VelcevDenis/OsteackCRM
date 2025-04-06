"""Add total_price and description to products

Revision ID: 367cac70a0c7
Revises: 87473a7fee1f
Create Date: 2025-03-31 22:48:01.353878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '367cac70a0c7'
down_revision: Union[str, None] = '87473a7fee1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new columns to the products table
    op.add_column('products', sa.Column('total_price', sa.Float(), nullable=False, server_default='0'))
    op.add_column('products', sa.Column('description', sa.Text(), nullable=True))


def downgrade():
    # Remove the columns in case of rollback
    op.drop_column('products', 'total_price')
    op.drop_column('products', 'description')
