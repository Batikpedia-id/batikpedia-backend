"""alter_batik_table

Revision ID: 049ad49f7f65
Revises: 18dca3ad69f5
Create Date: 2024-06-15 10:31:29.792839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '049ad49f7f65'
down_revision: Union[str, None] = '18dca3ad69f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add image_name column
    op.add_column('batik', sa.Column('image_name', sa.String(length=255), nullable=True))
    pass


def downgrade() -> None:
    # drop image_name column
    op.drop_column('batik', 'image_name')
    pass
