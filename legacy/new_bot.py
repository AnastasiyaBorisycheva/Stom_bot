import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
import pandas as pd
import os
from send import sm, edit_last_message
from time import sleep
from datetime import datetime
from messages_bot import messages_bot


root_dir = os.path.split(os.path.abspath(__file__))[0]
save_file = os.path.join(root_dir, 'chats.xlsx')
instruction_file = os.path.join(root_dir, 'Инструкция.docx')
if os.path.isfile(save_file):
    chats = pd.read_excel(save_file)
else:
    chats = {}

temp_df = {}
for k in chats.keys():
    temp_df[k]=chats[k].tolist()
chats = temp_df

admins = {'chat_id':[], 'Notification':[]}
for i in chats['ids']:
    ind = chats['ids'].index(i)
    if chats['isAdmin'][ind]==1:
        admins['chat_id'].append(i)
        admins['Notification'].append(chats['Notification'][ind])


v_ids = pd.read_excel(os.path.join(root_dir, 'video.xlsx'))
temp_df = {}
for k in v_ids.keys():
    temp_df[k]=v_ids[k].tolist()
v_ids = temp_df

def save_chats():
    global chats
    mlength = max([len(chats[k]) for k in chats.keys()])
    for k in chats.keys():
        while len(chats[k])<mlength:
            chats[k].append('')
    pd.DataFrame(chats).to_excel(os.path.join(root_dir,save_file), index=False)

def edit_chats(id, c_name, text):
    global chats
    chats[c_name][chats['ids'].index(id)]=text
    pd.DataFrame(chats).to_excel(os.path.join(root_dir,save_file), index=False)

def get_file_path(ss):
    temp = os.path.split(os.path.abspath(__file__))[0]
    for i in ss.split('/'):
        temp = os.path.join(temp, i)
    return temp


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


def send_msg(bot,chat_id, dct):
    global chats
    ind = chats['ids'].index(chat_id)
    if dct['edit_last_message']==True:
        if 'photo' in dct.keys():
            #chats['last_msg_id'][ind]=edit_last_message(bot, chat_id, chats['last_msg_id'][ind], photo=get_file_path(f'photo/'+dct['photo']), text=dct['caption'] if dct['caption']!='#' else '', buttons=dct['buttons'] if 'buttons' in dct.keys() else None)
            chats['last_msg_id'][ind]=edit_last_message(bot, chat_id, chats['last_msg_id'][ind], photo=v_ids['id'][v_ids['Наименование файла'].index(dct['photo'])], text=dct['caption'] if dct['caption']!='#' else '', buttons=dct['buttons'] if 'buttons' in dct.keys() else None)
        elif 'video_hash' in dct.keys():
            chats['last_msg_id'][ind]=edit_last_message(bot, chat_id, chats['last_msg_id'][ind], video_id=dct['video_hash'], text=dct['caption'] if dct['caption']!='#' else '', buttons=dct['buttons'] if 'buttons' in dct.keys() else None)
        else:
            chats['last_msg_id'][ind]=edit_last_message(bot, chat_id, chats['last_msg_id'][ind], text=dct['caption'] if dct['caption']!='#' else '', buttons=dct['buttons'] if 'buttons' in dct.keys() else None)
    else:
        if 'photo' in dct.keys():
            #chats['last_msg_id'][ind]=sm(bot, chat_id, photo=get_file_path(f'photo/'+dct['photo']), text=dct['caption'] if dct['caption']!='#' else '', buttons=dct['buttons'] if 'buttons' in dct.keys() else None)
            chats['last_msg_id'][ind]=sm(bot, chat_id, photo=v_ids['id'][v_ids['Наименование файла'].index(dct['photo'])], text=dct['caption'] if dct['caption']!='#' else '', buttons=dct['buttons'] if 'buttons' in dct.keys() else None)
        elif 'video_hash' in dct.keys():
            chats['last_msg_id'][ind]=sm(bot, chat_id, video_id=dct['video_hash'], text=dct['caption'] if dct['caption']!='#' else '', buttons=dct['buttons'] if 'buttons' in dct.keys() else None)
        else:
            chats['last_msg_id'][ind]=sm(bot, chat_id, text=dct['caption'] if dct['caption']!='#' else '', buttons=dct['buttons'] if 'buttons' in dct.keys() else None)

