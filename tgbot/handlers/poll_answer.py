import logging
from aiogram import Router, F

from aiogram.types import PollAnswer
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from ..misc.states import UserStates
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User



poll_answer_router = Router()
logger = logging.getLogger('Poll_Answer')

@poll_answer_router.poll_answer(StateFilter(UserStates.active_poll))
async def register_poll_answer(poll_answer: PollAnswer):
    #test
    print(poll_answer.option_ids, poll_answer.poll_id)


    
  
