"""empty message

Revision ID: 9332515a9165
Revises: 9087ce4cb9bb
Create Date: 2024-01-08 17:33:00.234838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9332515a9165'
down_revision: Union[str, None] = '9087ce4cb9bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('standard_buttons',
    sa.Column('key', sa.String(length=32), autoincrement=False, nullable=False),
    sa.Column('menu_key', sa.String(length=32), autoincrement=False, nullable=False),
    sa.Column('language', sa.String(length=10), server_default=sa.text("'en'"), nullable=False),
    sa.Column('button_text', sa.String(length=256), nullable=False),
    sa.Column('callback_data', sa.String(length=32), nullable=False),
    sa.Column('comment', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('key', 'menu_key')
    )
    op.drop_table('standard_buttonss')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('standard_buttonss',
    sa.Column('key', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('menu_key', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('language', sa.VARCHAR(length=10), server_default=sa.text("'en'::character varying"), autoincrement=False, nullable=False),
    sa.Column('button_text', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('callback_data', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('comment', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('key', 'menu_key', name='standard_buttonss_pkey')
    )
    op.drop_table('standard_buttons')
    # ### end Alembic commands ###
