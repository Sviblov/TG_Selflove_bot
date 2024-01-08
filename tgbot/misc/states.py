from aiogram.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    new_user = State() #New user didn't start the test, only welcome message received
    test_started = State()
    state3 = State()