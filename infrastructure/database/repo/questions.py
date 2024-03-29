import logging
from typing import List


from sqlalchemy import func, select


from infrastructure.database.models import question, questions, answer_option

from infrastructure.database.repo.base import BaseRepo

logger = logging.getLogger('questions')

class QuestionRepo(BaseRepo):

    async def get_Question(
        self,
        questionaire_id: int,
        order: int,
        language: str,
    ) -> question:
        
        # select_data = (
        #     select(standard_message.message).where(
        #         standard_message.key==key,
        #         standard_message.language==language
        #         )
        # )

        valid_languages = ['en', 'ru']
        if language not in valid_languages:
            lang_to_use = 'en'
        else:
            lang_to_use = language

        select_data = select(question).where(question.questionaire_id==questionaire_id, question.order == order,question.language==lang_to_use)

        questions = await self.session.execute(select_data)

        return questions.scalars().first()
    
    async def get_NumberOfQuestions(
        self,
        questionaire_id: int,
        language: str,
    ) -> int:
        
        valid_languages = ['en', 'ru']
        if language not in valid_languages:
            lang_to_use = 'en'
        else:
            lang_to_use = language
        
        select_data = select(func.count(question.order)).where(question.questionaire_id==questionaire_id, question.language==lang_to_use)

        questions = await self.session.execute(select_data)

        return questions.scalar()

    async def get_Answers(
        self,
        question_id: int,
        language: str,
    ) -> List[answer_option]:
        
        valid_languages = ['en', 'ru']
        if language not in valid_languages:
            lang_to_use = 'en'
        else:
            lang_to_use = language

        select_data = select(answer_option).where(answer_option.question_id==question_id, answer_option.language==lang_to_use)

        answers = await self.session.execute(select_data)

        return answers.scalars()
