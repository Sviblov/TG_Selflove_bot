import logging
from typing import Optional


from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import standard_message,standard_button, supported_language

from infrastructure.database.repo.base import BaseRepo
from infrastructure.database.repo.users import UserRepo
from infrastructure.database.models import emotionRecord


logger = logging.getLogger('interface')

class InterventionsRepo(BaseRepo):

    async def putEmotion(
            self,
            user_id: int,
            chat_id: int,
            emotion: str,
            what_thinking: str,
            what_doing: str
        ) -> str:
        
        emotionName = await self.getEmotionNamebyKey(emotion)

        insert_result = insert(emotionRecord).values(
            user_id=user_id,
            chat_id=chat_id,
            emotion=emotionName,
            what_thinking=what_thinking,
            what_doing=what_doing
            ).returning(emotionRecord)
        



        result = await self.session.execute(insert_result)
        
        await self.session.commit()
        return result.scalars().first()
    
    async def getEmotions(
            self,
            user_id: int
        ) -> Optional[emotionRecord]:
        
        result = await self.session.execute(
            select(emotionRecord).where(
                emotionRecord.user_id == user_id
            ).order_by(emotionRecord.timestamp.desc())
        )
        return result.scalars()

    async def getEmotionNamebyKey(self,
                                key: str
        ) -> Optional[str]:
        result = await self.session.execute(
            select(standard_button.button_text).where(
                standard_button.key == key
            )
        )
        return result.scalars().first()
        
