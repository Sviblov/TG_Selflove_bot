from typing import Optional

from sqlalchemy import String
from sqlalchemy import text, BIGINT, Boolean, true
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from aiogram.types import InlineKeyboardButton
from .base import Base, TimestampMixin, TableNameMixin


class standard_message(Base,TableNameMixin):
    """
    This class represents a Standard Message in the application.
    """
    key: Mapped[str]  = mapped_column(String(32), primary_key=True, autoincrement=False)
    language: Mapped[str] = mapped_column(String(10),primary_key=True, server_default=text("'en'"))
    message: Mapped[str]  = mapped_column(TEXT)
    comment: Mapped[str]  = mapped_column(String(256))


    def __repr__(self):
        return f"<StandardMessage {self.key} {self.language}>"
    

class standard_button(Base,TableNameMixin):
    """
    This class represents a Standard Message in the application.
    """
    key: Mapped[str]  = mapped_column(String(32), primary_key=True, autoincrement=False)
    menu_key: Mapped[str]  = mapped_column(String(32),primary_key=True, autoincrement=False)
    language: Mapped[str] = mapped_column(String(10), primary_key=True, server_default=text("'en'"))
    button_text: Mapped[str]  = mapped_column(String(256))
    callback_data: Mapped[str]  = mapped_column(String(32))
    comment: Mapped[str]  = mapped_column(String(256))


    def __repr__(self):
        return f"<StandardMessage {self.key} {self.language}>"
    
    def as_keyboard(self):
        return {
            f'{self.key}': InlineKeyboardButton(
            text=self.button_text,
            callback_data=self.callback_data
            )
            }