from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.broadcaster import send_message

from ..misc.states import UserStates

from ..keyboards.inline import StandardButtonMenu

user_messages_router = Router()


@user_messages_router.message(CommandStart(),StateFilter(None,UserStates.new_user, UserStates.test_started))
async def user_start(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    # #New user starts conversation:
    # Send welcome letter
    # Send description
    # Propose to run questionaire
    
    
    replyText=await repo.standardMessages.get_standardMessages('welcome_new_1','en')
    replyButtons= await repo.standardButtons.get_standardButtons('start_test', 'en')
    replyMarkup=StandardButtonMenu(replyButtons)
    
    replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)
    

    # replyText=await repo.standardMessages.get_standardMessages('welcome_new_2','en')
    # replyButtons= await repo.standardButtons.get_standardButtons('start_test', 'en')

    # replyMarkup=StandardButtonMenu(replyButtons)
    # replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup)

    await state.set_state(UserStates.new_user)

