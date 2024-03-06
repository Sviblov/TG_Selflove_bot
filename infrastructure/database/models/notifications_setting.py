from datetime import datetime
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import text, BIGINT, FLOAT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func

from sqlalchemy.dialects.postgresql import TEXT

from .base import Base


class notification_setting(Base):
    __tablename__ = "notification_settings"
    """
    This class represents a users' emotion record
    """
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    notification_type: Mapped[str]= mapped_column(String(16))
    timedelta: Mapped[str] = mapped_column(String(16))
    notification_time: Mapped[str] = mapped_column(TIMESTAMP)

    def __repr__(self):
        return f"<Emotion user:{self.user_id} >"
    