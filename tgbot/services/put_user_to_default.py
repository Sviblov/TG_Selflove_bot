from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, ForceReply
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
import logging
import os
from datetime import datetime, time

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.services import send_message, delete_message
from ..services.send_questionaire import sendNextQuestion, send_main_menu

from ..misc.states import UserStates

from ..misc.emodiary_report import generatePDFReport
from aiogram.types import BufferedInputFile

from ..keyboards.inline import StandardButtonMenu,dimeGameMarkup,EmoDiarySetupTrue, ntrSetupTrue, EmoDiarySetupMarkup,EmoDiarySetupMarkup, getEmotionList
from infrastructure.database.models import message as logmessage



async def putUserToDefault(user, repo, bot, state: FSMContext):
    #deleting messages
    allMessages = await repo.log_message.get_messages(user.user_id)
    
    for message in allMessages:
        await delete_message(bot, message[0],message[1])
        
    #deleting from logs
    await repo.log_message.delete_messages(user.user_id)

    #clearing state
    data= {
        'interventionsStatus': {
            'emodiary': {
                'status':False
            },
            'dimegame': {
                'status':False
            },
            'Herosjourney': {
                'status':False
            },
            'ntr': {
                'status':False
            },
        }
    }
    
    await state.set_data(data)

    await state.set_state(None)

    #deleting emotions and notifications
    await repo.users.deleteUser(user.user_id)
    # await repo.interventions.deleteAllEmotions(user.user_id)
    # await repo.interventions.deleteNotificationTime(user.user_id)
    # await repo.results.deleteLastSentPolls(user.user_id)