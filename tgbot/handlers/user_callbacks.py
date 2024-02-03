from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.services import send_message, delete_message
from ..services.send_questionaire import send_questionaire

from ..misc.states import UserStates

from ..keyboards.inline import StandardButtonMenu
from infrastructure.database.models import message as logmessage

user_callbacks_router = Router()


@user_callbacks_router.callback_query(F.data=="start_test", StateFilter(UserStates.new_user))
async def start_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    # 1) выбираются вопросы 
    #   для каждого вопроса выбираются ответы
    # отправляется опросник
    # repo.getQuestions
    # Send questionaire by 

    await send_questionaire(bot, user.user_id,1,'en',repo)

    await state.set_state(UserStates.test_started)

@user_callbacks_router.callback_query(F.data=="start_test", StateFilter(UserStates.test_started))
async def notify_about_started_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    replyText=await repo.standardMessages.get_standardMessages('test_already_started','en')
    replyMessage = await send_message(bot, user.user_id, replyText, repo=repo)


@user_callbacks_router.callback_query(F.data=="delete_all")
async def delete_messages(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    allMessages = await repo.log_message.get_messages(user.user_id)
  
    for message in allMessages:
       
        await delete_message(bot, message[0],message[1])
    
    await state.set_state(None)