from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter
from ..misc.states import UserStates

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User


admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message,  state: FSMContext, repo: RequestsRepo, user: User):

    
    replyText = [await repo.standardMessages.get_standardMessages('start_admin','en'), "userID:", str(message.from_user.id), user.language]

    
    
    await message.reply("\n".join(replyText))