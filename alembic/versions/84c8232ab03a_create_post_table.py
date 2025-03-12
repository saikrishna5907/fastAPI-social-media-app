"""Create Post Table

Revision ID: 84c8232ab03a
Revises: 
Create Date: 2025-03-11 16:41:54.866013

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '84c8232ab03a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', 
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False)
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
