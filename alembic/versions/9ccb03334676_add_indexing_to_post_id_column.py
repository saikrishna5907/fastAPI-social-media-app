"""add indexing to post id column

Revision ID: 9ccb03334676
Revises: ec752e98e06f
Create Date: 2025-03-11 17:31:59.604624

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9ccb03334676'
down_revision: Union[str, None] = 'ec752e98e06f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index('ix_post_id', 'posts', ['id'])
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_post_id', table_name='posts')
    pass
