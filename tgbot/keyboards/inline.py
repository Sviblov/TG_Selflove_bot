from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.utils.keyboard import ButtonType
from infrastructure.database.models import standard_button
from typing import List


def StandardButtonMenu(ButtonsData: List[standard_button]):

    keyboard = InlineKeyboardBuilder()
    for button in ButtonsData:
        newbutton = InlineKeyboardButton(
            text=button.button_text,
            callback_data=button.callback_data
            )
        keyboard.row(newbutton)

    return keyboard.as_markup()


def mainMenuButtons(ButtonsData: List[standard_button], severity_status: int):
    keyboard = InlineKeyboardBuilder()

    button_dict={}
    for button in ButtonsData:
        button_as_dict = button.as_keyboard()
   
        button_dict.update(button_as_dict)
    if severity_status >0:

        keyboard.row(
            button_dict['emodiary'],button_dict['video']
        )
        keyboard.row(
            button_dict['dimegame'],button_dict['psysupport']
        )
        keyboard.row(
            button_dict['Herosjourney'],button_dict['interventionDesc']
        )
        keyboard.row(
            button_dict['Negativethoughts'],button_dict['start_test']
        )
        keyboard.row(
            button_dict['security']
        )
    else:
        keyboard.row(
            button_dict['video']
        )
        keyboard.row(
            button_dict['psysupport']
        )
        keyboard.row(
            button_dict['interventionDesc']
        )
        keyboard.row(
            button_dict['start_test']
        )
        keyboard.row(
            button_dict['security']
        )


    return keyboard.as_markup()