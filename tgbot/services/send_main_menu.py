import asyncio
import logging
from typing import Union, List

from aiogram import Bot

from .services import send_message
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.questions import question, answer_option
from ..misc.states import UserStates
from tgbot.keyboards.inline import mainMenuButtons
from aiogram.fsm.context import FSMContext

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
    mainMenuMarkup = mainMenuButtons(MainMenuButtons, severity_status, interventionStatus)
    
    await send_message(bot, user_id, formattedText, reply_markup=mainMenuMarkup, repo = repo)
    
