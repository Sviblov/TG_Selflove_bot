from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    

def StartQuestionaireMarkup():

    button1 = KeyboardButton(text = 'Тарифы')





    keyboard =[row1, row2, row3]
    markup= ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    return markup