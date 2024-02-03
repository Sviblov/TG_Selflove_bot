"""empty message

Revision ID: 00e576bec3d2
Revises: c46c7cba6e1c
Create Date: 2024-02-03 19:13:49.013331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00e576bec3d2'
down_revision: Union[str, None] = 'c46c7cba6e1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'question',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.TEXT(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'question',
               existing_type=sa.TEXT(),
               type_=sa.VARCHAR(length=256),
               existing_nullable=False)
    # ### end Alembic commands ###
