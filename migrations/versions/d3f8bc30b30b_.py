"""empty message

Revision ID: d3f8bc30b30b
Revises: 9de4dc5c45d2
Create Date: 2024-03-06 14:43:46.035343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3f8bc30b30b'
down_revision: Union[str, None] = '9de4dc5c45d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('emotion_records_user_id_fkey', 'emotion_records', type_='foreignkey')
    op.create_foreign_key(None, 'emotion_records', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    # op.alter_column('notification_settings', 'timedelta',
    #            existing_type=sa.VARCHAR(length=16),
    #            type_=sa.INTEGER(),
    #            existing_nullable=False)
    op.drop_constraint('notification_settings_user_id_fkey', 'notification_settings', type_='foreignkey')
    op.create_foreign_key(None, 'notification_settings', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'notification_settings', type_='foreignkey')
    op.create_foreign_key('notification_settings_user_id_fkey', 'notification_settings', 'users', ['user_id'], ['user_id'])
    op.alter_column('notification_settings', 'timedelta',
               existing_type=sa.INTEGER(),
               type_=sa.VARCHAR(length=16),
               existing_nullable=False)
    op.drop_constraint(None, 'emotion_records', type_='foreignkey')
    op.create_foreign_key('emotion_records_user_id_fkey', 'emotion_records', 'users', ['user_id'], ['user_id'])
    # ### end Alembic commands ###
