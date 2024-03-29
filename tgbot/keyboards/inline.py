from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.utils.keyboard import ButtonType
from infrastructure.database.models import standard_button
from typing import List
from aiogram.types.web_app_info import WebAppInfo
from datetime import datetime,timedelta

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


def mainMenuButtons(ButtonsData: List[standard_button], severity_status: int, interventionStatus, lang_to_use:str):

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
            button_dict['ntr'],button_dict['start_test']
        )
        # if lang_to_use == 'en':
        #     keyboard.row(
        #         button_dict['hotline'],button_dict['feedback']
        #     )
            
        # keyboard.row(
        #     button_dict['security']
        # )

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
        # keyboard.row(
        #     button_dict['security']
        # )
        # if lang_to_use == 'en':
        #     keyboard.row(
        #         button_dict['hotline']
        #     )
        #     keyboard.row(
        #         button_dict['feedback']
        #     )


    return keyboard.as_markup()


def EmoDiarySetupMarkup(ButtonsData: List[standard_button], back_button: standard_button, step: int, delta: int=None):
    keyboard = InlineKeyboardBuilder()
    if step == 1:
       for button in ButtonsData:
            
            newbutton = InlineKeyboardButton(
                text=button.button_text,
                callback_data=button.callback_data
                )
            if button.callback_data == 'emodiary_notif_0':
                keyboard.row(newbutton)
            else:
                keyboard.add(newbutton)
    elif step == 2:

        for button in ButtonsData:
            text=button.button_text,
            callback_data=button.callback_data
            text=text[0]
            current_time = datetime.now()

            for i in range(-12,12):
                adjusted_time = current_time + timedelta(hours=i)
                adjusted_time_text = adjusted_time.strftime('%H:%M')
                if(i>=0):
                    
                    newbutton = InlineKeyboardButton(
                        text=text.format(adjusted_time_text,'+'+str(i)),
                        callback_data=callback_data.format(i)
                        )
                else:
                    newbutton = InlineKeyboardButton(
                        text=text.format(adjusted_time_text,i),
                        callback_data=callback_data.format(i)
                        )
                if i%2==0:
                    keyboard.row(newbutton)
                else:
                    keyboard.add(newbutton)

    else:
        for button in ButtonsData:
            text=button.button_text,
            callback_data=button.callback_data
            text=text[0]
            for i in range(0,24):
                adjusted_time = str(i)+':00'
                
                newbutton = InlineKeyboardButton(
                        text=adjusted_time,
                        callback_data=callback_data.format(delta,adjusted_time)
                        )
                if i%3==0:
                    keyboard.row(newbutton)
                else:
                    keyboard.add(newbutton)


    for button in back_button:
        newbutton = InlineKeyboardButton(
            text=button.button_text,
            callback_data=button.callback_data
            )
        keyboard.row(newbutton)

    return keyboard.as_markup()


def EmoDiarySetupTrue(ButtonsData: List[standard_button]):
    keyboard = InlineKeyboardBuilder()

    
    for button in ButtonsData:
        if button.key =='emodiary_add_emotion':
            # webappUrl = button.comment
            # webapp = WebAppInfo(
            # url=webappUrl,
            # )
            # newbutton = InlineKeyboardButton(
            #     text=button.button_text,
            #     web_app=webapp
            #     )
            newbutton = InlineKeyboardButton(
                text=button.button_text,
                callback_data=button.callback_data
            )
        else:
            newbutton = InlineKeyboardButton(
                text=button.button_text,
                callback_data=button.callback_data
            )
        
        keyboard.row(newbutton)
    return keyboard.as_markup()


def ntrSetupTrue(ButtonsData: List[standard_button]):
    keyboard = InlineKeyboardBuilder()

    
    for button in ButtonsData:
        if button.key =='ntr_add_record':
            # webappUrl = button.comment
            # webapp = WebAppInfo(
            # url=webappUrl,
            # )

            # newbutton = InlineKeyboardButton(
            #     text=button.button_text,
            #     web_app=webapp,
            #     callback_data='testwebapp'
            #     )
            newbutton = InlineKeyboardButton(
                text=button.button_text,
                callback_data=button.callback_data
            )
            
        
        else:
            newbutton = InlineKeyboardButton(
                text=button.button_text,
                callback_data=button.callback_data
            )
        
        keyboard.row(newbutton)
    return keyboard.as_markup()


def getEmotionList(ButtonsData: List[standard_button], backButton: standard_button):
    keyboard = InlineKeyboardBuilder()

    
    for button1, button2 in zip(ButtonsData[::2], ButtonsData[1::2]):
        newbutton1 = InlineKeyboardButton(
            text=button1.button_text,
            callback_data=button1.callback_data
        )
        newbutton2 = InlineKeyboardButton(
            text=button2.button_text,
            callback_data=button2.callback_data
        )
        
        keyboard.row(newbutton1, newbutton2)

    for button in backButton:
        newbutton = InlineKeyboardButton(
            text=button.button_text,
            callback_data=button.callback_data
            )
        keyboard.row(newbutton)

    return keyboard.as_markup()

