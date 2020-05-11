from telegram.ext import Updater, CommandHandler
import requests
import re

from services.user_service import UserService

from core.services.service import Service

class NotifierService(Service):

  def __init__(self):
    self.bot_token = '773143459:AAE8U-L2wvTvkmwj4P7zzjDBEpNezcGsrs4'
    self.updater = Updater(self.bot_token, use_context=True)
    self.dp = self.updater.dispatcher
    # self.pollMessages()    
    # self.updater.start_polling()

    Service.__init__(self, database)
    # updater.idle()

  def pollMessages(self):
    self.dp.add_handler(CommandHandler('me', self.me))

  def me(self, update, context):
    chatId = update.message.chat_id
    update.message.reply_text('You registration ID is ' + str(chatId))

  def push(self, user, message):
    if user is not None and user.telegram is not None:
      self.updater.bot.sendMessage(chat_id=user.telegram, text=message)
