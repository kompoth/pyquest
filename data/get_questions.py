from parse_md import md_2_dict, md_2_tree
import json

raw_url = 'https://raw.githubusercontent.com/yakimka/python_interview_questions/master/questions.md'
base_url = 'https://github.com/yakimka/python_interview_questions/blob/master/questions.md'

ignore = [
    'root/Django',
    'root/Вопросы работодателю',
    'root/Дизайн-интервью',
    'root/Интересные ссылки',
    'root/Источники вопросов'
]

if __name__ == '__main__':
    q_dict = md_2_dict(raw_url, base_url, ignore=ignore)
    with open('questions.json', 'w', encoding='utf-8') as fp:
        json.dump(q_dict, fp, ensure_ascii=False)
