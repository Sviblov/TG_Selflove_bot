import logging
from typing import Optional



from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete

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

    async def get_messages(
      self,
      user_id: int      
    ):
        select_data = select(logmessage.chat_id, logmessage.message_id).where(
                    (logmessage.user_from==user_id) | (logmessage.user_to==user_id)
                    )
        

        allMessages = await self.session.execute(select_data)
       
        return allMessages
    
    async def delete_messages(
      self,
      user_id: int      
    ):
        delete_data = delete(logmessage).where(
                    (logmessage.user_from==user_id) | (logmessage.user_to==user_id)
                    )
        
        
        deleteMessages = await self.session.execute(delete_data)
        await self.session.commit()
