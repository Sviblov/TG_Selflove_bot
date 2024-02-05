from typing import Optional

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import text, BIGINT, Float, INT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import TEXT


from .base import Base, TimestampMixin, TableNameMixin


class sentPoll(Base):
    __tablename__ = "sent_polls"
    """
    This class represents a sent poll
    """
    poll_id: Mapped[str] = mapped_column(String(32),primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("communication_history.message_id",ondelete='CASCADE'))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.question_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    selected_answer: Mapped[int] = mapped_column(INT, nullable=True)
    