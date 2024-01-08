from typing import Optional

from sqlalchemy import String
from sqlalchemy import text, BIGINT, Boolean, true
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class standard_message(Base,TableNameMixin):
    """
    This class represents a Standard Message in the application.
    """
    key: Mapped[str]  = mapped_column(String(32), primary_key=True, autoincrement=False)
    language: Mapped[str] = mapped_column(String(10), server_default=text("'en'"))
    message: Mapped[str]  = mapped_column(String(256))
    comment: Mapped[str]  = mapped_column(String(256))


    def __repr__(self):
        return f"<StandardMessage {self.key} {self.language}>"