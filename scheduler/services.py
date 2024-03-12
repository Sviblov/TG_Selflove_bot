import asyncio
import logging
from typing import Union, List
from datetime import time
from aiogram import Bot
from aiogram import exceptions
from aiogram.types import InlineKeyboardMarkup
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models import notification_setting


async def broadcastNotifications(
    bot: Bot,
    notifications: list[notification_setting],
    text,
    disable_notification: bool = False,
    reply_markup = None,
    repo: RequestsRepo = None,
) -> int:
    """
    Simple broadcaster.
    :param bot: Bot instance.
    :param users: List of users.
    :param text: Text of the message.
    :param disable_notification: Disable notification or not.
    :param reply_markup: Reply markup.
    :return: Count of messages.
    """
    count = 0
    try:
        for notification in notifications:
            notification_lang = notification.language
            
            valid_languages = ['en', 'ru']
            if notification_lang not in valid_languages:
                notification_lang = 'en'

            if await send_message(
                bot, notification.user_id, text[notification_lang], disable_notification, reply_markup[notification_lang], repo=repo
            ):
                count += 1
            await asyncio.sleep(
                0.05
            )  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count


async def send_message(
        bot: Bot,
        user_id: Union[int, str],
        text: str,
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
        repo: RequestsRepo = None,
        disable_web_page_preview: bool = True,
    
) -> bool:
    """
    Safe messages sender

    :param bot: Bot instance.
    :param user_id: user id. If str - must contain only digits.
    :param text: text of the message.
    :param disable_notification: disable notification or not.
    :param reply_markup: reply markup.
    :return: success.
    """
    try:
        replyMessage = await bot.send_message(
            user_id,
            text,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
            parse_mode="html",
            disable_web_page_preview=disable_web_page_preview,
     
        )
        if repo is not None:
            await repo.log_message.put_message(replyMessage,  user_from=bot.id, user_to=user_id)

    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(
            bot, user_id, text, disable_notification, reply_markup, repo
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def get_notifications_this_hour(
    repo: RequestsRepo, notification_hour: int, notification_type: str
) -> List[dict]:
    """
        Get notifications for this hour

    """

    current_hour = time(notification_hour,0,0)
    
    return await repo.interventions.getNotificationsThisHour(current_hour, notification_type)