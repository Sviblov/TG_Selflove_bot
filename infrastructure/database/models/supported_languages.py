from typing import Optional

from sqlalchemy import String, text, Boolean, false

from sqlalchemy.dialects.postgresql import TEXT, BIGINT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class supported_language(Base):
    """
    This class represents a Standard Message in the application.
    """
    __tablename__ = "supported_languages"
    lang_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    language: Mapped[str] = mapped_column(String(2), server_default=text("'en'"))
    language_full: Mapped[str]  = mapped_column(String(15))
    is_default: Mapped[bool] = mapped_column(Boolean, server_default=false())
    


    def __repr__(self):
        return f"<{self.language} language>"
    