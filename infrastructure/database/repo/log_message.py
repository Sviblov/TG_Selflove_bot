import logging
from typing import Optional



from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import message as logmessage

from infrastructure.database.repo.base import BaseRepo

from aiogram.types import Message

logger = logging.getLogger('log_message')

class logMessageRepo(BaseRepo):
    async def put_message(
        self,
        message: Message,
        user_to: int,
        user_from: int
    ):
    #     chat_id: Mapped[int] = mapped_column(BIGINT)
    # message_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    # message_type: Mapped[str] = mapped_column(String(16))
    # user_from: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    # user_to: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    # text: Mapped[str]  = mapped_column(String(256))
    # sent_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
        
        

        insert_log_message = (
            insert(logmessage)
            .values(
                chat_id=message.chat.id,
                message_id=message.message_id,
                message_type=message.content_type,
                user_from=user_from,
                user_to=user_to,
                text=message.text,
                sent_at=message.date.replace(tzinfo=None)
            )
            
        )
        result = await self.session.execute(insert_log_message)

        await self.session.commit()
      