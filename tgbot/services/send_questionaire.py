import asyncio
import logging
from typing import Union, List

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import Poll

from .services import send_poll
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.questions import question, answer_option
from aiogram.fsm.context import FSMContext
from ..misc.states import UserStates
from ..services.send_main_menu import send_main_menu

async def sendNextQuestion(
    bot: Bot,
    user_id: Union[int, str],
    questionaire_id: int,
    language: str,
    state: FSMContext,
    repo: RequestsRepo = None,
):
   
#    TODO: Implement sending questiona one by one
        

        if await state.get_state() == UserStates.active_poll:
            data = await state.get_data()
            polls_left = data['polls_left']
            current_question = data['current_question']
            
            if polls_left == 0:
                await state.set_state(UserStates.main_menu)
                await send_main_menu(bot, user_id, language, repo)
                await state.set_data(None)
            else:
                nextQuestion: question = await repo.questions.get_Question(questionaire_id, current_question ,language)   
                questionAnswers: List[answer_option] = await repo.questions.get_Answers(nextQuestion.question_id,language)
                answerOptionsList=[]
                for answerOptionItem in questionAnswers:
                    answerOptionsList.append(answerOptionItem.answer)
                
                result = await send_poll(bot, user_id, nextQuestion.question, answerOptionsList, repo)
                if result:
                    await repo.results.putSentQuestion(result.poll.id, result.message_id, nextQuestion.question_id, user_id)
       
                await state.set_data({
                    'polls_left': polls_left-1,
                    'current_question': current_question+1
                    })
                
            
               
            
            
                    


        
             
    

