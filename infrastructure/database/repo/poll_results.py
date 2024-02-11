import logging
from typing import Optional, Union


from sqlalchemy import select, insert, update, and_, delete
from sqlalchemy.sql.expression import func

from infrastructure.database.models import sentPoll, pollResults, answer_option

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

    async def isPollAnswered(
            self,
            poll_id: str,
            user_id: Union[int,str],
    ):
        pass
    

    async def getUncompletedNumber(
            self,
            user_id: int,
    ):
        """
        Get the number of questions that are not answered by the user
        
        """
        
        #TODO: improve this select in order not to query 2 times
        count_answered = select(func.count(sentPoll.selected_answer)).where(sentPoll.user_id==user_id)
        count_all= select(func.count(sentPoll.user_id)).where(sentPoll.user_id==user_id)
        
        result_answered = await self.session.execute(count_answered)
        result_all= await self.session.execute(count_all)

        
        return result_all.scalar()-result_answered.scalar()
    
    async def calculateTestResult(
        self,
        user_id: Union[int,str],
    ):
        """
        Calculate the result of the poll
        """
        test_results=select(answer_option.weight).select_from(sentPoll, answer_option).join(
            answer_option, 
            and_(
                sentPoll.question_id==answer_option.question_id, 
                sentPoll.selected_answer==answer_option.answer_index),
            isouter=True
            ).where(sentPoll.user_id==user_id)
        result = await self.session.execute(test_results)
        result_scalar = result.scalars()

        return sum(result_scalar)

    async def saveTestResult(
        self,
        user_id: Union[int,str],
        score: int,
        severity: int=0,
    ):
        """
        Save the result of the poll
        """
        update_request = update(pollResults).where(
            pollResults.user_id==user_id
            ).values(
                is_valid=False
                )
        await self.session.execute(update_request)
        await self.session.commit()

        insert_result = insert(pollResults).values(
            user_id=user_id,
            is_valid=True,
            score=score,
            severity_status=severity
            ).returning(pollResults)
        result = await self.session.execute(insert_result)
        
        await self.session.commit()
        return result.scalars().first()
    
    async def getTestResult(
        self,
        user_id: Union[int,str],
    ):
        """
        Save the result of the poll
        """
        test_results=select(pollResults).where(pollResults.user_id==user_id, pollResults.is_valid==True)
        result = await self.session.execute(test_results)
        result=result.scalars().first()
        score=result.score

        return score
        
    async def getSeverityStatus(
        self,
        user_id: Union[int,str],
    ):
        """
        Save the result of the poll
        """
        test_results=select(pollResults).where(pollResults.user_id==user_id, pollResults.is_valid==True)
        result = await self.session.execute(test_results)
        result=result.scalars().first()
        severityStatus=result.severity_status

        return severityStatus
    async def deleteLastSentPolls(
        self,
        user_id: Union[int,str],
    ):
        """
        Save the result of the poll
        """
        test_results=delete(sentPoll).where(sentPoll.user_id==user_id)
        result = await self.session.execute(test_results)
        result=await self.session.commit()
        