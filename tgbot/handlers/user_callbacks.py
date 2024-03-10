from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, ForceReply
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
import logging
import os
from datetime import datetime, time

from aiogram import Bot

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models.users import User

from ..services.services import send_message, delete_message
from ..services.send_questionaire import sendNextQuestion
from ..services.send_main_menu import send_main_menu, send_completed_emodiary_menu, send_completed_ntr_menu
from ..services.put_user_to_default import putUserToDefault

from ..misc.states import UserStates

from ..misc.emodiary_report import generatePDFReport
from aiogram.types import BufferedInputFile

from ..keyboards.inline import StandardButtonMenu,dimeGameMarkup,EmoDiarySetupTrue, ntrSetupTrue, EmoDiarySetupMarkup,EmoDiarySetupMarkup, getEmotionList
from infrastructure.database.models import message as logmessage

user_callbacks_router = Router()
logger = logging.getLogger(__name__)

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
    await putUserToDefault(user, repo, bot, state)


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
        await send_completed_emodiary_menu(repo, bot, user,  state)
        # replyText=await repo.interface.get_messageText('emodiary_setup_true',user.language)
        # numberOfnotification = state_data['interventionsStatus']['emodiary']['no_of_notifications']
        # notifications = state_data['interventionsStatus']['emodiary']['notification_time']
        # delta = state_data['interventionsStatus']['emodiary']['timedelta']
        # notifications_formated = ', '.join(notifications)
        # timezone = 'UTC '+str(delta)
        # replyTextFormatted = replyText.format(numberOfnotification,notifications_formated,timezone)


        # replyButtons= await repo.interface.get_ButtonLables('emodiary_setup_true', user.language)
        # backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        # replyMarkup = EmoDiarySetupTrue(replyButtons+backButton)
        # await send_message(bot, user.user_id, replyTextFormatted, reply_markup=replyMarkup, repo = repo)

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
    if numberOfNotification == 0:
        await repo.interventions.deleteNotificationTime(user.user_id, 'emodiary') 
        stateData = await state.get_data()  
        stateData['interventionsStatus']['emodiary']['no_of_notifications'] = 0
        stateData['interventionsStatus']['emodiary']['notification_time'] = ['Do Not Notify']
        stateData['interventionsStatus']['emodiary']['timedelta'] = 0
        stateData['interventionsStatus']['emodiary']['status'] = True
        await state.set_data(stateData)
        await send_main_menu(bot, user.user_id, user.language, state, repo)
    else:
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
        #save intervention notification to DB
        
        await repo.interventions.deleteNotificationTime(user.user_id, 'emodiary')
        for notificationTime in notifications:
            selected_hour_utc =int(notificationTime.split(':')[0])-delta
            if selected_hour_utc>=24:
                selected_hour_utc = selected_hour_utc-24
            elif selected_hour_utc<0:
                selected_hour_utc = selected_hour_utc+24
                
            await repo.interventions.setNotificationTime(user.user_id,'emodiary',str(delta), time(selected_hour_utc,0,0))
        
        # await repo.interventions.setNotificationTime(user.user_id,'emodiary',delta, notifications)
        await state.set_data(stateData)


        #TODO here instead of sending main menu send emotional diary markup with true
        await send_completed_emodiary_menu(repo, bot, user, 
                                            state,message_to_change=callback.message)
        # await send_main_menu(bot, user.user_id, user.language, state, repo)
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
    ntrStatus = state_data['interventionsStatus']['ntr']['status']

    if ntrStatus:
        await send_completed_ntr_menu(repo, bot, user,  state)
    else:

        replyText=await repo.interface.get_messageText('ntr_setup_false',user.language)
        replyButtons= await repo.interface.get_ButtonLables('ntr_setup_false', user.language)
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        replyMarkup = StandardButtonMenu(replyButtons+backButton)
        await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)



