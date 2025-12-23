"""add phone_number column to user

Revision ID: 0f4130c005d0
Revises: 
Create Date: 2025-12-09 13:55:09.922780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f4130c005d0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user",
                   sa.Column("phone",sa.String(),nullable=True)),
    op.create_unique_constraint("uq_phone_number","user",["phone"])

    # make the phone column not nullable

    op.alter_column("user","phone",existing_type=sa.String(),nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user","phone")
