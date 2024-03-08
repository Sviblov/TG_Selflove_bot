import asyncio
import logging
from typing import Union, List

from aiogram import Bot

from .services import send_message
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.questions import question, answer_option
from ..misc.states import UserStates
from tgbot.keyboards.inline import mainMenuButtons, EmoDiarySetupTrue
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from infrastructure.database.models.users import User


async def send_main_menu(
    bot: Bot,
    user_id: Union[int, str],
    language: str,
    state: FSMContext,
    repo: RequestsRepo = None,
) -> bool:
   
#    1) select questiond by questionaire_id
#    2) send question by question id
    
    lang_to_use = await repo.users.supported_language(language)
    stateData = await state.get_data()
    interventionStatus= stateData['interventionsStatus']
    severity_status = await repo.results.getSeverityStatus(user_id)



    replyText = await repo.interface.get_messageText(f'main_menu_{severity_status}', lang_to_use)
    user_score = await repo.results.getTestResult(user_id)
    numberOfQuestions = await repo.questions.get_NumberOfQuestions(1,lang_to_use)
    
    formattedText = replyText.format(user_score,numberOfQuestions*4)
    MainMenuButtons = await repo.interface.get_ButtonLables('main_menu', lang_to_use)
    mainMenuMarkup = mainMenuButtons(MainMenuButtons, severity_status, interventionStatus, lang_to_use)
    
    await send_message(bot, user_id, formattedText, reply_markup=mainMenuMarkup, repo = repo)
    

async def send_completed_emodiary_menu(repo: RequestsRepo, bot: Bot, user: User, language: str, state: FSMContext, message_to_change: Message=None):
    state_data = await state.get_data()
    replyText=await repo.interface.get_messageText('emodiary_setup_true',user.language)
    numberOfnotification = state_data['interventionsStatus']['emodiary']['no_of_notifications']
    notifications = state_data['interventionsStatus']['emodiary']['notification_time']
    delta = state_data['interventionsStatus']['emodiary']['timedelta']
    notifications_formated = ', '.join(notifications)
    timezone = 'UTC '+str(delta)
    replyTextFormatted = replyText.format(numberOfnotification,notifications_formated,timezone)


    replyButtons= await repo.interface.get_ButtonLables('emodiary_setup_true', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    replyMarkup = EmoDiarySetupTrue(replyButtons+backButton)
    if message_to_change:
        await bot.edit_message_text(replyTextFormatted, message_to_change.chat.id, message_to_change.message_id, reply_markup=replyMarkup)
    else:
        await send_message(bot, user.user_id, replyTextFormatted, reply_markup=replyMarkup, repo = repo)