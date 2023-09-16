""" add content column again

Revision ID: e29b47d0a74f
Revises: 377fd4c4ed08
Create Date: 2023-09-09 18:11:58.023926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e29b47d0a74f'
down_revision: Union[str, None] = '377fd4c4ed08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drown_column('posts', 'content')
    pass
