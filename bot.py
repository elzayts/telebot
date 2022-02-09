
import logging
import typing
import json
from template_engine import TemplateEngine


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

engine = None
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Hello world')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('This bot was created to make phatic dialogue')


def echo(update, context):
    users_message=update.message.text
    update.message.reply_text(find_answer(users_message))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def find_answer(engine, user_message):
    return engine.process_question(user_message)

def get_patterns():
    with open('patterns.json') as file:
        data = json.load(file)

    templates = []

    for patterns in data:
        for answer in patterns["answers"]:
            templates.append(tuple(patterns["pattern"], answer))
    
    return templates

def main():
    updater = Updater("5178687337:AAHxxFeBLsYRMOpBDwsDZZ58HaH2Pyo7p3I", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    global engine
    engine = TemplateEngine(get_patterns())

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()