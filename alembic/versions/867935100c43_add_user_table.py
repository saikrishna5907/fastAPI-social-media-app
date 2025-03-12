"""add user table

Revision ID: 867935100c43
Revises: 9ccb03334676
Create Date: 2025-03-11 17:38:02.163023

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '867935100c43'
down_revision: Union[str, None] = '9ccb03334676'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
