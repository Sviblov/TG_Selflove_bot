from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from infrastructure.database.repo.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool, bot) -> None:
        self.session_pool = session_pool
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        
        async with self.session_pool() as session:
            repo = RequestsRepo(session)
           
            if type(event) in (Message, CallbackQuery):
                user = await repo.users.get_or_create_user(
                    event.from_user.id,
                    event.from_user.full_name,
                    event.from_user.language_code,
                    event.from_user.username
                )
                data["user"] = user
            
            #data["session"] = session
            data["repo"] = repo
            

            result = await handler(event, data)



        return result
