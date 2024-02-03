import logging
from typing import Optional, List


from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import questionaire, question, questions

from infrastructure.database.repo.base import BaseRepo

logger = logging.getLogger('questions')

class getQuestions(BaseRepo):
    async def get_Questions(
        self,
        questionaire_id: int,
        language: str,
    ) -> List[question]:
        
        # select_data = (
        #     select(standard_message.message).where(
        #         standard_message.key==key,
        #         standard_message.language==language
        #         )
        # )

        select_data = select(question).where(question.questionaire_id==questionaire_id, question.language==language)

        questions = await self.session.execute(select_data)

        return questions