def find_msg_by_id(id):
    for k in messages_bot:
        if k['message_id']==id:
            return k
    return False

@bot.message_handler(commands=['iamadminT3FRV4gK1phdbMK'])
def send_welcome(message):
    global chats
    chat_id = message.chat.id
    ind = chats['ids'].index(chat_id)
    chats['isAdmin'][ind]=1
    if not(chat_id in admins['chat_id']):
        admins['chat_id'].append(chat_id)
        admins['Notification'].append(1)
    save_chats()
    sm(bot, chat_id, text='Вы успешно получили права администратора!\nКогда новые клиенты будут запрашивать обратную связь, Вы получите уведомление в этом чате.\nЧтобы войти в панель администратора, введите /panel')

@bot.message_handler(commands=['panel'])
def send_welcome(message):
    global chats
    chat_id = message.chat.id
    ind = chats['ids'].index(chat_id)
    if chats['isAdmin'][ind]==1:
        send_msg(bot,message.chat.id, find_msg_by_id('admin_panel'))
    save_chats()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chats
    u_ind = None
    if not message.chat.id in chats['ids']:
        chats['ids'].append(message.chat.id)
        u_ind = len(chats['ids'])-1
        chats['name'].append('\'@'+str(message.from_user.username))
        chats['last_users_activity'].append(str(datetime.now()))
        save_chats()
    if not u_ind:
        u_ind = chats['ids'].index(message.chat.id)
    param = message.text[7:]
    if '_' in param:
        place = param[:param.index('_')]
        chats['from'][u_ind]=place
        param = param[len(place)+1:]
        if param == "WT":
            send_msg(bot,message.chat.id, find_msg_by_id('wisdom_teeth_start_f'))
        elif param == "TMJ":
            send_msg(bot,message.chat.id, find_msg_by_id('vncs_start_f'))
        elif param == "WEAR":
            send_msg(bot,message.chat.id, find_msg_by_id('wear_start_f'))
        elif param == 'BITE':
            send_msg(bot,message.chat.id, find_msg_by_id('bite_start_f'))
        elif param == 'BRACES':
            send_msg(bot,message.chat.id, find_msg_by_id('braces_start_f'))
        else:
            send_msg(bot,message.chat.id, find_msg_by_id('start_main'))
    else:
        send_msg(bot,message.chat.id, find_msg_by_id('start_main'))

    save_chats()

