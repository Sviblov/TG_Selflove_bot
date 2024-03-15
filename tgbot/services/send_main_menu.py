import asyncio
import logging
from typing import Union, List

from aiogram import Bot

from .services import send_message
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.questions import question, answer_option
from ..misc.states import UserStates
from tgbot.keyboards.inline import mainMenuButtons, EmoDiarySetupTrue,ntrSetupTrue
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
    if not severity_status:
        results = await repo.results.calculateTestResult(user_id)
        numberOfQuestions = await repo.questions.get_NumberOfQuestions(1,lang_to_use)
        if results<numberOfQuestions*4*0.65:
            severity_status = 0;
        elif results<numberOfQuestions*4*0.84:
            severity_status = 1;
        else:
            severity_status = 2;

        await repo.results.saveTestResult(user_id,results, severity_status)


    replyText = await repo.interface.get_messageText(f'main_menu_{severity_status}', lang_to_use)
    user_score = await repo.results.getTestResult(user_id)
    numberOfQuestions = await repo.questions.get_NumberOfQuestions(1,lang_to_use)
    
    formattedText = replyText.format(user_score,numberOfQuestions*4)
    MainMenuButtons = await repo.interface.get_ButtonLables('main_menu', lang_to_use)
    mainMenuMarkup = mainMenuButtons(MainMenuButtons, severity_status, interventionStatus, lang_to_use)
    
    await send_message(bot, user_id, formattedText, reply_markup=mainMenuMarkup, repo = repo)
    

async def send_completed_emodiary_menu(repo: RequestsRepo, bot: Bot, user: User, state: FSMContext, message_to_change: Message=None):
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


async def send_completed_ntr_menu(repo: RequestsRepo, bot: Bot, user: User, state: FSMContext, message_to_change: Message=None):
    
    state_data = await state.get_data()
    replyText=await repo.interface.get_messageText('ntr_setup_true',user.language)
    notifications = state_data['interventionsStatus']['ntr']['notification_time']
    delta = state_data['interventionsStatus']['ntr']['timedelta']
    notifications_formated = notifications
    timezone = 'UTC '+str(delta)
    replyTextFormatted = replyText.format(notifications_formated,timezone)


    replyButtons= await repo.interface.get_ButtonLables('ntr_setup_true', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    #TODO
    replyMarkup = ntrSetupTrue(replyButtons+backButton)

    if message_to_change:
        await bot.edit_message_text(replyTextFormatted, message_to_change.chat.id, message_to_change.message_id, reply_markup=replyMarkup)
    else:
        await send_message(bot, user.user_id, replyTextFormatted, reply_markup=replyMarkup, repo = repo)