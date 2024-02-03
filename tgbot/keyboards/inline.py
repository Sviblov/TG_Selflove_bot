from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.utils.keyboard import ButtonType

# This is a simple keyboard, that contains 2 buttons
def StandardButtonMenu(ButtonsData):

    keyboard = InlineKeyboardBuilder()
    for button in ButtonsData:
        newbutton = InlineKeyboardButton(
            text=button[0],
            callback_data=button[1]
            )
        keyboard.row(newbutton)

    return keyboard.as_markup()
