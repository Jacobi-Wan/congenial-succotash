""" create posts table again

Revision ID: 377fd4c4ed08
Revises: 21dbf34f561e
Create Date: 2023-09-09 18:11:08.533993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '377fd4c4ed08'
down_revision: Union[str, None] = '21dbf34f561e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), 
                nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass