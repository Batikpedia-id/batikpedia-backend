"""create users table

Revision ID: 18dca3ad69f5
Revises: f341e8528def
Create Date: 2024-06-11 21:21:23.027658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from flask_bcrypt import Bcrypt


# revision identifiers, used by Alembic.
revision: str = '18dca3ad69f5'
down_revision: Union[str, None] = 'f341e8528def'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())
    )

    # create admin user
    bcrypt = Bcrypt()
    hashed_password = bcrypt.generate_password_hash("Pokin5432!").decode('utf-8')
    op.execute(
        """
        INSERT INTO users (username, password) VALUES ('pokin', '{}')
        """.format(hashed_password)
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
