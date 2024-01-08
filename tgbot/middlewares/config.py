from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config, bot) -> None:
        self.config = config
        self.bot = bot


    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["config"] = self.config
        data["bot"] = self.bot
        
        return await handler(event, data)
