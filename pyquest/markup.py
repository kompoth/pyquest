import re
import markdown
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from aiogram.utils.callback_data import CallbackData

import pyquest.nodes as nodes

MAX_BATCH_LEN = 4036

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
        callback_data=choice_cb.new(
            path=new_path,
            leaf=not kid['kids']
        )
        button = InlineKeyboardButton(
            text=f"{emoji} {kid['title']}",
            callback_data=callback_data
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

def gen_answer_html(path: str):
    ans_str = markdown.markdown(nodes.cat_node(path))
    ans = []
    for par in re.split(r'<\/?p>', ans_str):
        par = par.replace('<ol>', '').replace('</ol>', '')
        par = par.replace('<ul>', '').replace('</ul>', '')
        par = par.replace('<li>', '- ').replace('</li>', '')
        par = par.replace('<h1>', '<strong>').replace('</h1>', '</strong>')
        if ans and len(ans[-1] + par) < MAX_BATCH_LEN:
            ans[-1] += '\n' + par
        elif len(par) < MAX_BATCH_LEN:
            ans.append(par)
        else:
            raise ValueError 
        print(par)
    return ans

def gen_answer_link(path: str):
    node = nodes.find_node(path)
    link = f"<a href=\"{node['url']}\">{node['title']}</a>"
    print(link)
    return [link]
