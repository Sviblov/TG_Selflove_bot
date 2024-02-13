from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.services import send_message
from ..services.send_main_menu import send_main_menu    

from ..misc.states import UserStates

from ..keyboards.inline import StandardButtonMenu

user_messages_router = Router()

#to think - from which state we shour run on start
@user_messages_router.message(CommandStart(),StateFilter(None,UserStates.welcome_new_user_1))
async def user_start(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    data= {
        'interventionsStatus': {
            'emodiary': {
                'status': False
            },
        'dimegame': {
                'status':False
            },
        'Herosjourney': {
                'status':False
            },
        'Negativethoughts': {
                'status':False
            },
        }
    }
    await state.set_data(data)

    replyText=await repo.interface.get_messageText('welcome_new_1',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_1', user.language)
    replyMarkup=StandardButtonMenu(replyButtons)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)
    
    await state.set_state(UserStates.welcome_new_user_1)

@user_messages_router.message(Command('security'))
async def security_menu(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    replyText=await repo.interface.get_messageText('security_desc','en')
    replyButtons= await repo.interface.get_ButtonLables('security_desc', 'en')
    replyMarkup=StandardButtonMenu(replyButtons)
    
    replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_messages_router.message(CommandStart(),StateFilter(UserStates.active_poll))
async def user_start(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    replyText=await repo.interface.get_messageText('active_poll',user.language)
    numberToComplete= await repo.results.getUncompletedNumber(message.from_user.id)
    replyTextFormated= replyText.format(numberToComplete)

    await send_message(bot, user.user_id, replyTextFormated, repo = repo)
    
@user_messages_router.message(CommandStart(),StateFilter(UserStates.main_menu))
async def main_menu(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
 
   await send_main_menu(bot, user.user_id, user.language, state, repo)
    