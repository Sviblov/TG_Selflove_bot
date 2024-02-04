from aiogram.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    
    test_started = State()
    welcome_new_user_2 = State() #new user second message
    new_user = State()
    main_menu = State()
    start_questionaire_first=State()
