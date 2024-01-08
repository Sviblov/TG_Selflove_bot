from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.broadcaster import send_message

from ..misc.states import UserStates

from ..keyboards.inline import StandardButtonMenu

user_callbacks_router = Router()


@user_callbacks_router.callback_query(F.data=="start_test", StateFilter(UserStates.new_user))
async def start_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    replyText='Тут присылаются вопросы к тесту'
    replyMessage = await send_message(bot, user.user_id, replyText)
    replyMessage = await send_message(bot, user.user_id, replyText)
    await state.set_state(UserStates.test_started)

@user_callbacks_router.callback_query(F.data=="description", StateFilter(UserStates.new_user))
async def start_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    replyText=await repo.standardMessages.get_standardMessages('detailed_description','en')
    replyButtons= await repo.standardButtons.get_standardButtons('start_test_desc', 'en')

    replyMarkup=StandardButtonMenu(replyButtons)
    replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup)