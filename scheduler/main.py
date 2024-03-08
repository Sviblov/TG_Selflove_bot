import os
import sys
import aiohttp
from typing import Optional
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

import asyncio
import logging

import betterlogging as bl
from aiogram import Bot
 
from infrastructure.database.repo.requests import RequestsRepo
from services import broadcast



from infrastructure.database.setup import create_engine
from infrastructure.database.setup import create_session_pool

from tgbot.config import load_config


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcast(bot, admin_ids, "testing")

    

def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def get_session(self) -> Optional[aiohttp.ClientSession]: 
     if self._session is None or self._session.closed: 
         self._session = await self.get_new_session() 
  
     if not self._session._loop.is_running():  # NOQA 
         # Hate `aiohttp` devs because it juggles event-loops and breaks already opened session 
         # So... when we detect a broken session need to fix it by re-creating it 
         # @asvetlov, if you read this, please no more juggle event-loop inside aiohttp, it breaks the brain. 
         await self._session.close() 
         self._session = await self.get_new_session() 
  
     return self._session   

async def main():
    setup_logging()



    config = load_config(parent_dir+"/.env")


    db_engine=create_engine(config.db)
    session_pool=create_session_pool(db_engine)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    logging.info("Starting scheduler")

    async with session_pool() as session:
        repo = RequestsRepo(session)
        
    
    logging.info(f"Bot Token: {config.tg_bot.token}")
    async with bot.session: 
        await bot.send_message('5516377862','testing')
  
    
    # await on_startup(bot, config.tg_bot.admin_ids)
    logging.info("Scheduler ended")
    
    


if __name__ == "__main__":
    try:
        asyncio.run(main())
        
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен")
