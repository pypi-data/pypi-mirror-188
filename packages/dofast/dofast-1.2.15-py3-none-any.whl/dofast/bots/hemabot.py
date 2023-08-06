#!/usr/bin/env python
"""
Simple Bot to send timed Telegram messages.

This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import re
from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import uuid4

import codefast as cf
from codefast.patterns.singleton import SingletonMeta
from telegram import Bot, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dofast.auth import auth
from dofast.bots.processors.deepl import DeeplProcessor
from dofast.bots.processors.mix import AvatarProcessor, WeatherProcessor
from dofast.bots.processors.oncemessager import OnceMessager
from dofast.bots.processors.pcloud import PcloudProcessor
from dofast.bots.processors.twitter import TwitterVideoDownloader
from dofast.oss import Bucket
from dofast.utils import DeeplAPI

from .mysqlite import Message as SqlMessage


class BotProducer(metaclass=SingletonMeta):

    def __init__(self) -> None:
        Bot(auth.hema)


class TextClient:

    @staticmethod
    def run_in_order(objects: List, text: str, update: Update) -> bool:
        obj = next((o for o in objects if o.match(text)), None)
        if obj:
            cf.info("Matched {}".format(obj.__class__.__name__))
            obj.process(text, update)


def get_text_handler(text: str) -> MessageHandler:
    reflection = {
        'oncemessage': OnceMessager,
        'weather': WeatherProcessor,
        'avatar': AvatarProcessor,
        'deepl': DeeplProcessor,
        'pcloud': PcloudProcessor,
        'twitter': TwitterVideoDownloader
    }
    try:
        if re.findall(r'[\u4e00-\u9fff]+', text):  # contain chinese
            label = 'deepl'
        else:
            params = {'text': text}
            resp = cf.net.post('http://localhost:5000', json=params)
            label = resp.json()['label']
    except Exception as e:
        cf.info(e)
        label = ''

    return reflection.get(label, None)


class Psycho(object):

    def __init__(self):
        cf.info('start Psycho TG bot.')
        self.bucket = Bucket()
        self.deeplapi = DeeplAPI()
        self.bot_name = 'hemahema'
        self.text = ''
        self.sql_messager = SqlMessage()
        self.pool = ThreadPoolExecutor(23)

    def alarm(self, context: CallbackContext) -> None:
        """Send the alarm message."""
        job = context.job
        context.bot.send_message(job.context, text=self.text)

    def remove_job_if_exists(self, name: str,
                             context: CallbackContext) -> bool:
        """Remove job with given name. Returns whether job was removed."""
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    def deepl(self, update: Update, context: CallbackContext) -> None:
        '''deepl trans'''
        text = ' '.join(context.args)
        result = self.deeplapi.translate(text)['translations'].pop()['text']
        update.message.reply_text(result)

    def set_timer(self, update: Update, context: CallbackContext) -> None:
        """Add a job to the queue."""
        chat_id = update.message.chat_id
        try:
            # args[0] should contain the time for the timer in seconds
            due = int(context.args[0])
            if due < 0:
                update.message.reply_text(
                    'Sorry we can not go back to future!')
                return

            job_removed = self.remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(self.alarm,
                                       due,
                                       context=chat_id,
                                       name=str(chat_id))

            text = 'Timer successfully set!'
            if job_removed:
                text += ' Old one was removed.'
            update.message.reply_text(text)

        except (IndexError, ValueError):
            update.message.reply_text('Usage: /set <seconds>')

    def unset(self, update: Update, context: CallbackContext) -> None:
        """Remove the job if the user changed their mind."""
        chat_id = update.message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id), context)
        text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
        update.message.reply_text(text)

    def text_handler(self, update: Update, context: CallbackContext) -> None:
        """Echo the user message."""
        if not update.message:
            # Avoid error when user sends a message without text
            return
        text = update.message.text
        self.sql_messager.add(text)
        self.text = text
        cf.io.write(text, '/tmp/wechat.txt')
        cf.info(f"received text: {text}")
        processor = get_text_handler(text)
        if processor:
            update.message.reply_text('Match {}'.format(processor.__name__))
            self.pool.submit(processor().process, text, update)
        else:
            update.message.reply_text('Input {} found No match'.format(text))

    def file_handler(self, update: Update, context: CallbackContext) -> None:
        ''' save phone to cloud
        # https://stackoverflow.com/questions/50388435/how-save-photo-in-telegram-python-bot
        '''
        _files = []
        if update.message.document:
            # uncompressed photo
            file_id = update.message.document.file_id
            file_type = update.message.document.mime_type.split('/')[-1]

        elif update.message.photo:
            # compressed photo
            file_type = 'jpeg'
            photoes = update.message.photo
            cf.info('receive photos', photoes)
            for p in photoes[-1:]:
                file_id = p.file_id
                file_name = f'{uuid4()}.{file_type}'
                obj = context.bot.get_file(file_id)
                obj.download(file_name)
                _files.append(file_name)
                cf.info(f"received photo: {file_name}")

        elif update.message.video:
            file_type = 'mp4'
            video = update.message.video
            cf.info('receive videos', video)
            file_id = video['file_id']
            file_name = f'{uuid4()}.{file_type}'
            obj = context.bot.get_file(file_id)
            obj.download(file_name)
            _files.append(file_name)
            cf.info(f"received video: {file_name}")

        else:
            update.message.reply_text(
                'No photo nor ducument detected from {}'.format(
                    str(update.message)))
            return

    @staticmethod
    def main() -> None:
        """Run bot
        update.message methods: https://docs.pyrogram.org/api/bound-methods/Message.reply_text
        """
        psy = Psycho()
        token = auth.hema
        updater = Updater(token)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("set", psy.set_timer))
        dispatcher.add_handler(CommandHandler(("deepl", 'dpl'), psy.deepl))
        dispatcher.add_handler(CommandHandler("unset", psy.unset))
        dispatcher.add_handler(MessageHandler(Filters.text, psy.text_handler))
        dispatcher.add_handler(
            MessageHandler(Filters.document | Filters.photo | Filters.video,
                           psy.file_handler))

        # Start the Bot
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    Psycho.main()
