import asyncio
import logging
from typing import Union, List

from aiogram import Bot

from .services import send_message
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.questions import question, answer_option
from ..misc.states import UserStates
from tgbot.keyboards.inline import mainMenuButtons

async def send_main_menu(
    bot: Bot,
    user_id: Union[int, str],
    language: str,
    repo: RequestsRepo = None,
) -> bool:
   
#    1) select questiond by questionaire_id
#    2) send question by question id
    replyText = await repo.interface.get_messageText('main_menu', language)
    user_score = await repo.results.getTestResult(user_id)
    numberOfQuestions = await repo.questions.get_NumberOfQuestions(1,language)
    formattedText = replyText.format(user_score,numberOfQuestions)
    MainMenuButtons = await repo.interface.get_ButtonLables('main_menu', language)
    mainMenuMarkup = mainMenuButtons(MainMenuButtons)
    
    await send_message(bot, user_id, formattedText, reply_markup=mainMenuMarkup, repo = repo)
    
    return True