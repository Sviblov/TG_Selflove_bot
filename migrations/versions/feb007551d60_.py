"""empty message

Revision ID: feb007551d60
Revises: 0d08114bfb90
Create Date: 2024-02-05 10:02:24.619614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'feb007551d60'
down_revision: Union[str, None] = '0d08114bfb90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer_options', 'answer_index',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer_options', 'answer_index',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
