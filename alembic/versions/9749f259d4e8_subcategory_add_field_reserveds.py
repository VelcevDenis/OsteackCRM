"""SubCategory add field booked

Revision ID: 9749f259d4e8
Revises: 2fd05ef3f3c0
Create Date: 2025-03-21 14:09:09.290779
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9749f259d4e8'
down_revision: Union[str, None] = '2fd05ef3f3c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the 'booked' column to the 'sub_categories' table
    op.add_column('sub_categories', sa.Column('booked', sa.Integer(), nullable=False, default=0))

    # If necessary, create index on the new column (Optional)
    op.create_index(op.f('ix_sub_categories_booked'), 'sub_categories', ['booked'], unique=False)


def downgrade() -> None:
    # Remove the 'booked' column if downgrading
    op.drop_column('sub_categories', 'booked')

    # Drop the index on the 'booked' column (if it was created)
    op.drop_index(op.f('ix_sub_categories_booked'), table_name='sub_categories')
