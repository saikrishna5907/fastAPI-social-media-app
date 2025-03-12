"""add foreign-key to posts table

Revision ID: a036fb6a6ed2
Revises: 867935100c43
Create Date: 2025-03-11 17:47:23.115342

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a036fb6a6ed2'
down_revision: Union[str, None] = '867935100c43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts', 
        sa.Column('user_id', 
                  sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE', name='posts_users_fkey'), 
                  nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'user_id')
    pass
