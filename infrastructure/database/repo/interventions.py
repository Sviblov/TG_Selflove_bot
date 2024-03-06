import logging
from typing import Optional


from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import standard_message,standard_button, supported_language, notification_setting

from infrastructure.database.repo.base import BaseRepo
from infrastructure.database.repo.users import UserRepo
from infrastructure.database.models import emotionRecord, ntrRecord


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
    

    async def putNegativeThought(
            self,
            user_id: int,
            chat_id: int,
            negative_thought: str,
            reframing: str
        ) -> str:
        


        insert_result = insert(ntrRecord).values(
            user_id=user_id,
            chat_id=chat_id,
            negative_thought=negative_thought,
            reframing=reframing
            ).returning(ntrRecord)
        



        result = await self.session.execute(insert_result)
        
        await self.session.commit()
        return result.scalars().first()
    
    async def getNegativeThought(
            self,
            user_id: int
        ) -> Optional[emotionRecord]:
        
        result = await self.session.execute(
            select(ntrRecord).where(
                ntrRecord.user_id == user_id
            ).order_by(ntrRecord.timestamp.desc())
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

    async def setNotificationTime(
            self,
            user_id: int,
            notification_type: str,
            timedelta: int,
            notification_time: str
        ) -> str:
        
        
        

        insert_result = insert(notification_setting).values(
            user_id=user_id,
            notification_time=notification_time,
            timedelta=timedelta,
            notification_type=notification_type
            
            ).returning(notification_setting)
        
        result = await self.session.execute(insert_result)
        
        await self.session.commit()
        return result.scalars().first()
    
    async def deleteNotificationTime(
            self,
            user_id: int,
            notification_type: str
        ) -> str:
        
        delete_previous = delete(notification_setting).where(
            (notification_setting.user_id==user_id) &
            (notification_setting.notification_type==notification_type)
        )
        await self.session.execute(delete_previous)
        await self.session.commit()
        return 'done'
    

    async def deleteAllEmotions(
            self,
            user_id: int
    )-> str:
        delete_emotions = delete(emotionRecord).where(
            user_id==user_id
        )
        await self.session.execute(delete_emotions)
        await self.session.commit()
        return 'done'