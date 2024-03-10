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
from tgbot.keyboards.inline import StandardButtonMenu



    

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
    logger.info("Starting scheduler process")


async def main():
    



    config = load_config(parent_dir+"/.env")


    db_engine=create_engine(config.db)
    session_pool=create_session_pool(db_engine)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    logging.info("Starting scheduler")
    current_hour=time.localtime().tm_hour

    
    
    async with session_pool() as session:
        repo = RequestsRepo(session)
        emoDiaryNotifications = await services.get_notifications_this_hour(repo, current_hour, "emodiary")
        emotionNotificationText = await repo.interface.get_messageTextNotification('emotionNotification')
        emotionNotificationButtons = await repo.interface.get_ButtonLablesNotification('emotionNotification')
        
        emotionNotificationMarkup = {
            'en': StandardButtonMenu(emotionNotificationButtons['en']),
            'ru': StandardButtonMenu(emotionNotificationButtons['ru'])
        }

        ntrNotifications = await services.get_notifications_this_hour(repo, current_hour, "ntr")
        ntrNotificationText = await repo.interface.get_messageTextNotification('ntrNotification')
        ntrNotificationButtons = await repo.interface.get_ButtonLablesNotification('ntrNotification')
        ntrNotificationMarkup = {
            'en': StandardButtonMenu(ntrNotificationButtons['en']),
            'ru': StandardButtonMenu(ntrNotificationButtons['ru'])
        }
        async with bot.session: 
            countEmotionNotifications = await services.broadcastNotifications(bot,emoDiaryNotifications,emotionNotificationText, reply_markup=emotionNotificationMarkup, repo=repo)
            countNTFNotifications = await services.broadcastNotifications(bot,ntrNotifications,ntrNotificationText, reply_markup=ntrNotificationMarkup, repo=repo)


            
    logging.info(f"Regular notifications were sent. NO of emotion notifications: {countEmotionNotifications}. NO of NTR notifications: {countNTFNotifications}")
    

    


if __name__ == "__main__":
    try:

        setup_logging()

        def scheduler_job():
            asyncio.run(main())
        
      
      
        schedule.every(1).hour.at(":00").do(scheduler_job)

        
        

        while True:
            schedule.run_pending()
            time.sleep(1)

        # asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен")
