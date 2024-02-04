import logging
from typing import Optional


from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import standard_message,standard_button, supported_language

from infrastructure.database.repo.base import BaseRepo
from infrastructure.database.repo.users import UserRepo


logger = logging.getLogger('interface')

class InterfaceRepo(BaseRepo):


    async def getSupportedLanguage(
        self,
        language: str
    )-> bool:
        
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
            
            #In order not to overload DB:
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
            logger.error("Error code no messages defined when queryng standard messages")
            return 'Error code 1. Contact administrator'
            



    async def get_ButtonLables(
        self,
        menu_key: str,
        language: str
    ):
        lang_to_use = await self.getSupportedLanguage(language)
        select_data = (
            select(standard_button.button_text, standard_button.callback_data).where(
                standard_button.menu_key==menu_key,
                standard_button.language==lang_to_use
                )
        )
        
        rows = await self.session.execute(select_data)

        return rows

