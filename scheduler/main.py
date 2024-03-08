import os
import sys
import aiohttp
import schedule
import time
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
import services



from infrastructure.database.setup import create_engine
from infrastructure.database.setup import create_session_pool

from tgbot.config import load_config




    

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
    logger.info("Starting scheduler")


async def main():
    



    config = load_config(parent_dir+"/.env")


    db_engine=create_engine(config.db)
    session_pool=create_session_pool(db_engine)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    logging.info("Starting scheduler")
    current_hour=time.localtime().tm_hour

    
    
    async with session_pool() as session:
        repo = RequestsRepo(session)
        emoDiaryNotificationUsers = await services.get_notifications_this_hour(repo, current_hour, "emodiary")
        
    async with bot.session: 
        await services.broadcast(bot,emoDiaryNotificationUsers,f'Current Time: {time.localtime().tm_hour}:{time.localtime().tm_min}')
  
    
    # await on_startup(bot, config.tg_bot.admin_ids)
    logging.info("Scheduler ended")
    

    


if __name__ == "__main__":
    try:
        def scheduler_job():
            asyncio.run(main())
        
        setup_logging()
      
        schedule.every(1).hour.at(":00").do(scheduler_job)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен")
