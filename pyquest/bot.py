import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pyquest.config import config
from pyquest.markup import gen_menu, gen_answer_link
from pyquest.db import check_timer 
import pyquest.nodes as nodes

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
       for text in gen_answer_link(path):
            await bot.send_message(
                query.from_user.id,
                text=text,
                parse_mode="html"
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

@dp.message_handler(commands=['full_dbg'])
async def cmd_full_dbg(message: Message):
    queue = [None]
    while queue:
        path = queue.pop()
        node = nodes.find_node(path)
        if node['kids']:
            if path is not None:
                path += '#'
            else:
                path = ''
            new_vals = [path + str(kid['order']) for kid in node['kids']]
            queue += new_vals
        else:
            for text in gen_answer(path):
                await bot.send_message(
                    message.chat.id,
                    text=text,
                    parse_mode="Markdown"
                )


async def send_reminders():
    for chat_id in check_timer():
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
