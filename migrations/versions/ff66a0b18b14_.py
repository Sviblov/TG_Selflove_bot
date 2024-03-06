"""empty message

Revision ID: ff66a0b18b14
Revises: 3b988b05f55b
Create Date: 2024-03-06 10:02:05.050014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ff66a0b18b14'
down_revision: Union[str, None] = '3b988b05f55b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback_messages',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('user_from', sa.BIGINT(), nullable=False),
    sa.Column('feedback_text', sa.TEXT(), nullable=True),
    sa.Column('sent_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_from'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification_settings',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('notification_type', sa.String(length=16), nullable=False),
    sa.Column('timedelta', sa.String(length=16), nullable=False),
    sa.Column('notification_time', postgresql.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'emotion_records', 'users', ['user_id'], ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'emotion_records', type_='foreignkey')
    op.drop_table('notification_settings')
    op.drop_table('feedback_messages')
    # ### end Alembic commands ###
