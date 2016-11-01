
from telegram.ext import(Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Katcha_Yakisoba():
    logger = logging.getLogger(__name__)

    START,VALIDADOR_START  = range(2)



    def validador_start(self,bot, update):

        msg = update.message.text
        user = update.message.from_user.first_name

        type = self.type_msg(update.message.entities)


        if type == "url":
            mensagem = """{} \n{}""".format(msg,user)

            links_postados = open("links.txt", "r").read()
            links_postados = links_postados.split()

            for verificar_site in links_postados:
                if msg == verificar_site:
                    bot.sendMessage(update.message.chat_id,
                                text="""Link ja foi postado, consulte em https://twitter.com/KatchaYakisoba""",
                                    one_time_keyboard=True)
                    return self.cancel(bot,update)
            links_postados.append(msg)
            links_postados = " ".join(links_postados)
            salvar_links_postados = open("links.txt","w").write(links_postados)
            self.enviar_twitter(mensagem)
            bot.sendMessage(update.message.chat_id,

                            text="""Link salvo com sucesso, consulte em https://twitter.com/KatchaYakisoba""",
                            one_time_keyboard=True)

            return self.cancel(bot,update)




    def start(self,bot, update):




        bot.sendMessage(update.message.chat_id,

                        text="""envie o link""",
                         one_time_keyboard=True)

        return self.VALIDADOR_START



    def cancel(self,bot, update):
        user = update.message.from_user



        return ConversationHandler.END


    def error(self,bot, update, error):
        self.logger.warn('Update "%s" caused error "%s"' % (update, error))


    def __init__(self):
        # Create the EventHandler and pass it your bot's token.
        updater = Updater("codigodobot")

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('link', self.start)],

            states={
                self.START: [MessageHandler([Filters.text], self.start)],
                self.VALIDADOR_START: [MessageHandler([Filters.text], self.validador_start)],

            },

            fallbacks=[CommandHandler('xau', self.cancel)]
        )

        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    def type_msg(self,type):
        for i in type:
            type = i
        try:
            type = type["type"]
        except:
            pass
        return type

    def enviar_twitter(self,msg):
        from twython import Twython

        APP_KEY = "APP_KEY"
        APP_SECRET = "APP_SECRET"
        OAUTH_TOKEN = "OAUTH_TOKEN "
        OAUTH_TOKEN_SECRET = "OAUTH_TOKEN_SECRET"

        twitter = Twython(APP_KEY, APP_SECRET,
                          OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        twitter.update_status(status=msg)




if __name__ == '__main__':
    Katcha_Yakisoba()


























"""
    reply_keyboard = [['SANGRIA', 'FINANCEIRO']]

        bot.sendMessage(update.message.chat_id,

                        text="Link salvo com sucesso!",
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return self.VALIDADOR_START

    def gender(self,bot, update):
        user = update.message.from_user
        self.logger.info("Gender of %s: %s" % (user.first_name, update.message.text))
        bot.sendMessage(update.message.chat_id,
                        text='I see! Please send me a photo of yourself, '
                             'so I know what you look like, or send /skip if you don\'t want to.')

return 0"""