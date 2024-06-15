"""alter_batik_table_add_treshold_column

Revision ID: 7972ee894c6c
Revises: 72f7781daab9
Create Date: 2024-06-15 12:09:05.329981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7972ee894c6c'
down_revision: Union[str, None] = '72f7781daab9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('batik', sa.Column('treshold', sa.Integer(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('batik', 'treshold')
    pass
