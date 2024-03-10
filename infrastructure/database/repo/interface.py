import logging
from typing import Optional


from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import standard_message,standard_button, supported_language, feedback_message

from infrastructure.database.repo.base import BaseRepo
from infrastructure.database.repo.users import UserRepo
from aiogram.types import Message

logger = logging.getLogger('interface')

class InterfaceRepo(BaseRepo):


    async def getSupportedLanguage(
        self,
        language: str
    ) -> str:
        """
        Retrieve the supported language from the database.

        Args:
            language (str): The language to check for support.

        Returns:
            str: The supported language.
        """
        select_data = select(supported_language).where(supported_language.language==language)
        result = await self.session.execute(select_data)
        first_row = result.first()
        if first_row:
            return language
        else:
            # select_data=select(supported_language).where(supported_language.is_default==True)
            # result = await self.session.execute(select_data)
            # first_row: supported_language=result.first()
            # return first_row.language
            
            # In order not to overload DB:
            return 'en'
        

    async def get_messageText(
        self,
        key: str,
        language: str
    ):
        
        #checking for user language is present in the table:
        lang_to_use = await self.getSupportedLanguage(language)
        
       
        select_data = (
            select(standard_message).where(
                standard_message.key==key,
                standard_message.language==lang_to_use
                )
        )
        
        row: standard_message = await self.session.scalar(select_data)
        
     
        
        if row:
             return row.message    
        else:
            
            logger.warn(f"No Russian messages defined when queryng standard messages: {key}")
            select_data_en = (
                select(standard_message).where(
                    standard_message.key==key,
                    standard_message.language=='en'
                    )
            )

            row_en: standard_message = await self.session.scalar(select_data_en)
            if row_en:
                return row_en.message
            else:

                logger.error(f"Error code no messages defined when queryng standard messages: {key}")
                return 'Message error. Contact administrator'
            



    async def get_ButtonLables(
        self,
        menu_key: str,
        language: str
    ):
        lang_to_use = await self.getSupportedLanguage(language)

        select_data = (
            select(standard_button).where(
                standard_button.menu_key==menu_key,
                standard_button.language==lang_to_use
                )
        )

        
        
        rows = await self.session.execute(select_data)
        rows_scalar = rows.scalars().all()
        if len(rows_scalar) > 0:
            return rows_scalar
        else: 
            logger.warn(f"No Russian buttons defined when queryng standard button: {menu_key}")
            select_data_en = (
                select(standard_button).where(
                    standard_button.menu_key==menu_key,
                    standard_button.language=='en'
                    )
            )
            rows_en = await self.session.execute(select_data_en)
            return rows_en.scalars().all()

    

    async def putFeedback(
        self,
        message: Message,
        user_id: int
    ):
        insert_data = insert(feedback_message).values(
            user_from=user_id,
            feedback_text=message.text
        )
        await self.session.execute(insert_data)
        await self.session.commit()
        