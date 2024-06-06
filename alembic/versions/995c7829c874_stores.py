"""stores

Revision ID: 995c7829c874
Revises: 44b5414f74a8
Create Date: 2024-06-05 16:36:51.717849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '995c7829c874'
down_revision: Union[str, None] = '44b5414f74a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'stores',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('address', sa.String, nullable=True),
        sa.Column('phone', sa.String, nullable=True),
        sa.Column('instagram', sa.String, nullable=True),
        sa.Column('tokopedia', sa.String, nullable=True),
        sa.Column('tiktok', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())
    )
    pass


def downgrade() -> None:
    op.drop_table('stores')
    pass