@bot.message_handler(content_types=['video', 'photo'])
def handle_video(message):
    chat_id = message.chat.id
    try:
        file_name = message.video.file_name
        file_size = message.video.file_size
        file_id = message.video.file_id
    except:
        file_name = message.caption
        file_size = message.photo[0].file_size
        file_id = message.photo[0].file_id
    if chat_id==chats['ids'][0]:
        if not file_name in v_ids['Наименование файла']:
            v_ids['Наименование файла'].append(file_name)
            v_ids['Размер'].append(file_size)
            v_ids['id'].append(file_id)
        elif not file_size==v_ids['Размер'][v_ids['Наименование файла'].index(file_name)]:
            v_ids['Размер'][v_ids['Наименование файла'].index(file_name)]=file_size
            v_ids['id'][v_ids['Наименование файла'].index(file_name)]=file_id
            print(f'Видео {file_name} было изменено. Перезалил на сервер')
        elif file_name in v_ids['Наименование файла']:
            v_ids['id'][v_ids['Наименование файла'].index(file_name)]=file_id
    pd.DataFrame(v_ids).to_excel('video.xlsx', index=False)
    bot.send_message(chat_id, f"Add a video! File ID: {file_id}")

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global chats
    chat_id = call.message.chat.id
    ind = chats['ids'].index(chat_id)
    chats['last_users_activity'][ind]=str(datetime.now())
    chats['position'][ind]=str(call.data)
    #if call.data=='spec':
    if 'test_vncs_q' in call.data or 'wear_test_q' in call.data or 'bite_braces_q' in call.data or 'wisdom_teeth_test_q' in call.data:                                  #########ТЕСТЫ
        dtd = call.data.split('_')
        q_num = dtd[2].replace('q','')
        if 'wisdom' in call.data:
            q_num = dtd[3].replace('q','')
        if q_num!='1':
            chats[call.data[:-3]+str(int(q_num)-1)][ind]=call.data[len(call.data)-1]
            send_msg(bot,chat_id, find_msg_by_id(call.data[:-2]))
        else:
            send_msg(bot,chat_id, find_msg_by_id(call.data))
    elif 'bite_type_' in call.data:
        chats['Type'][ind]=call.data[-1:]
        send_msg(bot,chat_id, find_msg_by_id(call.data))
    elif 'result_vncs_normal_' in call.data:                                                    ########РЕЗУЛЬТАТ ВНЧС
        chats['test_vncs_q5'][ind]=call.data[len(call.data)-1]
        itogo = sum([int(chats[i][ind]) for i in [f'test_vncs_q{k}' for k in range(1,6)]])
        if itogo<2:
            send_msg(bot,chat_id, find_msg_by_id('result_vncs_normal'))
        elif itogo<4:
            send_msg(bot,chat_id, find_msg_by_id('result_vncs_overload'))
        elif itogo<6:
            send_msg(bot,chat_id, find_msg_by_id('result_vncs_dysfunction'))
        else:
            print(send_msg(bot,chat_id, find_msg_by_id('result_vncs_pathology')))

    elif 'wear_result_' in call.data:                                                           ########РЕЗУЛЬТАТ СТИРАЕМОСТЬ
        chats['wear_test_q6'][ind]=call.data[len(call.data)-1]
        itogo = sum([int(chats[i][ind]) for i in [f'wear_test_q{k}' for k in range(1,7)]])
        if itogo<3:
            send_msg(bot,chat_id, find_msg_by_id('wear_result_low'))
        elif itogo<6:
            send_msg(bot,chat_id, find_msg_by_id('wear_result_medium'))
        elif itogo<9:
            send_msg(bot,chat_id, find_msg_by_id('wear_result_high'))
        else:
            send_msg(bot,chat_id, find_msg_by_id('wear_result_critical'))

    elif 'bite_result_' in call.data:                                                           #############РЕЗУЛЬТАТЫ БРЕКЕТЫ
        chats['bite_braces_q5'][ind]=call.data[len(call.data)-1]
        itogo = sum([int(chats[i][ind]) for i in [f'bite_braces_q{k}' for k in range(1,6)]])
        if itogo<3:
            send_msg(bot,chat_id, find_msg_by_id('bite_result_no_braces'))
        elif itogo<6:
            send_msg(bot,chat_id, find_msg_by_id('bite_result_consult'))
        else:
            send_msg(bot,chat_id, find_msg_by_id('bite_result_need_braces'))

    elif 'wisdom_teeth_result_' in call.data:                                                  #############РЕЗУЛЬТАТЫ ЗУБЫ МУДРОСТИ
        chats['wisdom_teeth_test_q5'][ind]=call.data[len(call.data)-1]
        itogo = sum([int(chats[i][ind]) for i in [f'wisdom_teeth_test_q{k}' for k in range(1,6)]])
        if itogo<4:
            send_msg(bot,chat_id, find_msg_by_id('wisdom_teeth_result_low'))
        elif itogo<7:
            send_msg(bot,chat_id, find_msg_by_id('wisdom_teeth_result_medium'))
        else:
            send_msg(bot,chat_id, find_msg_by_id('wisdom_teeth_result_high'))
    elif call.data=='consultation':
        send_msg(bot,chat_id, find_msg_by_id('consultation'))
        text = f'Пользователь {chats['name'][ind][1:]} запросил консультацию.\n'
        if type(chats['Type'][ind])==type(''):
            type_p = {'1': 'Правильный', '2':'Мезиальный', '3':'Глубокий', '4':'Перекрёстный', '5':'Диастема', '6':'Скученность', '7':'Открытый'}[chats['Type'][ind]]
            text+=f'Тип прикуса: {type_p}\n'
        if chats['test_vncs_q5'][ind] in [0,1,2,'0','1','2']:
            text+=f'Результат теста по ВНЧС: {sum([int(chats[i][ind]) for i in [f'test_vncs_q{k}' for k in range(1,6)]])}/10\n'
        if chats['wear_test_q6'][ind] in [0,1,2,'0','1','2']:
            text+=f'Результат теста по стираемости: {sum([int(chats[i][ind]) for i in [f'wear_test_q{k}' for k in range(1,7)]])}/12\n'
        if chats['bite_braces_q5'][ind] in [0,1,2,'0','1','2']:
            text+=f'Результат теста по прикусу: {sum([int(chats[i][ind]) for i in [f'bite_braces_q{k}' for k in range(1,6)]])}/10\n'
        if chats['wisdom_teeth_test_q5'][ind] in [0,1,2,'0','1','2']:
            text+=f'Результат теста по зубам мудрости: {sum([int(chats[i][ind]) for i in [f'wisdom_teeth_test_q{k}' for k in range(1,6)]])}/10\n'
        for admin in range(len(admins['chat_id'])):
            if admins['Notification'][admin]==1:
                sm(bot,admins['chat_id'][admin], text = text, markdown=False)
    elif call.data in ['download_info', 'download_instruction', 'SetNotifications', 'offNotifications', 'onNotifications']:
        if call.data == 'download_info':
            with open(save_file, 'rb') as file:
                bot.send_document(chat_id, file)
        elif call.data == 'download_instruction':
            with open(instruction_file, 'rb') as file:
                bot.send_document(chat_id, file)
        elif call.data=='SetNotifications':
            text = f'Сейчас уведомления {'включены' if chats['Notification'][ind]==1 else 'отключены'}.'
            buttons = [['<<< Назад', 'admin_panel'], ['Отключить', 'offNotifications'] if chats['Notification'][ind]==1 else ['Включить', 'onNotifications']]
            chats['last_msg_id'][ind] = sm(bot, chat_id, text, buttons=buttons)
        else:
            chats['Notification'][ind]= 1 if chats['Notification'][ind]==0 else 0
            save_chats()
            admins['Notification'][admins['chat_id'].index(chats['ids'][ind])]=chats['Notification'][ind]
            chats['last_msg_id'][ind] = edit_last_message(bot, chat_id, chats['last_msg_id'][ind], text=f'Сейчас уведомления {'включены' if chats['Notification'][ind]==1 else 'отключены'}.', buttons=[['<<< Назад', 'admin_panel'], ['Отключить', 'offNotifications'] if chats['Notification'][ind]==1 else ['Включить', 'onNotifications']])



    elif not call.data in ['wisdom_teeth_education', 'more_cases_bite', 'wear_cases']:
        send_msg(bot,chat_id, find_msg_by_id(call.data))
    elif call.data=='wisdom_teeth_education': ######################## ОТПРАВКА КЕЙСА ЗУБОВ МУДРОСТИ (С АУДИО)
        keyboard = InlineKeyboardMarkup()
        #for btn_text, btn_id in [['🔘 Записаться на консультацию', 'consultation'],['🔘 Зубы мудрости', 'wisdom_teeth_start'],['🔘 Стираемость зубов', 'wear_start'],['🔘 Прикус', 'bite_start'],['🔘 ВНЧС', 'vncs_learn_1']]:
        #    keyboard.add(InlineKeyboardButton(text=btn_text, callback_data=btn_id))
        #with open(get_file_path(f'photo/кейс_зубы_мудрости_2.JPG'), 'rb') as photo_file:
        bot.send_photo(chat_id, v_ids['id'][v_ids['Наименование файла'].index('кейс_зубы_мудрости_2.JPG')])
        #with open(get_file_path(f'photo/кейс_зубы_мудрости_1.JPG'), 'rb') as photo_file:
        bot.send_photo(chat_id, v_ids['id'][v_ids['Наименование файла'].index('кейс_зубы_мудрости_1.JPG')])

        chats['last_msg_id'][ind]=bot.send_audio(chat_id, open(get_file_path(f'photo/кейс зубы мудрости.mp3'), 'rb'))
        chats['last_msg_id'][ind] = sm(bot,chat_id,text='После прослушивания информации об этом кейсе, можете записаться на консультацию или изучить другую тему.', buttons=[['🔘 Записаться на консультацию', 'consultation'],['🔘 Зубы мудрости', 'wisdom_teeth_start'],['🔘 Стираемость зубов', 'wear_start'],['🔘 Прикус', 'bite_start'],['🔘 ВНЧС', 'vncs_learn_1']])
    elif 'wear_cases'==call.data:
        keyboard = InlineKeyboardMarkup()
        for btn_text, btn_id in [['🔘 Записаться на консультацию', 'consultation'],['🔘 Зубы мудрости', 'wisdom_teeth_start'],['🔘 ВНЧС', 'vncs_learn_1'],['🔘 Стираемость зубов', 'wear_start'],['🔘 Прикус', 'bite_start']]:
            keyboard.add(InlineKeyboardButton(text=btn_text, callback_data=btn_id))
        #with open(get_file_path(f'photo/Стираемость 1.jpg'), 'rb') as photo_file:
        #    bot.send_photo(chat_id, photo_file)
        #with open(get_file_path(f'photo/Стираемость 2.jpg'), 'rb') as photo_file:
        #    bot.send_photo(chat_id, photo_file)
        bot.send_photo(chat_id, v_ids['id'][v_ids['Наименование файла'].index('Стираемость 1.jpg')])
        #bot.send_photo(chat_id, v_ids['id'][v_ids['Наименование файла'].index('Стираемость 2.jpg')], reply_markup=keyboard)
        chats['last_msg_id'][ind]=sm(bot,chat_id, photo=v_ids['id'][v_ids['Наименование файла'].index('Стираемость 2.jpg')], buttons=[['🔘 Записаться на консультацию', 'consultation'],['🔘 Зубы мудрости', 'wisdom_teeth_start'],['🔘 ВНЧС', 'vncs_learn_1'],['🔘 Стираемость зубов', 'wear_start'],['🔘 Прикус', 'bite_start']])
        #send_msg(bot,chat_id, find_msg_by_id(call.data))
    elif call.data=='more_cases_bite': ############################### ОТПРАВКА КЕЙСОВ БРЕКЕТЫ 2
        vidosiki = [
        InputMediaVideo('BAACAgIAAxkBAAICJ2l0mZQ7GCxnUKxg_vh0shw3VdT_AAL3ggACHl_QSPhqpxTVD2V3OAQ'),
        InputMediaVideo('BAACAgIAAxkBAAICGWl0kyQrakBph1xi2fwBMHyArNUfAAL2ggACHl_QSD3xiidOFgvgOAQ'),
        InputMediaVideo('BAACAgIAAxkBAAICKGl0mZT3vINPd9oeVywZf4FMly_sAAL4ggACHl_QSM7dBNuBg8_AOAQ'),
        InputMediaVideo('BAACAgIAAxkBAAICKWl0mZQCwL6ZcIpEo-W2fa2zWMj9AAL5ggACHl_QSPbYjMrkBfAqOAQ'),
        InputMediaVideo('BAACAgIAAxkBAAICKml0mZS2uJI2XNBk4kWMjGdHqma3AAL6ggACHl_QSHAYOlxCT3DmOAQ'),]
        capt = """🦷 *Разбираем кейс одной из наших пациенток*
С чем столкнулись?
- несоответствие размеров верхней и нижней челюсти
- недостаточно места для клыков в зубном ряду
- проблемы с целостностью эмали после проведенного ранее ортодонтического лечения
Процесс лечения:
- удаление четырех премоляров, с целью сохранения клыков
- проведение ортодонтического лечения на брекет-системе для выравнивания положения зубов
В видео показали в 3D моделировании как будут выглядеть зубы после лечения 👆🏼
#МАРТИортодонтия
📍 г.Москва, 3-й Павелецкий проезд, 3
📞 +7 (495) 003-14-53
✈️ @stommarti"""
        keyboard = InlineKeyboardMarkup()
        for btn_text, btn_id in [
            ['🔘 Записаться на консультацию', 'consultation'], ['🔘 Зубы мудрости', 'wisdom_teeth_start'],['🔘 ВНЧС', 'vncs_learn_1'],['🔘 Стираемость зубов', 'wear_start'],['🔘 Прикус', 'bite_start']]:
            keyboard.add(InlineKeyboardButton(text=btn_text, callback_data=btn_id))
        bot.send_media_group(chat_id, vidosiki)
        chats['last_msg_id'][ind]=sm(bot,chat_id,text=capt, buttons=[['🔘 Записаться на консультацию', 'consultation'], ['🔘 Зубы мудрости', 'wisdom_teeth_start'],['🔘 ВНЧС', 'vncs_learn_1'],['🔘 Стираемость зубов', 'wear_start'],['🔘 Прикус', 'bite_start']])

    save_chats()

bot.infinity_polling()
