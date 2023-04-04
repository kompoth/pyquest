# pyquest - Telegram bot to prepare for interviews

I develop this bot as my personal instrument that reminds me to walk through
some topics for Python developer interviews on a daily basis. It's not just a
reminder as it features a menu with a list of preloaded questions, divided
into sections.

This repo also contains scripts to load those questions from a Markdown file.
I personaly use [this](https://github.com/yakimka/python_interview_questions)
repo that covers a huge number of topics on Python. This is only in Russian
though.

I'm going to add a database with user information soon. This would allow users
to set preffered reminder time and to mark questins and topics as completed.

Sorry, currently pyquest repo is a mess as development is in a pre-alpha state.

## Running pyquest

Create virtual environment and install dependencies:
```
python -n venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make a copy of `example_config.toml`, name it `config.toml` and edit the way
you need.

Now you can start bot with following command:
```
python -m pyquest
```
