"""create_batik_table

Revision ID: 44b5414f74a8
Revises: 
Create Date: 2024-06-05 16:34:44.978310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44b5414f74a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'batik',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('code', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('image', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())
    )
    pass


def downgrade() -> None:
    op.drop_table('batik')
    pass
