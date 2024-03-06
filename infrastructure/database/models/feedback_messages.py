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

class feedback_message(Base):
    __tablename__ = "feedback_messages"
    """
    This class represents a messages sent by users
    """
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_from: Mapped[int] = mapped_column(BIGINT)
    feedback_text: Mapped[str]  = mapped_column(TEXT,nullable=True)
    sent_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<Message {self.message_id} >"