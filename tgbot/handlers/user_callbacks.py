from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.services import send_message, delete_message
from ..services.send_questionaire import sendNextQuestion, send_main_menu

from ..misc.states import UserStates

from ..keyboards.inline import StandardButtonMenu,dimeGameMarkup,EmoDiarySetupTrue, EmoDiarySetupMarkup,EmoDiarySetupMarkup
from infrastructure.database.models import message as logmessage

user_callbacks_router = Router()


@user_callbacks_router.callback_query(F.data=="start_test", StateFilter(UserStates.welcome_new_user_2,UserStates.confirm_start_test))
async def start_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    if await state.get_state() == UserStates.confirm_start_test:
        # delete last test results
        await repo.results.deleteLastSentPolls(user.user_id)

    state_data = await state.get_data()
    state_data['polls_left']=await repo.questions.get_NumberOfQuestions(1,'en')
    state_data['current_question']=1
  
    await state.set_data(state_data)
    await state.set_state(UserStates.active_poll)

    await sendNextQuestion(bot, user.user_id,1,'en',state, repo)




@user_callbacks_router.callback_query(F.data=="start_test", StateFilter(UserStates.active_poll))
async def notify_about_started_test(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    replyText=await repo.interface.get_messageText('active_poll','en')
    replyMessage = await send_message(bot, user.user_id, replyText, repo=repo)


@user_callbacks_router.callback_query(F.data=="delete_all")
async def delete_messages(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    allMessages = await repo.log_message.get_messages(user.user_id)
    
    for message in allMessages:
       
        await delete_message(bot, message[0],message[1])
        
    
    await repo.log_message.delete_messages(user.user_id)

    data= {
        'interventionsStatus': {
            'emodiary': {
                'status':False
            },
        'dimegame': {
                'status':False
            },
        'Herosjourney': {
                'status':False
            },
        'Negativethoughts': {
                'status':False
            },
        }
    }
    await state.set_data(data)

    await state.set_state(None)

@user_callbacks_router.callback_query(F.data=='welcome_2', StateFilter(UserStates.welcome_new_user_1))
async def send_second_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    replyText=await repo.interface.get_messageText('welcome_new_2',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_2', user.language)
    replyMarkup=StandardButtonMenu(replyButtons)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)
    
    
    await state.set_state(UserStates.welcome_new_user_2)

@user_callbacks_router.callback_query(F.data=='welcome_3', StateFilter(UserStates.welcome_new_user_2))
async def send_third_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    replyText=await repo.interface.get_messageText('welcome_new_3',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_3', user.language)
    replyMarkup=StandardButtonMenu(replyButtons)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_callbacks_router.callback_query(F.data=='security')
async def send_security_description(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    replyText=await repo.interface.get_messageText('security_desc',user.language)
    replyButtons= await repo.interface.get_ButtonLables('security_desc', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)

    replyMarkup=StandardButtonMenu(replyButtons+backButton)
    
    replyMessage = await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_callbacks_router.callback_query(F.data=='main_menu')
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.main_menu)
    await send_main_menu(bot, user.user_id, user.language, state, repo)
    

@user_callbacks_router.callback_query(F.data=='start_test_again', StateFilter(UserStates.main_menu))
async def confirm_start_test_again(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    replyText=await repo.interface.get_messageText('start_test_again',user.language)
    replyButtons= await repo.interface.get_ButtonLables('welcome_new_3', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    replyMarkup=StandardButtonMenu(replyButtons+backButton)
    await state.set_state(UserStates.confirm_start_test)
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)


@user_callbacks_router.callback_query(F.data.in_({'psysupport','showvideo','interventionDesc','heros_journey'}), StateFilter(UserStates.main_menu))
async def show_one_message(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    if callback.data == 'showvideo':
        videoLink=await repo.interface.get_messageText('video_link',user.language)
        await send_message(bot, user.user_id, videoLink, repo = repo,disable_web_page_preview=False)
        
    replyText=await repo.interface.get_messageText(callback.data,user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    replyMarkup = StandardButtonMenu(backButton)
    if callback.data == 'heros_journey':
        replyButtons= await repo.interface.get_ButtonLables('herojourney_completed', user.language)
        replyMarkup = StandardButtonMenu(replyButtons+backButton)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)


@user_callbacks_router.callback_query(F.data=='herojourney_completed', StateFilter(UserStates.main_menu))
async def show_herojourney_completed(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.main_menu)
    state_data = await state.get_data()
    state_data['interventionsStatus']['Herosjourney']['status'] = True
    await state.set_data(state_data)
    await send_main_menu(bot, user.user_id, user.language, state, repo)


@user_callbacks_router.callback_query(F.data.in_({'dimegame_completed'}), StateFilter(UserStates.main_menu))
async def dime_game_completed(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.main_menu)
    state_data = await state.get_data()
    state_data['interventionsStatus']['dimegame']['status'] = True
    await state.set_data(state_data)
    await send_main_menu(bot, user.user_id, user.language, state, repo)
   
    
    

@user_callbacks_router.callback_query(F.data.in_({'dimegame'}), StateFilter(UserStates.main_menu))
async def start_dime_game(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()

    
    replyText=await repo.interface.get_messageText(callback.data,user.language)
    replyButtons= await repo.interface.get_ButtonLables('dimegame_completed', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    dimegameButton = await repo.interface.get_ButtonLables('start_dimegame', user.language)
    
    replyMarkup = dimeGameMarkup(dimegameButton,replyButtons+backButton)
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)


@user_callbacks_router.callback_query(F.data.in_({'emodiary'}), StateFilter(UserStates.main_menu))
async def show_emodiary(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    

    state_data = await state.get_data()
    emoDiaryStatus = state_data['interventionsStatus']['emodiary']['status']

    if emoDiaryStatus:
        replyText=await repo.interface.get_messageText('emodiary_setup_true',user.language)
        numberOfnotification = state_data['interventionsStatus']['emodiary']['no_of_notifications']
        notifications = state_data['interventionsStatus']['emodiary']['notification_time']
        delta = state_data['interventionsStatus']['emodiary']['timedelta']
        notifications_formated = ', '.join(notifications)
        timezone = 'UTC '+str(delta)
        replyTextFormatted = replyText.format(numberOfnotification,notifications_formated,timezone)


        replyButtons= await repo.interface.get_ButtonLables('emodiary_setup_true', user.language)
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        replyMarkup = EmoDiarySetupTrue(replyButtons+backButton)
        await send_message(bot, user.user_id, replyTextFormatted, reply_markup=replyMarkup, repo = repo)

    else:
        replyText=await repo.interface.get_messageText('emodiary_setup_false',user.language)
        replyButtons= await repo.interface.get_ButtonLables('emodiary_setup_false', user.language)
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        replyMarkup = StandardButtonMenu(replyButtons+backButton)
        await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

@user_callbacks_router.callback_query(F.data=='emodiary_setup_step_1', StateFilter(UserStates.main_menu))
async def show_emodiary_setup(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()


    replyButtons= await repo.interface.get_ButtonLables(callback.data, user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    replyMarkup = EmoDiarySetupMarkup(replyButtons,backButton,1)
    replyText=await repo.interface.get_messageText(callback.data,user.language)
  

    await callback.message.edit_text(replyText, reply_markup=replyMarkup) 

@user_callbacks_router.callback_query(F.data.contains('emodiary_notif'), StateFilter(UserStates.main_menu))
async def show_emodiary_setup_step_1(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()

    numberOfNotification = int(callback.data[-1])

    replyButtons = await repo.interface.get_ButtonLables('emodiary_setup_step_2', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    replyMarkup = EmoDiarySetupMarkup(replyButtons,backButton,2)
    replyText = await repo.interface.get_messageText('emodiary_setup_step_2',user.language)
    
    stateData = await state.get_data()
    stateData['interventionsStatus']['emodiary']['no_of_notifications'] = numberOfNotification
    
    stateData['interventionsStatus']['emodiary']['notification_time'] = []

    await state.set_data(stateData)

    await callback.message.edit_text(replyText, reply_markup=replyMarkup)
    
@user_callbacks_router.callback_query(F.data.contains('emoutc_'), StateFilter(UserStates.main_menu))
async def show_emodiary_setup_step_2(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()

    stateData = await state.get_data()
    delta = int(callback.data.split('_')[1])
    stateData['interventionsStatus']['emodiary']['timedelta'] = delta

    if len(callback.data.split('_'))==2:
        
        pass
        
        
    else:
      
        selected_time = callback.data.split('_')[2]
        notifications = stateData['interventionsStatus']['emodiary']['notification_time']
        notifications.append(selected_time)
        stateData['interventionsStatus']['emodiary']['notification_time'] = notifications

        await state.set_data(stateData)
        

    notifications = stateData['interventionsStatus']['emodiary']['notification_time']
    numberOfnotification = stateData['interventionsStatus']['emodiary']['no_of_notifications']

    if len(notifications)==numberOfnotification:
        stateData['interventionsStatus']['emodiary']['status'] = True
        await state.set_data(stateData)
        await send_main_menu(bot, user.user_id, user.language, state, repo)
    else:
        replyButtons = await repo.interface.get_ButtonLables('emodiary_setup_step_3', user.language)
        replyText = await repo.interface.get_messageText('emodiary_setup_step_3',user.language)
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        replyMarkup = EmoDiarySetupMarkup(replyButtons,backButton,3, delta)
    
        replyTextFormatted= replyText.format(numberOfnotification,len(notifications)+1)
        await callback.message.edit_text(replyTextFormatted, reply_markup=replyMarkup)



@user_callbacks_router.callback_query(F.data.in_({'ntr_menu'}), StateFilter(UserStates.main_menu))
async def show_ntrdiary(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    

    state_data = await state.get_data()
    ntrStatus = state_data['interventionsStatus']['NTR']['status']

    if ntrStatus:
        replyText=await repo.interface.get_messageText('ntr_setup_true',user.language)
        notifications = state_data['interventionsStatus']['NTR']['notification_time']
        delta = state_data['interventionsStatus']['NTR']['timedelta']
        notifications_formated = notifications
        timezone = 'UTC '+str(delta)
        replyTextFormatted = replyText.format(notifications_formated,timezone)


        replyButtons= await repo.interface.get_ButtonLables('NTR_setup_true', user.language)
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        #TODO
        replyMarkup = EmoDiarySetupTrue(replyButtons+backButton)
        await send_message(bot, user.user_id, replyTextFormatted, reply_markup=replyMarkup, repo = repo)

    else:

        replyText=await repo.interface.get_messageText('NTR_setup_false',user.language)
        replyButtons= await repo.interface.get_ButtonLables('NTR_setup_false', user.language)
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        replyMarkup = StandardButtonMenu(replyButtons+backButton)
        await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)



@user_callbacks_router.callback_query(F.data=='ntr_setup_step_1', StateFilter(UserStates.main_menu))
async def show_ntr_setup(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()

    replyButtons = await repo.interface.get_ButtonLables('NTR_setup_step_1', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    #TODO
    replyMarkup = EmoDiarySetupMarkup(replyButtons,backButton,2)
    replyText = await repo.interface.get_messageText('NTR_setup_step_1',user.language)
    
    stateData = await state.get_data()
    


    await state.set_data(stateData)

    await callback.message.edit_text(replyText, reply_markup=replyMarkup) 

@user_callbacks_router.callback_query(F.data.contains('ntr_utc_'), StateFilter(UserStates.main_menu))
async def show_ntr_setup_step_2(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()

    stateData = await state.get_data()
    delta = int(callback.data.split('_')[1])
    stateData['interventionsStatus']['emodiary']['timedelta'] = delta

    if len(callback.data.split('_'))==2:
        
        pass
        
        
    else:
      
        selected_time = callback.data.split('_')[2]
        notifications = stateData['interventionsStatus']['emodiary']['notification_time']
        notifications.append(selected_time)
        stateData['interventionsStatus']['emodiary']['notification_time'] = notifications

        await state.set_data(stateData)
        

    notifications = stateData['interventionsStatus']['emodiary']['notification_time']
    numberOfnotification = stateData['interventionsStatus']['emodiary']['no_of_notifications']

    if len(notifications)==numberOfnotification:
        stateData['interventionsStatus']['emodiary']['status'] = True
        await state.set_data(stateData)
        await send_main_menu(bot, user.user_id, user.language, state, repo)
    else:
        replyButtons = await repo.interface.get_ButtonLables('emodiary_setup_step_3', user.language)
        replyText = await repo.interface.get_messageText('emodiary_setup_step_3',user.language)
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        replyMarkup = EmoDiarySetupMarkup(replyButtons,backButton,3, delta)
    
        replyTextFormatted= replyText.format(numberOfnotification,len(notifications)+1)
        await callback.message.edit_text(replyTextFormatted, reply_markup=replyMarkup)


    
    