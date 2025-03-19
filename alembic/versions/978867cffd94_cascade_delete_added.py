"""cascade delete added

Revision ID: 978867cffd94
Revises: 5da4e63b01fd
Create Date: 2025-03-19 20:00:28.647846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '978867cffd94'
down_revision: Union[str, None] = '5da4e63b01fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('presentations_report_id_fkey', 'presentations', type_='foreignkey')
    op.create_foreign_key(None, 'presentations', 'reports', ['report_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('users_presentations_presentation_id_fkey', 'users_presentations', type_='foreignkey')
    op.create_foreign_key(None, 'users_presentations', 'presentations', ['presentation_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('users_reports_report_id_fkey', 'users_reports', type_='foreignkey')
    op.drop_constraint('users_reports_user_id_fkey', 'users_reports', type_='foreignkey')
    op.create_foreign_key(None, 'users_reports', 'reports', ['report_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'users_reports', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_reports', type_='foreignkey')
    op.drop_constraint(None, 'users_reports', type_='foreignkey')
    op.create_foreign_key('users_reports_user_id_fkey', 'users_reports', 'users', ['user_id'], ['id'])
    op.create_foreign_key('users_reports_report_id_fkey', 'users_reports', 'reports', ['report_id'], ['id'])
    op.drop_constraint(None, 'users_presentations', type_='foreignkey')
    op.create_foreign_key('users_presentations_presentation_id_fkey', 'users_presentations', 'presentations', ['presentation_id'], ['id'])
    op.drop_constraint(None, 'presentations', type_='foreignkey')
    op.create_foreign_key('presentations_report_id_fkey', 'presentations', 'reports', ['report_id'], ['id'])
    # ### end Alembic commands ###
