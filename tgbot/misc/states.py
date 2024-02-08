from aiogram.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    
    active_poll = State()
    welcome_new_user_1 = State() #new user second message
    welcome_new_user_2 = State() #
    new_user = State()
    main_menu = State()

    