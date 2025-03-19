"""create table votes

Revision ID: ff9b442bb09d
Revises: 31b739e6a7e3
Create Date: 2025-03-11 18:11:47.373284

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ff9b442bb09d'
down_revision: Union[str, None] = '31b739e6a7e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("votes", 
                    sa.Column("user_id", sa.INTEGER(), nullable=False, primary_key=True),
                    sa.Column("post_id", sa.INTEGER(), nullable=False, primary_key=True),
                    sa.Column("flag", sa.INTEGER(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.CheckConstraint("flag IN (0, 1)", name="check_flag_values")
    ),

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("votes")
