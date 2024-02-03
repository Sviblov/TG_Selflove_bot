import asyncio
import logging
from typing import Union

from aiogram import Bot
from aiogram import exceptions

from infrastructure.database.repo.requests import RequestsRepo

async def send_questionaire(
    bot: Bot,
    user_id: Union[int, str],
    questionaire_id: int,
    landuage: str,
    repo: RequestsRepo = None,
) -> bool:
   
#    1) select questiond by questionaire_id
#    2) send question by question id


   return True

async def send_question(
    bot: Bot,
    user_id: Union[int, str],
    question_id: int,
    landuage: str,
    repo: RequestsRepo = None,
) -> bool:
   
#    1) select answers by question id
#    2) save send of questions_id
   
       
   return True