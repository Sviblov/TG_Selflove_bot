
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import text, BIGINT, FLOAT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func
import datetime
from sqlalchemy.dialects.postgresql import TEXT

from .base import Base

class message(Base):
    __tablename__ = "communication_history"
    """
    This class represents a messages sent by users
    """
    chat_id: Mapped[int] = mapped_column(BIGINT)
    message_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    message_type: Mapped[str] = mapped_column(String(16))
    user_from: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user_to: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    text: Mapped[str]  = mapped_column(TEXT,nullable=True)
    sent_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<Message {self.message_id} >"