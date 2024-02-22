import logging
from aiogram import Router, F

from aiogram.types import PollAnswer
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from infrastructure.database.repo.requests import RequestsRepo
from aiogram.types import Message
from ..services.send_questionaire import sendNextQuestion

from aiogram import Bot

from ..misc.states import UserStates

webapp_router = Router()

    
@webapp_router.message()
async def get_data(message: Message):
    
    print(message.web_app_data)