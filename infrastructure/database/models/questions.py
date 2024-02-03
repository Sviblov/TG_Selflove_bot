from typing import Optional

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import text, BIGINT, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import TEXT


from .base import Base, TimestampMixin, TableNameMixin


class question(Base):
    __tablename__ = "questions"
    """
    This class represents a question in questinaire the application.
    """
    question_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    questionaire_id: Mapped[int] = mapped_column(ForeignKey("questionaires.questionaire_id"))
    language: Mapped[str] = mapped_column(String(10), server_default=text("'en'"))
    question: Mapped[str]  = mapped_column(TEXT)
    comment: Mapped[str]  = mapped_column(String(256))


    def __repr__(self):
        return f"<Question {self.question_id} >"

class questionaire(Base):
    __tablename__ = "questionaires"
    """
    This class represents a question in questinaire the application.
    """
    questionaire_id: Mapped[int]  = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    language: Mapped[str] = mapped_column(String(10), server_default=text("'en'"))
    questionare_name: Mapped[str]  = mapped_column(String(256))
    comment: Mapped[str]  = mapped_column(String(256))


    def __repr__(self):
        return f"<Questionaire {self.questionaire_id}>"


class answer_option(Base,TableNameMixin):
    __tablename__ = "answer_options"
    """
    This class represents a question in questinaire the application.
    """
    answer_id: Mapped[int]  = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.question_id"))
    language: Mapped[str] = mapped_column(String(10), server_default=text("'en'"))
    answer: Mapped[str]  = mapped_column(String(256))
    weight: Mapped[float]   = mapped_column(Float())
    comment: Mapped[str]  = mapped_column(String(256))


    def __repr__(self):
        return f"<answer_option {self.answer_id}>"