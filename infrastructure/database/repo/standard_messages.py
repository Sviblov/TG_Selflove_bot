from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import standard_message
from infrastructure.database.repo.base import BaseRepo


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
        
        return first_row[0]
