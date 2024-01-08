import logging
from typing import Optional


from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import standard_message
from infrastructure.database.models import standard_button
from infrastructure.database.repo.base import BaseRepo

logger = logging.getLogger('standard_messages')

class standardMessageRepo(BaseRepo):
    async def get_standardMessages(
        self,
        key: str,
        language: str
    ):
        
        select_data = (
            select(standard_message.message).where(
                standard_message.key==key,
                standard_message.language==language
                )
        )
        
        row = await self.session.execute(select_data)

        first_row=row.first()
        
        if first_row is None:
            message = "Error code 1. Contact administrator"
            logger.error("Error code no messages defined when queryng standard messages")
        else:
            message = first_row[0]


        return message

class standardButtonsRepo(BaseRepo):
    async def get_standardButtons(
        self,
        menu_key: str,
        language: str
    ):
        
        select_data = (
            select(standard_button.button_text, standard_button.callback_data).where(
                standard_button.menu_key==menu_key,
                standard_button.language==language
                )
        )
        
        rows = await self.session.execute(select_data)

        return rows