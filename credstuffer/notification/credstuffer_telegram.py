import logging
from telegram.ext import Updater, CommandHandler
from telegram.bot import Bot
from telegram.parsemode import ParseMode


class CredstufferTelegram:
    """ class Telegram to send telegram messages

    USAGE:
            telegram = CredstufferTelegram()
            telegram.new_msg()

    """
    def __init__(self, token):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('Create class CredstufferTelegram')

        self.token = token
        self.updater = Updater(token=self.token)
        self.dp = self.updater.dispatcher

        self.bot = Bot(token=self.token)

        self.credstuffer_chat_id = 755923632

    def run(self):
        """ runs the telegram updater

        """
        self.updater.start_polling()
        self.updater.idle()

    def add_handler(self, command, handler):
        """ add a handler function to the dispatcher

        :param command: command msg
        :param handler: handler function to execute
        """
        self.dp.add_handler(handler=CommandHandler(command=command, callback=handler))

    def new_msg(self, text):
        """ new text message for the bot

        """
        self.logger.info("Send new message to credstuffer chat: {}".format(text))
        self.bot.sendMessage(chat_id=self.credstuffer_chat_id, text=text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    tele = CredstufferTelegram(token="")
    tele.run()
