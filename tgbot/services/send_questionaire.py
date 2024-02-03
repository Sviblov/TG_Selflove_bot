import asyncio
import logging
from typing import Union, List

from aiogram import Bot
from aiogram import exceptions

from .services import send_poll
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.questions import question, answer_option

async def send_questionaire(
    bot: Bot,
    user_id: Union[int, str],
    questionaire_id: int,
    language: str,
    repo: RequestsRepo = None,
) -> bool:
   
#    1) select questiond by questionaire_id
#    2) send question by question id

    questionList: List[question] = await repo.questions.get_Questions(questionaire_id,language)

    for questionItem in questionList:
        questionAnswers: List[answer_option] = await repo.questions.get_Answers(questionItem.question_id,language)
        answerOptionsList=[]
        for answerOptionItem in questionAnswers:
            answerOptionsList.append(answerOptionItem.answer)

        question = await send_poll(bot,user_id,questionItem.question,answerOptionsList, repo)
        
        


    return True

