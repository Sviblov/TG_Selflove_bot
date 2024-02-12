from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.services import send_message, delete_message
from ..services.send_questionaire import sendNextQuestion, send_main_menu

from ..misc.states import UserStates

from ..keyboards.inline import StandardButtonMenu,dimeGameMarkup
from infrastructure.database.models import message as logmessage

user_callbacks_router = Router()


@user_callbacks_router.callback_query(F.data=="start_test", StateFilter(UserStates.welcome_new_user_2,UserStates.confirm_start_test))
async def start_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    if await state.get_state() == UserStates.confirm_start_test:
        # delete last test results
        await repo.results.deleteLastSentPolls(user.user_id)


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
async def send_third_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    replyText=await repo.interface.get_messageText('welcome_new_3',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_3', user.language)
    replyMarkup=StandardButtonMenu(replyButtons)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_callbacks_router.callback_query(F.data=='security')
async def send_security_description(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    replyText=await repo.interface.get_messageText('security_desc',user.language)
    replyButtons= await repo.interface.get_ButtonLables('security_desc', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)

    replyMarkup=StandardButtonMenu(replyButtons+backButton)
    
    replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_callbacks_router.callback_query(F.data=='main_menu')
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.main_menu)
    await send_main_menu(bot, user.user_id, user.language, state, repo)
    

@user_callbacks_router.callback_query(F.data=='start_test_again', StateFilter(UserStates.main_menu))
async def confirm_start_test_again(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    replyText=await repo.interface.get_messageText('start_test_again',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_3', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    replyMarkup=StandardButtonMenu(replyButtons+backButton)
    await state.set_state(UserStates.confirm_start_test)
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

#, 'psysupport', 'interventionDesc'
@user_callbacks_router.callback_query(F.data.in_({'psysupport','showvideo','interventionDesc','heros_journey'}), StateFilter(UserStates.main_menu))
async def show_one_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    if callback.data == 'showvideo':
        #send video lecture
        pass
        
    replyText=await repo.interface.get_messageText(callback.data,user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    replyMarkup = StandardButtonMenu(backButton)
    if callback.data == 'heros_journey':
        replyButtons= await repo.interface.get_ButtonLables('herojourney_completed', user.language)
        replyMarkup = StandardButtonMenu(replyButtons+backButton)

    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)


@user_callbacks_router.callback_query(F.data=='herojourney_completed', StateFilter(UserStates.main_menu))
async def show_one_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.main_menu)
    state_data = await state.get_data()
    state_data['interventionsStatus']['Herosjourney'] = True
    await state.set_data(state_data)
    await send_main_menu(bot, user.user_id, user.language, state, repo)


@user_callbacks_router.callback_query(F.data.in_({'dimegame'}), StateFilter(UserStates.main_menu))
async def start_dime_game(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    
    replyText=await repo.interface.get_messageText(callback.data,user.language)

    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    dimegameButton = await repo.interface.get_ButtonLables('start_dimegame', user.language)
    
    replyMarkup = dimeGameMarkup(dimegameButton,backButton)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)
