"""add content column to posts table

Revision ID: 65b49ba4e5dc
Revises: 7d61663505b7
Create Date: 2023-09-08 18:21:43.823416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65b49ba4e5dc'
down_revision: Union[str, None] = '7d61663505b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drown_column('posts', 'content')
    pass
