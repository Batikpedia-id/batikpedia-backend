"""add_on_delete_cascade_batik_stores

Revision ID: 72f7781daab9
Revises: f5d0034c582a
Create Date: 2024-06-15 12:02:31.236428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72f7781daab9'
down_revision: Union[str, None] = 'f5d0034c582a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add on delete cascade store_id
    op.drop_constraint('batik_stores_store_id_fkey', 'batik_stores')
    op.create_foreign_key('batik_stores_store_id_fkey', 'batik_stores', 'stores', ['store_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    # drop on delete cascade store_id
    op.drop_constraint('batik_stores_store_id_fkey', 'batik_stores')
    pass
