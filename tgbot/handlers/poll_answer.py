import logging
from aiogram import Router, F

from aiogram.types import PollAnswer
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from infrastructure.database.repo.requests import RequestsRepo

from ..services.send_questionaire import sendNextQuestion

from aiogram import Bot

from ..misc.states import UserStates


poll_answer_router = Router()
logger = logging.getLogger('Poll_Answer')

@poll_answer_router.poll_answer()
async def register_poll_answer(poll_answer: PollAnswer, state: FSMContext, repo: RequestsRepo, bot: Bot):
    

    #check that questionaire is complete
    if poll_answer.option_ids:
        await repo.results.updatePollResult(poll_answer.poll_id, poll_answer.option_ids[0])
        await sendNextQuestion(bot, poll_answer.user.id,1,'en',state, repo)
    else:
        await repo.results.updatePollResult(poll_answer.poll_id)
    
  
