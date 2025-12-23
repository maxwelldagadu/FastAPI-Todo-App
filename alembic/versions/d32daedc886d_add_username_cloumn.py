"""add username cloumn

Revision ID: d32daedc886d
Revises: 0f4130c005d0
Create Date: 2025-12-17 01:16:18.956027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd32daedc886d'
down_revision: Union[str, Sequence[str], None] = '0f4130c005d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user",sa.Column("username",sa.String(),nullable=True))

    op.create_unique_constraint("uq_username","user",["username"])
     
    # username nullabe False
    op.alter_column("user","username",existing_type=sa.String(),nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    pass
