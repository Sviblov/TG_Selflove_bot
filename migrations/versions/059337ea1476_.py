"""empty message

Revision ID: 059337ea1476
Revises: 00e576bec3d2
Create Date: 2024-02-04 17:47:53.375052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '059337ea1476'
down_revision: Union[str, None] = '00e576bec3d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supported_languages',
    sa.Column('lang_id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('language', sa.String(length=2), server_default=sa.text("'en'"), nullable=False),
    sa.Column('language_full', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('lang_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supported_languages')
    # ### end Alembic commands ###
