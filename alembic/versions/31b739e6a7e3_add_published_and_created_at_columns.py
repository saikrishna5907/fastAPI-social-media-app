"""add published and created_at columns

Revision ID: 31b739e6a7e3
Revises: a036fb6a6ed2
Create Date: 2025-03-11 18:01:21.223499

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '31b739e6a7e3'
down_revision: Union[str, None] = 'a036fb6a6ed2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
