import logging
from aiogram import Router, F

from aiogram.types import PollAnswer
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from infrastructure.database.repo.requests import RequestsRepo
from ..services.send_main_menu import send_main_menu

from aiogram import Bot

from ..misc.states import UserStates


poll_answer_router = Router()
logger = logging.getLogger('Poll_Answer')

@poll_answer_router.poll_answer()
async def register_poll_answer(poll_answer: PollAnswer, state: FSMContext, repo: RequestsRepo, bot: Bot):
    

    #check that questionaire is complete
    if poll_answer.option_ids:
        await repo.results.updatePollResult(poll_answer.poll_id, poll_answer.option_ids[0])
    else:
        await repo.results.updatePollResult(poll_answer.poll_id)
    
    numberOfUncompleted = await repo.results.getUncompletedNumber(poll_answer.user.id)

    if numberOfUncompleted==0:
        await state.set_state(UserStates.main_menu)
        #TODO calculate and poll result
        results = await repo.results.calculateTestResult(poll_answer.user.id)
        await repo.results.saveTestResult(poll_answer.user.id,results)
        #Send Main Menu

        await send_main_menu(bot, poll_answer.user.id,poll_answer.user.language_code,repo)
    
  
