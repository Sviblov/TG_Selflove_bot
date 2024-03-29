"""empty message

Revision ID: 65eebc01eb3f
Revises: 06ef76f5b0df
Create Date: 2024-03-08 16:22:43.062591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65eebc01eb3f'
down_revision: Union[str, None] = '06ef76f5b0df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification_settings', sa.Column('language', sa.String(length=10), server_default=sa.text("'en'"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification_settings', 'language')
    # ### end Alembic commands ###
