"""empty message

Revision ID: 6251d0e33033
Revises: a574ff8ecb12
Create Date: 2024-02-05 11:26:05.742200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6251d0e33033'
down_revision: Union[str, None] = 'a574ff8ecb12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sent_polls', 'poll_id',
               existing_type=sa.BIGINT(),
               type_=sa.String(length=32),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sent_polls', 'poll_id',
               existing_type=sa.String(length=32),
               type_=sa.BIGINT(),
               existing_nullable=False)
    # ### end Alembic commands ###
