from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.utils.keyboard import ButtonType
from infrastructure.database.models import standard_button
from typing import List
from aiogram.types.web_app_info import WebAppInfo

def StandardButtonMenu(ButtonsData: List[standard_button]):

    keyboard = InlineKeyboardBuilder()
    for button in ButtonsData:
        newbutton = InlineKeyboardButton(
            text=button.button_text,
            callback_data=button.callback_data
            )
        keyboard.row(newbutton)

    return keyboard.as_markup()

def dimeGameMarkup(dimeGameButton, otherButtons):
    keyboard = InlineKeyboardBuilder()
    
    for button in dimeGameButton:
        webappUrl = button.comment
        webapp = WebAppInfo(
            url=webappUrl,

            )
        
        newbutton = InlineKeyboardButton(
            text=button.button_text,
            # callback_data=button.callback_data,
            web_app=webapp
            )
        keyboard.row(newbutton)
  
    
    for button in otherButtons:
        newbutton = InlineKeyboardButton(
            text=button.button_text,
            callback_data=button.callback_data
            )
        keyboard.row(newbutton)
    return keyboard.as_markup()


def mainMenuButtons(ButtonsData: List[standard_button], severity_status: int, interventionStatus):
    keyboard = InlineKeyboardBuilder()

    button_dict={}
    for button in ButtonsData:

        button_as_dict = button.as_keyboard()

        button_dict.update(button_as_dict)

    for key, value in interventionStatus.items():
        if value['status']:
            button_dict[key].text= button_dict[key].text+'🟢'
        else:
            button_dict[key].text= button_dict[key].text+'🔴'
    

    if severity_status >0:

        keyboard.row(
            button_dict['emodiary'] ,button_dict['video']
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