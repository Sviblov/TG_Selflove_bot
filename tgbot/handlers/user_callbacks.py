from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.services import send_message, delete_message
from ..services.send_questionaire import sendNextQuestion

from ..misc.states import UserStates

from ..keyboards.inline import StandardButtonMenu
from infrastructure.database.models import message as logmessage

user_callbacks_router = Router()


@user_callbacks_router.callback_query(F.data=="start_test", StateFilter(UserStates.welcome_new_user_2))
async def start_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()

    await state.set_data({
        'polls_left': await repo.questions.get_NumberOfQuestions(1,'en'),
        'current_question': 1
        })

    await state.set_state(UserStates.active_poll)

    await sendNextQuestion(bot, user.user_id,1,'en',state, repo)




@user_callbacks_router.callback_query(F.data=="start_test", StateFilter(UserStates.active_poll))
async def notify_about_started_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    replyText=await repo.interface.get_messageText('active_poll','en')
    replyMessage = await send_message(bot, user.user_id, replyText, repo=repo)


@user_callbacks_router.callback_query(F.data=="delete_all")
async def delete_messages(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    allMessages = await repo.log_message.get_messages(user.user_id)
  
    for message in allMessages:
       
        await delete_message(bot, message[0],message[1])
        
    
    await repo.log_message.delete_messages(user.user_id)
    await state.set_state(None)

@user_callbacks_router.callback_query(F.data=='welcome_2', StateFilter(UserStates.welcome_new_user_1))
async def send_second_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    replyText=await repo.interface.get_messageText('welcome_new_2',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_2', user.language)
    replyMarkup=StandardButtonMenu(replyButtons)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)
    
    
    await state.set_state(UserStates.welcome_new_user_2)

@user_callbacks_router.callback_query(F.data=='welcome_3', StateFilter(UserStates.welcome_new_user_2))
async def send_second_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    replyText=await repo.interface.get_messageText('welcome_new_3',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_3', user.language)
    replyMarkup=StandardButtonMenu(replyButtons)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_callbacks_router.callback_query(F.data=='security')
async def send_second_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    replyText=await repo.interface.get_messageText('security_desc','en')
    replyButtons= await repo.interface.get_ButtonLables('security_desc', 'en')
    backButton = await repo.interface.get_ButtonLables('back_to_main', 'en')

    replyMarkup=StandardButtonMenu(replyButtons+backButton)
    
    replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)
