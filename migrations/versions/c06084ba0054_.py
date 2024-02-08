"""empty message

Revision ID: c06084ba0054
Revises: b3f802017ffe
Create Date: 2024-02-08 05:19:31.594145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c06084ba0054'
down_revision: Union[str, None] = 'b3f802017ffe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('poll_results',
    sa.Column('poll_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('score', sa.INTEGER(), nullable=False),
    sa.Column('is_valid', sa.BOOLEAN(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('poll_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('poll_results')
    # ### end Alembic commands ###
