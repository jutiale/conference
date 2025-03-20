"""add demo data

Revision ID: f76326d22621
Revises: 878b9c30c8e6
Create Date: 2025-03-20 16:29:28.058796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.

revision: str = 'f76326d22621'
down_revision: Union[str, None] = '878b9c30c8e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(f"""
            INSERT INTO users (name, password_hash) VALUES
            ('user1', '$2b$12$O0dKQWLKKsIEz/FZa/X6meSCWc5ft4lcoV2Sl2vo.2YpUyN2G7Dbm'),
            ('user2', '$2b$12$iGUOV5mYDScia1aMy3rn.uZ/UAsY60hnojPmuWxmLnVwfHNpoU6vW');
            
            INSERT INTO reports (name, text) VALUES
            ('test_report_1', 'test_report_text'),
            ('test_report_2', 'test_report_text');
            INSERT INTO users_reports (user_id, report_id) VALUES
            (1, 1), (2, 2);
            
            INSERT INTO rooms (name) VALUES ('361'), ('454');
            
            INSERT INTO presentations(report_id, time_start, time_end, room_id) VALUES
            (1, '2025-03-20T13:30:00', '2025-03-20T13:50:00', 1),
            (2, '2025-03-20T13:30:00', '2025-03-20T13:50:00', 2),
            (1, '2025-03-20T14:30:00', '2025-03-20T14:50:00', 2);
            
            INSERT INTO users_presentations(user_id, presentation_id, user_role) VALUES
            (1, 1, 'presenter'), (1, 3, 'presenter'), (2, 2, 'presenter'), (2, 3, 'listener');
            
        """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(f"""
                DELETE from users where users.id < 3;
                
                DELETE FROM rooms where rooms.id < 3;

            """)
    pass
