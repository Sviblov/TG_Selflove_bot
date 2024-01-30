"""empty message

Revision ID: 1097aa640207
Revises: 119296cd3671
Create Date: 2024-01-15 14:05:29.685152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1097aa640207'
down_revision: Union[str, None] = '119296cd3671'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('chat_id', sa.BIGINT(), nullable=False),
    sa.Column('message_id', sa.BIGINT(), nullable=False),
    sa.Column('user_from', sa.BIGINT(), nullable=False),
    sa.Column('user_to', sa.BIGINT(), nullable=False),
    sa.Column('text', sa.String(length=256), nullable=False),
    sa.Column('sent_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_from'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['user_to'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('message_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###