@user_callbacks_router.callback_query(F.data.contains('ntr_setup_step_1'), StateFilter(UserStates.main_menu))
async def show_ntr_setup(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    isConfiguredString=callback.data.split('_')[4]
    if isConfiguredString == 'true':
        stopButton = await repo.interface.get_ButtonLables('ntr_stop_notifications', user.language)
        

        
    replyButtons = await repo.interface.get_ButtonLables('ntr_setup_step_1', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
    
    if isConfiguredString == 'true':
        stopButton = await repo.interface.get_ButtonLables('ntr_stop_notifications', user.language)
        replyMarkup = EmoDiarySetupMarkup(replyButtons,[stopButton[0],backButton[0]],2)
    else:
        replyMarkup = EmoDiarySetupMarkup(replyButtons,backButton,2)
    replyText = await repo.interface.get_messageText('ntr_setup_step_1',user.language)
    
    stateData = await state.get_data()
    


    await state.set_data(stateData)

    await callback.message.edit_text(replyText, reply_markup=replyMarkup) 

@user_callbacks_router.callback_query(F.data.contains('ntr_notif_0'), StateFilter(UserStates.main_menu))
async def show_ntr_setup(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.main_menu)
    await repo.interventions.deleteNotificationTime(user.user_id, 'ntr')

    stateData = await state.get_data()  

    stateData['interventionsStatus']['ntr']['notification_time'] = 'Not Defined'
    stateData['interventionsStatus']['ntr']['timedelta'] = 'Not defined'
    stateData['interventionsStatus']['ntr']['status'] = True
    await state.set_data(stateData)
    await send_completed_ntr_menu(repo, bot, user, state, message_to_change=callback.message)
    

@user_callbacks_router.callback_query(F.data.contains('ntrutc_'), StateFilter(UserStates.main_menu))
async def show_ntr_setup_step_2(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()

    stateData = await state.get_data()
    delta = int(callback.data.split('_')[1])
    stateData['interventionsStatus']['ntr']['timedelta'] = delta
    notifications=[]
    if len(callback.data.split('_'))==2:
        
        await state.set_data(stateData)
        replyButtons = await repo.interface.get_ButtonLables('ntr_setup_step_2', user.language)
        replyText = await repo.interface.get_messageText('ntr_setup_step_2',user.language)
        backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)
        replyMarkup = EmoDiarySetupMarkup(replyButtons,backButton,3, delta)
    
        await callback.message.edit_text(replyText, reply_markup=replyMarkup)
        
        
    else:
      
        selected_time = callback.data.split('_')[2]
        
       
        stateData['interventionsStatus']['ntr']['notification_time'] = selected_time
        await state.set_data(stateData)

        selected_hour_utc =int(selected_time.split(':')[0])-delta
        if selected_hour_utc>=24:
            selected_hour_utc = selected_hour_utc-24
        elif selected_hour_utc<0:
            selected_hour_utc = selected_hour_utc+24
        
        await repo.interventions.deleteNotificationTime(user.user_id, 'ntr')
        await repo.interventions.setNotificationTime(user.user_id,'ntr',str(delta), time(selected_hour_utc,0,0))
        stateData['interventionsStatus']['ntr']['status'] = True
        await state.set_data(stateData)
        await send_completed_ntr_menu(repo, bot, user,  state, message_to_change=callback.message)
        
@user_callbacks_router.callback_query(F.data=='emodiary_add_emotion', StateFilter(UserStates.main_menu))
async def add_emotion_1(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.set_emotion)

    replyText=await repo.interface.get_messageText('emodiary_add_emotion_1',user.language)
    replyEmotionButtons=await repo.interface.get_ButtonLables('emodiary_add_emotion_1', user.language)
    backButton = await repo.interface.get_ButtonLables('back_to_main', user.language)

    replyMarkup = getEmotionList(replyEmotionButtons,backButton)
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)

    
@user_callbacks_router.callback_query(F.data.contains('emotion_'), StateFilter(UserStates.set_emotion))
async def add_emotion_2(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.set_emotion_what_doing)
    current_data = await state.get_data()
    current_data['set_emotion']={
        'emotion': callback.data,
        'what_doing': None,
        'what_thinking': None
    }
    await state.set_data(current_data)

    replyText=await repo.interface.get_messageText('emodiary_add_emotion_2',user.language)
    
    await send_message(bot, user.user_id, replyText,  repo = repo, reply_markup=ForceReply())
 

    

@user_callbacks_router.callback_query(F.data == 'generate_emodiary_report')
async def generate_reports(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    emotions = await repo.interventions.getEmotions(user.user_id)
    title = await repo.interface.get_messageText('emodiary_report_title',user.language)
    path =os.getcwd()+'/report_template'

    

    pdfReport = generatePDFReport(title, emotions, path, "EmoDiary_report_template.html" )
    text_file = BufferedInputFile(pdfReport, filename="report.pdf")
    
    document = await bot.send_document(user.user_id, text_file)
    await repo.log_message.put_message(document,user.user_id, bot.id)


@user_callbacks_router.callback_query(F.data == 'feedback', StateFilter(UserStates.main_menu))
async def get_feedback(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    
    await state.set_state(UserStates.ask_feedback)
    replyText=await repo.interface.get_messageText(callback.data,user.language)
    replyMarkup = ForceReply()
    
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)


@user_callbacks_router.callback_query(F.data=='ntr_add_record', StateFilter(UserStates.main_menu))
async def add_ntr_1(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    await state.set_state(UserStates.set_ntr_step_1)
    current_data = await state.get_data()
    current_data['set_ntr']={
        'negative_thought': None,
        'reframing': None
    }
    await state.set_data(current_data)
    replyText=await repo.interface.get_messageText('ntr_set_step_1',user.language)
    
    replyMarkup = ForceReply()
    await send_message(bot, user.user_id, replyText, reply_markup=replyMarkup, repo = repo)


@user_callbacks_router.callback_query(F.data == 'generate_ntr_report')
async def generate_reports(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    ntrEntries = await repo.interventions.getNegativeThought(user.user_id)
    title = await repo.interface.get_messageText('ntr_report_title',user.language)
    path =os.getcwd()+'/report_template'

    

    pdfReport = generatePDFReport(title, ntrEntries, path, "NTR_report_template.html" )
    text_file = BufferedInputFile(pdfReport, filename="report.pdf")
    
    document = await bot.send_document(user.user_id, text_file)
    await repo.log_message.put_message(document,user.user_id, bot.id)



@user_callbacks_router.callback_query(F.data.contains('switgh_language_to_'))
async def switch_language(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot, user: User):
    await callback.answer()
    language = callback.data.split('_')[-1]
    await repo.users.setUserLanguage(user.user_id, language)
    
    replyMessage = await repo.interface.get_messageText('language_switched',language)
    await bot.send_message(user.user_id, replyMessage)