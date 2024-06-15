"""add_unique_column_batik_id_store_id_on_batik_stores


Revision ID: f5d0034c582a
Revises: 049ad49f7f65
Create Date: 2024-06-15 11:30:52.401859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5d0034c582a'
down_revision: Union[str, None] = '049ad49f7f65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('unique_batik_id_store_id', 'batik_stores', ['batik_id', 'store_id'])
    pass


def downgrade() -> None:
    op.drop_constraint('unique_batik_id_store_id', 'batik_stores')
    pass
