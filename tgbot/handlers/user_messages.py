from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,ForceReply
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.services import send_message
from ..services.send_main_menu import send_main_menu    

from ..misc.states import UserStates

from ..keyboards.inline import StandardButtonMenu

user_messages_router = Router()

#to think - from which state we shour run on start
@user_messages_router.message(CommandStart(),StateFilter(None,UserStates.welcome_new_user_1))
async def user_start(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    data= {
        'interventionsStatus': {
            'emodiary': {
                'status': False
            },
        'dimegame': {
                'status':False
            },
        'Herosjourney': {
                'status':False
            },
        'ntr': {
                'status':False
            },
        }
    }
    await state.set_data(data)

    replyText=await repo.interface.get_messageText('welcome_new_1',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_1', user.language)
    replyMarkup=StandardButtonMenu(replyButtons)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)
    
    await state.set_state(UserStates.welcome_new_user_1)

@user_messages_router.message(Command('security'))
async def security_menu(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    replyText=await repo.interface.get_messageText('security_desc','en')
    replyButtons= await repo.interface.get_ButtonLables('security_desc', 'en')
    replyMarkup=StandardButtonMenu(replyButtons)
    
    replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_messages_router.message(CommandStart(),StateFilter(UserStates.active_poll))
async def user_start(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
    replyText=await repo.interface.get_messageText('active_poll',user.language)
    numberToComplete= await repo.results.getUncompletedNumber(message.from_user.id)
    replyTextFormated= replyText.format(numberToComplete)

    await send_message(bot, user.user_id, replyTextFormated, repo = repo)
    
@user_messages_router.message(CommandStart(),StateFilter(UserStates.main_menu, 
                                                         UserStates.set_emotion,
                                                         UserStates.set_emotion_what_doing,
                                                         UserStates.set_emotion_what_thinking,
                                                         UserStates.set_ntr_step_1,
                                                         UserStates.set_ntr_step_1))
async def main_menu(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    
 
   await send_main_menu(bot, user.user_id, user.language, state, repo)
    
@user_messages_router.message(StateFilter(UserStates.set_emotion_what_doing))
async def set_emotion_what_doing(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
        current_data = await state.get_data()
        current_data['set_emotion']['what_doing'] = message.text
        await state.set_data(current_data)

        await state.set_state(UserStates.set_emotion_what_thinking)
        replyText=await repo.interface.get_messageText('emodiary_add_emotion_3',user.language)
        await send_message(bot, user.user_id, replyText,reply_markup=ForceReply() ,  repo = repo)

@user_messages_router.message(StateFilter(UserStates.set_emotion_what_thinking))
async def set_emotion_what_thinking(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
        current_data = await state.get_data()
        
        emotion = current_data['set_emotion']['emotion']
        await repo.interventions.putEmotion(message.from_user.id,message.chat.id, current_data['set_emotion']['emotion'], message.text, current_data['set_emotion']['what_doing'])
        
        current_data['set_emotion'] = None
        await state.set_data(current_data)
        await state.set_state(UserStates.main_menu)
        
        await send_main_menu(bot, user.user_id, user.language, state, repo)


@user_messages_router.message(StateFilter(UserStates.ask_feedback))
async def set_emotion_what_thinking(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
       
        
        await state.set_state(UserStates.main_menu)
   
        if message.content_type == 'text':
            await send_message(bot, 173409214, f'Feedback from {user.username} {user.full_name}: {message.text}', repo = repo)
            # await send_message(bot, '6808009045', f'Feedback from {user.username }: {message.text}', repo = repo)
            await send_message(bot, user.user_id, 'Thank you for your feedback', repo = repo)
            await repo.interface.putFeedback(message, user.user_id)
            await send_main_menu(bot, user.user_id, user.language, state, repo)
        else:
            replyText = repo.interface.get_messageText('not_text_feedback', user.language)
            await send_message(bot, user.user_id, replyText, repo = repo)


@user_messages_router.message(StateFilter(UserStates.set_ntr_step_1))
async def set_emotion_what_doing(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
        current_data = await state.get_data()
        current_data['set_ntr']['negative_thought'] = message.text
        await state.set_data(current_data)

        await state.set_state(UserStates.set_ntr_step_2)
        replyText=await repo.interface.get_messageText('ntr_add_record_2 ',user.language)
        await send_message(bot, user.user_id, replyText,reply_markup=ForceReply(),  repo = repo)


@user_messages_router.message(StateFilter(UserStates.set_ntr_step_2))
async def set_emotion_what_doing(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
        current_data = await state.get_data()
       
        
        await repo.interventions.putNegativeThought(message.from_user.id,message.chat.id, current_data['set_ntr']['negative_thought'], message.text)
        current_data['set_ntr'] = None
        await state.set_data(current_data)
        await state.set_state(UserStates.main_menu)
        await send_main_menu(bot, user.user_id, user.language, state, repo)


@user_messages_router.message(Command('language'))
async def security_menu(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    replyText=await repo.interface.get_messageText('choose_language','en')
    replyButtons= await repo.interface.get_ButtonLables('choose_language', 'en')
    replyMarkup=StandardButtonMenu(replyButtons)
    
    replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)


@user_messages_router.message(Command('hotline'))
async def hotline_menu(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    replyText=await repo.interface.get_messageText('hotline','en')
    currentState = await state.get_state()
    if currentState == UserStates.main_menu:
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        replyMarkup=StandardButtonMenu(backButton)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_messages_router.message(Command('feedback'))
async def hotline_menu(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await state.set_state(UserStates.ask_feedback)
    replyText=await repo.interface.get_messageText('feedback',user.language)
    replyMarkup = ForceReply()
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)