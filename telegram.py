from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class KatchaYakisoba():
    logger = logging.getLogger(__name__)

    START, VALIDADOR_START = range(2)

    def validador_start(self, bot, update):

        msg = update.message.text
        user = update.message.from_user.first_name

        type_ = self.type_msg(update.message.entities)

        if type_ == "url":
            mensagem = "{} \n{}".format(msg, user)

            links_postados = open("links.txt", "r").read()
            links_postados = links_postados.split()
            twitter = "https://twitter.com/KatchaYakisoba"

            for verificar_site in links_postados:
                if msg == verificar_site:
                    text = "Link ja foi postado, consulte em " + twitter
                    bot.sendMessage(update.message.chat_id,
                                    text=text,
                                    one_time_keyboard=True)
                    return self.cancel(bot, update)

            links_postados.append(msg)
            links_postados = " ".join(links_postados)
            salvar_links_postados_handler = open("links.txt", "w")
            salvar_links_postados_handler.write(links_postados)
            self.enviar_twitter(mensagem)

            text = "Link salvo com sucesso, consulte em " + twitter
            bot.sendMessage(update.message.chat_id,
                            text=text,
                            one_time_keyboard=True)

            return self.cancel(bot, update)

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
