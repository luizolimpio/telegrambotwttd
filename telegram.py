import hashlib
import os
import logging

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class KatchaYakisoba():
    logger = logging.getLogger(__name__)

    START, VALIDADOR_START = range(2)
    LINKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'links')

    def validador_start(self, bot, update):

        msg = update.message.text
        user = update.message.from_user.first_name
        type_ = self.type_msg(update.message.entities)

        if type_ == "url":
            mensagem = "{} \n{}".format(msg, user)
            twitter = "https://twitter.com/KatchaYakisoba"
            hash = hashlib.md5(msg.encode())

            # abort if link was already posted
            if self.link_exists(hash):
                text = "Link ja foi postado, consulte em " + twitter
                bot.sendMessage(update.message.chat_id,
                                text=text,
                                one_time_keyboard=True)
                return self.cancel(bot, update)

            self.create_link_file(hash)
            self.enviar_twitter(mensagem)

            text = "Link salvo com sucesso, consulte em " + twitter
            bot.sendMessage(update.message.chat_id,
                            text=text,
                            one_time_keyboard=True)

            return self.cancel(bot, update)

    def link_file(self, hash):
        """Gets URL (str) or hash obj. and return the path to the file."""
        if isinstance(str, hash):
            hash = hashlib.md5(hash.encode())
        return os.path.join(self.LINKS, hash.hexdigest())

    def link_exists(self, hash):
        """Gets URL (str) or hash obj. and return a boolean."""
        if isinstance(str, hash):
            hash = hashlib.md5(hash.encode())
        return os.path.exists(self.link_file(hash))

    def create_link_file(self, hash):
        """Gets URL (str) or hash obj. and creates a file (returns boolean)."""
        if isinstance(str, hash):
            hash = hashlib.md5(hash.encode())

        if not self.link_exists(hash):
            open(self.link_file(hash), 'a').close()
            return True

        return False

    def start(self, bot, update):
        bot.sendMessage(update.message.chat_id,
                        text="envie o link",
                        one_time_keyboard=True)
        return self.VALIDADOR_START

    def cancel(self, bot, update):
        update.message.from_user
        return ConversationHandler.END

    def error(self, bot, update, error):
        self.logger.warn('Update "%s" caused error "%s"' % (update, error))

    def __init__(self):

        # create directory to store link files
        if not os.path.exists(self.LINKS):
            os.makedirs(self.LINKS)

        # Backward compatibility with links.txt
        if os.path.exists('links.txt'):
            for link in open('links.txt', 'r').read().split():
                self.create_link_file(link)

        # Create the EventHandler and pass it your bot's token.
        updater = Updater("codigodobot")

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Add conversation handler w/ the states GENDER, PHOTO, LOCATION & BIO
        validator = [MessageHandler([Filters.text], self.validador_start)]
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('link', self.start)],
            states={
                self.START: [MessageHandler([Filters.text], self.start)],
                self.VALIDADOR_START: validator,

            },
            fallbacks=[CommandHandler('xau', self.cancel)]
        )

        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives
        # SIGINT, SIGTERM or SIGABRT. This should be used most of the time,
        # since start_polling() is non-blocking and will stop the bot
        # gracefully.
        updater.idle()

    def type_msg(self, type_):
        for i in type_:
            type_ = i
        try:
            type_ = type_["type"]
        except:
            pass
        return type_

    def enviar_twitter(self, msg):
        from twython import Twython

        app_key = "APP_KEY"
        app_secret = "APP_SECRET"
        oauth_token = "OAUTH_TOKEN "
        oauth_token_secret = "OAUTH_TOKEN_SECRET"

        twitter = Twython(app_key, app_secret,
                          oauth_token, oauth_token_secret)

        twitter.update_status(status=msg)


if __name__ == '__main__':
    KatchaYakisoba()

"""
reply_keyboard = [['SANGRIA', 'FINANCEIRO']]

    bot.sendMessage(update.message.chat_id,

                    text="Link salvo com sucesso!",
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                     one_time_keyboard=True))

    return self.VALIDADOR_START

def gender(self,bot, update):
    user = update.message.from_user
    self.logger.info("Gender of %s: %s" % (user.first_name,
                                           update.message.text))
    text = "I see! Please send me a photo of yourself, so I know what you look
            like, or send /skip if you don\'t want to."
    bot.sendMessage(update.message.chat_id, text=text)
    return 0
"""