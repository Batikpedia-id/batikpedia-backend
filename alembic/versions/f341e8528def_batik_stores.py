"""batik_stores

Revision ID: f341e8528def
Revises: 995c7829c874
Create Date: 2024-06-05 16:36:57.363062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f341e8528def'
down_revision: Union[str, None] = '995c7829c874'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'batik_stores',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('batik_id', sa.Integer, sa.ForeignKey('batik.id'), nullable=False),
        sa.Column('store_id', sa.Integer, sa.ForeignKey('stores.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())
    )
    pass


def downgrade() -> None:
    op.drop_table('batik_stores')
    pass
