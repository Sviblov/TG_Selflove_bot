from typing import Callable, Dict, Any, Awaitable 
from aiogram.client.session.middlewares.base import NextRequestMiddlewareType
from aiogram.client.session.middlewares.base import BaseRequestMiddleware

from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo


class LoggingMiddleware(BaseMiddleware):
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

            await repo.log_message.put_message(event, user_to=self.bot.id, user_from=event.from_user.id)
            result = await handler(event, data)
    
        return result

# class OutcomingLoggingMiddleware(BaseRequestMiddleware):
#     def __init__(self, session_pool, include_methods = None) -> None:
#         self.session_pool = session_pool
#         self.include_methods = include_methods if include_methods else []

#     async def __call__(
#         self,
#         make_request: NextRequestMiddlewareType[TelegramType],
#         bot: Bot,
#         method: TelegramMethod[TelegramType]
#     ) -> TelegramType:
        
#         if type(method) in self.include_methods:
#             print(method.text)
        
#         return await make_request(bot, method)