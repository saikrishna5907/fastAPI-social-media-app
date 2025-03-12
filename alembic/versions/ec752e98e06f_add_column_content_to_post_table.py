"""add column content to post table

Revision ID: ec752e98e06f
Revises: 84c8232ab03a
Create Date: 2025-03-11 17:29:40.576017

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ec752e98e06f'
down_revision: Union[str, None] = '84c8232ab03a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
