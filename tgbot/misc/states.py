from aiogram.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    
    active_poll = State()
    welcome_new_user_1 = State() #new user second message
    welcome_new_user_2 = State() #
    new_user = State()
    main_menu = State()
    hero_journey = State()
    confirm_start_test = State()
    set_emotion = State()
    set_emotion_what_doing = State()
    set_emotion_what_thinking = State()
    ask_feedback =State()
    set_ntr_step_1 = State()
    set_ntr_step_2 = State()


    