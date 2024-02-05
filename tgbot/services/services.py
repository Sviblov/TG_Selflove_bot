import asyncio
import logging
from typing import Union, List

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import InlineKeyboardMarkup
from infrastructure.database.repo.requests import RequestsRepo

async def send_message(
    bot: Bot,
    user_id: Union[int, str],
    text: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
    repo: RequestsRepo = None,
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
        )
        if repo is not None:
            await repo.log_message.put_message(replyMessage,  user_from=bot.id, user_to=user_id)

    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request: chat not found")
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


async def broadcast(
    bot: Bot,
    users: list[Union[str, int]],
    text: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
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
        for user_id in users:
            if await send_message(
                bot, user_id, text, disable_notification, reply_markup
            ):
                count += 1
            await asyncio.sleep(
                0.05
            )  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count

async def delete_message(
    bot: Bot,
    chat_id: Union[int, str],
    message_id: Union[int,str],
   
) -> bool:

    try:
        deleteMessage = await bot.delete_message(
            chat_id,message_id
        )

    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{chat_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await delete_message(
            bot, chat_id, message_id
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{chat_id}]: failed")
    else:
        logging.info(f"Message Deleted in [ID:{chat_id}]: success")
        return True
    return False


async def send_poll(
    bot: Bot,
    user_id: Union[int, str],
    question_text: str,
    answer_options: List[str],
    repo: RequestsRepo = None,
) -> bool:

    try:
        replyQuestionaire = await bot.send_poll(user_id,question_text,answer_options,is_anonymous=False, allows_multiple_answers=False )
        replyQuestionaire.poll.id
        if repo is not None:
            await repo.log_message.put_message(replyQuestionaire,  user_from=bot.id, user_to=user_id)

    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_poll(
            bot, user_id, question_text, answer_options, repo
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Poll sent [ID:{user_id}]: success")
        return replyQuestionaire
    return False