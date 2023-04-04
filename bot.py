from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, \
    InlineKeyboardMarkup, InlineKeyboardButton 
from aiogram.utils.callback_data import CallbackData
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

from config import config
import nodes
import db

MAX_BATCH_LEN = 4036
TRANS_DICT = str.maketrans({
    '(': r'\(', ')': r'\)', '-': r'\-', '+': r'\+',
    '.': r'\.', '#': r'\#', '>': r'\>'
})
ERR_MSG = '''Ошибка приложения:
<code>{}</code>
Пожалуйста, сообщи о ней администратору бота.'''
REM_MSG = '''Привет!
Напоминаю просмотреть вопросы для подготовки к собеседованию)
Чтобы перейти к списку вопросов, выполни команду /start
'''

# Initialize bot and dispatcher
bot = Bot(token=config.token)
dp = Dispatcher(bot)


def gen_menu(path: str):
    path = None if path == 'root' else path
    base_path = '' if not path else f'{path}#' 
    node = nodes.find_node(path)

    markup = InlineKeyboardMarkup()
    choice_cb = CallbackData('choice', 'path', 'leaf')
    
    for kid in node['kids']:
        if kid['done']:
            emoji = '✅'
        elif kid['kids']:
            emoji = '🗂'
        else:
            emoji = '📑'
        new_path = base_path + str(kid['order'])
        button = InlineKeyboardButton(
        text=f"{emoji} {kid['title']}",
            callback_data=choice_cb.new(
                path=new_path,
                leaf=not kid['kids']
            )
        )
        markup.add(button)

    if path:
        back_button = InlineKeyboardButton(
            text='🔙 В начало',
            callback_data=choice_cb.new(
                path='root',
                leaf=False
            )
        )
        markup.add(back_button)
    return markup

def gen_answer(path: str):
    ans_str = nodes.cat_node(path)
    ans = []
    pos = 0
    while pos < len(ans_str):
        new_pos = ans_str.find('\n', pos)
        if new_pos == -1:
            new_pos = min(len(ans_str), pos + MAX_BATCH_LEN)
        
        batch_str = ans_str[pos:new_pos]
        batch_str = batch_str.replace('**', r'*')
        batch_str = batch_str.translate(TRANS_DICT) 

        if ans and len(ans[-1] + batch_str) < MAX_BATCH_LEN:
            ans[-1] += '\n' + batch_str
        else:
            ans.append(batch_str)
        pos = new_pos + 1
    return ans

@dp.errors_handler()
async def error_msg(update, error):
    logging.error(error)
    chat_id = None
    for key, val in update:
        if isinstance(val, dict) and 'from' in val:
            chat_id = val['from']['id']
            break
    if chat_id:
        await bot.send_message(
            chat_id,
            text=ERR_MSG.format(error),
            parse_mode="html"
        )
    return chat_id is not None

@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    markup = gen_menu('root')
    await bot.send_message(
        message.chat.id,
        text='Выбери раздел',
        reply_markup=markup
    )

@dp.callback_query_handler()
async def menu_choice(query: CallbackQuery):
    path, leaf = query['data'].split(':')[1:]
    if leaf == 'True':
       for text in gen_answer(path):
            await bot.send_message(
                query.from_user.id,
                text=text,
                parse_mode="MarkdownV2"
            )
    else:
        markup = gen_menu(path)
        if path == 'root':
            text = 'Выбери раздел'
        else: 
            text = 'Выбери подраздел или вопрос'
        await bot.send_message(
            query.from_user.id,
            text=text,
            reply_markup=markup
        )

async def send_reminders():
    for chat_id in db.check_timer():
         await bot.send_message(
                chat_id, 
                text=REM_MSG
            )

def start_bot():
    logging.info('Starting bot')
    
    # Initialize scheduler
    period = config.period
    aps = AsyncIOScheduler(timezone=config.timezone)
    aps.add_job(send_reminders, 'cron', second=f'*/{period}')
    aps.start()

    # Start polling
    executor.start_polling(dp, skip_updates=True)
