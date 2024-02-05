import logging
from typing import Optional, Union


from sqlalchemy import select, insert, update

from infrastructure.database.models import sentPoll

from infrastructure.database.repo.base import BaseRepo
from infrastructure.database.repo.users import UserRepo


logger = logging.getLogger('ResultRepo')

class ResultsRepo(BaseRepo):


    async def putSentQuestion(
        self,
        poll_id: str,
        message_id: int,
        question_id: int,
        user_id: Union[int,str],
        answer: int = None
    ):
        
        insert_poll = insert(sentPoll).values(
            poll_id=poll_id,
            message_id=message_id,
            question_id=question_id,
            user_id=user_id,
            selected_answer=answer,
            ).returning(sentPoll)
        result = await self.session.execute(insert_poll)
        await self.session.commit()
    

    async def updatePollResult(
            self,
            poll_id: str,
            answer: int = None,

    ):
        update_request = update(sentPoll).where(
            sentPoll.poll_id==poll_id
            ).values(
                selected_answer=answer
                )
        result = await self.session.execute(update_request)
        await self.session.commit()

        