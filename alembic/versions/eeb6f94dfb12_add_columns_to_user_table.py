"""add columns to user table

Revision ID: eeb6f94dfb12
Revises: ff9b442bb09d
Create Date: 2025-03-12 15:03:36.945478

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'eeb6f94dfb12'
down_revision: Union[str, None] = 'ff9b442bb09d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone', sa.String(), nullable=False))
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('active', sa.Boolean(), server_default=sa.text('true'), default=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'active')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'phone')
    pass
