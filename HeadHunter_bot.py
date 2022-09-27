
import logging
import hh_parser
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    Filters,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
)
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
KEY, DATE, FIN = range(3)

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""

    update.message.reply_text('*This is hh bot*', parse_mode='MarkdownV2', reply_markup=ReplyKeyboardRemove())
    """Starts the conversation and asks for key words"""

    update.message.reply_text('Please enter the keywords', reply_markup=ReplyKeyboardRemove())
    return KEY

def get_key_words(update: Update, context: CallbackContext) -> int:
    logger.info("keywords: %s", update.message.text)
    with open("/Users/Evgenia/Desktop/keywords.txt", 'w') as f:
        f.write(update.message.text + " ")
    reply_keyboard = [['1 week', '2 weeks', '1 day']]
    update.message.reply_text(
        'choose date range',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='date range:'
        ),
    )
    return FIN

def get_date_range(update: Update, context: CallbackContext) -> int:
    logger.info("Date range: %s", update.message.text)
    with open ("/Users/Evgenia/Desktop/date_range.txt", 'w') as f:
        f.write(update.message.text)
    vacancies = hh_parser.get_vacancies()
    print(type(vacancies))
    if len(vacancies) == 0:
        update.message.reply_text('no available vacancies', reply_markup=ReplyKeyboardRemove())
    else:
        for vacancy in range(len(vacancies)):
            update.message.reply_text(vacancies[vacancy],  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('If you want to continue, press /continue')
    return DATE

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5465440987:AAE63EpoRz6LQ-3gAMXyUdGhSHGka5DnjsA")
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states = {KEY: [MessageHandler(Filters.text & ~Filters.command, get_key_words)],
                  FIN: [MessageHandler(Filters.regex('^(1 week|2 weeks|1 day)$'), get_date_range)],
                  DATE: [MessageHandler(Filters.text & ~Filters.command, cancel)],
                  },
        fallbacks = [CommandHandler('cancel', cancel)],
        allow_reentry = True
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
