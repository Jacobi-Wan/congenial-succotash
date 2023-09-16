"""add last few column to posts table

Revision ID: e57308aecfc6
Revises: c86c6336c84a
Create Date: 2023-09-15 18:06:11.371043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e57308aecfc6'
down_revision: Union[str, None] = 'c86c6336c84a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_defult=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_olumn('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
