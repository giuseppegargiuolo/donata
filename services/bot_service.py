import logging
import apiai, json

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

from core.config import Config
from core.services.service import Service

from services.apartment_service import ApartmentService
from services.city_service import CityService
from services.label_service import LabelService
from services.parameter_service import ParameterService
from services.user_service import UserService

from database.database import ApartmentsDatabase

from database.models.group import Group
from database.models.label import Label
from database.models.restriction import Restriction
from database.models.subscription import Subscription
from database.models.user import User

class BotService(Service):
    
    MENU, FEEDBACK, GETFEEDBACK, UNSUBSCRIBE, EDITMODE, EDITCITY, EDITROOMS, EDITSURFACE, EDITPRICE = range(9)

    def __init__(self, database):
        Service.__init__(self, database)

        # Telegram initialization
        self.updater = Updater(self.config.get('telegram')['token'], use_context=True)

    def start(self, update, context):
        message = update.message
        user = message.from_user

        # we have the user. Let's register him in the database
        self.db = ApartmentsDatabase()

        userService = UserService(self.db)
        self.user = userService.get(user)

        if self.user is not None and bool(self.user.isActive) == True: # user is registered
            keyboard = [
                [ '-Modifica criteri di ricerca-' ],
                [ '-Statistiche-', '-Annulla iscrizione-' ],
            ]
            update.message.reply_text('...', reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
        else:
            keyboard = [
                [ '-Registrati-' ]
            ]
            update.message.reply_text('Premi sul tasto Registra e imposta i criteri di ricerca per la casa dei tuoi sogni. Se non vedi nessun menu, premi sul quadrato contenente i 4 piccoli cerchi', reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))

        return self.MENU

    def menu(self, update, context):
        message = update.message
        user = message.from_user

        self.log.info(user.full_name + ' selected ' + message.text)

        if message.text == '-Registrati-':
            return self.register(update, context)
        elif message.text == '-Feedback-':
            return self.feedback(update, context)
        elif message.text == '-Statistiche-':
            return self.statistics(update, context)
        elif message.text == '-Modifica criteri di ricerca-':
            return self.editCriteria(update, context)
        elif message.text == '-Annulla iscrizione-':
            return self.unsubscribe(update, context)
        else:
            return ConversationHandler.END

    def register(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)


        # we have the user. Let's register him in the database
        userService = UserService(self.db)
        subscriber = userService.get(user)

        response = self.isMaxSubscription(user)

        if subscriber is None:
            # region create user
            group = Group()
            group = self.db.groups.save(group)
            self.db.commit()

            subscriber = User()
            subscriber.name = user.first_name
            subscriber.surname = user.last_name
            subscriber.telegram = user.id
            subscriber.groupId = group.id
            subscriber.isActive = False
            subscriber.token = user.id
            subscriber = self.db.users.save(subscriber)
            self.db.commit()

            subscription = Subscription()
            subscription.userId = subscriber.id
            self.db.subscriptions.save(subscription)
            self.db.commit()
            #endregion create user

            if response == True:
                return ConversationHandler.END

            # let's choose the mode (Affitto|Acquisto)
            labelService = LabelService(self.db)
            labels = labelService.all()

            keyboard = [['-' + getattr(label, 'name') + '-'] for label in labels]

            # next question
            update.message.reply_text('Vuoi acquistare o prendere casa in affitto?', reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))

            return self.EDITMODE

        elif bool(subscriber.isActive) == False:
            if response == True:
                return ConversationHandler.END

            subscriber.isActive = True
            subscriber = self.db.users.save(subscriber)
            self.db.commit()

            subscription = self.user.subscriptions[0]

            # let's choose the mode (Affitto|Acquisto)
            labelService = LabelService(self.db)
            labels = labelService.all()

            keyboard = [['-' + getattr(label, 'name') + '-'] for label in labels]

            # next question
            update.message.reply_text('Vuoi acquistare o prendere casa in affitto?', reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))

            return self.EDITMODE

    def unsubscribe(self, update, context):
        message = update.message
        user = message.from_user
        
        if message.text == '/start':
            return self.start(update, context)

        # disable subscription
        userService = UserService(self.db)
        subscriber = userService.get(user)
        userService.unsubscribe(subscriber)

        # final confirmation
        update.message.reply_text('A presto! Ci dispiace vederti andare via.', reply_markup=ReplyKeyboardRemove())

        return self.start(update, context)

    def editCriteria(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        # let's choose the mode (Affitto|Acquisto)
        labelService = LabelService(self.db)
        labels = labelService.all()

        keyboard = [['-' + getattr(label, 'name') + '-'] for label in labels]

        # next question
        update.message.reply_text('Vuoi acquistare o prendere casa in affitto?', reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))

        return self.EDITMODE

    def editMode(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        self.log.info(user.full_name + ' selected city ' + message.text)

        # user selected the mode. Let's add it in the database
        apartmentService = ApartmentService(self.db)
        userService = UserService(self.db)

        subscriber = userService.get(user)

        if subscriber.subscriptions is not None and len(subscriber.subscriptions) > 0:
            subscription = subscriber.subscriptions[0]
        else:
            subscription = Subscription()

        subscription.labelId = apartmentService.getLabel(message.text).id
        subscription = self.db.subscriptions.save(subscription)
        self.db.commit()

        # next question
        # let's choose the city you want to rent|buy in
        cityService = CityService(self.db)
        cities = cityService.all()

        keyboard = [['-' + getattr(city, 'name') + '-'] for city in cities]
        update.message.reply_text('Bene! Adesso scegli la città in cui cerchi la tua nuova casa', reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
        
        return self.EDITCITY

    def editCity(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        # save the city
        userService = UserService(self.db)

        subscriber = userService.get(user)
        if subscriber.subscriptions is not None and len(subscriber.subscriptions) > 0:
            subscription = subscriber.subscriptions[0]
        else:
            subscription = Subscription()

        subscription.cityId = self.db.cities.getByName(message.text).id
        self.db.subscriptions.save(subscription)
        self.db.commit()

        self.log.info(user.full_name + ' selected ' + message.text + ' as a city')

        # next question
        update.message.reply_text('Quante stanze vuoi che la tua casa abbia di minimo (es. 3)? Scrivi 0 (zero) se è irrilevante', reply_markup=ReplyKeyboardRemove())

        return self.EDITROOMS

    def editRooms(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        userService = UserService(self.db)

        subscriber = userService.get(user)

        subscription = subscriber.subscriptions[0]
        if subscription.restrictionId is not None:
            restriction = self.db.restrictions.get(subscription.restrictionId)
        else:
            restriction = Restriction() 

        if not message.text.isdigit():
            update.message.reply_text('Puoi inserire solo numeri. Riprova: ')
            return self.EDITROOMS
        if message.text == '0':
            restriction.minRooms = None
        else:
            restriction.minRooms = message.text

        # edit rooms
        self.db.restrictions.save(restriction)
        self.db.commit()

        subscription.restrictionId = restriction.id
        self.db.subscriptions.save(subscription)
        self.db.commit()

        # next message
        update.message.reply_text('Quanti metri quadri minimo deve avere la tua nuova casa? Scrivi 0 (zero) se è irrilevante', reply_markup=ReplyKeyboardRemove())

        return self.EDITSURFACE

    def editSurface(self, update, context):
        message = update.message
        user = message.from_user

        userService = UserService(self.db)
        subscriber = userService.get(user)
        restriction = subscriber.subscriptions[0].restrictions

        if message.text == '/start':
            return self.start(update, context)

        if not message.text.isdigit():
            update.message.reply_text('Puoi inserire solo numeri. Riprova: ')
            return self.EDITSURFACE
        if message.text == '0':
            restriction.minSurface = None
        else:
            restriction.minSurface = message.text

        restriction.minSurface = message.text
        self.db.restrictions.save(restriction)
        self.db.commit()

        # next message
        update.message.reply_text('Qual è il prezzo massimo che saresti disposto a pagare per la tua nuova casa?', reply_markup=ReplyKeyboardRemove())

        return self.EDITPRICE

    def editPrice(self, update, context):
        message = update.message
        user = message.from_user

        userService = UserService(self.db)
        subscriber = userService.get(user)
        restriction = subscriber.subscriptions[0].restrictions

        if message.text == '/start':
            return self.start(update, context)

        if not message.text.isdigit():
            update.message.reply_text('Puoi inserire solo numeri. Riprova: ')
            return self.EDITPRICE
        if message.text == '0':
            restriction.maxPrice = None
        else:
            restriction.maxPrice = message.text

        self.db.restrictions.save(restriction)
        self.db.commit()

        subscriber.isActive = True
        self.db.users.save(subscriber)
        self.db.commit()

        # next message
        update.message.reply_text('Ho applicato i tuoi nuovi criteri di ricerca con successo', reply_markup=ReplyKeyboardRemove())

        return self.statistics(update, context)

    def feedback(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        # final confirmation
        update.message.reply_text('Cosa vuoi segnalarmi?', reply_markup=ReplyKeyboardRemove())

        return self.GETFEEDBACK

    def getFeedback(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        giuseppe = User()
        giuseppe.telegram = '644177311'

        # save feedback
        update.message.reply_text('Grazie ' + user.first_name + '. Il tuo feedback è importante. Ti forniremo una risposta al più presto.', reply_markup=ReplyKeyboardRemove())
        self.push(giuseppe, 'Messagggio da ' + user.name + ' (' + str(user.id) + '): ' + message.text)

        return self.start(update, context)

    def statistics(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        self.log.info('User ' + user.full_name + ' selected Statistiche')

        # self.db.users.close()
        # self.db = ApartmentsDatabase()
        userService = UserService(self.db)
        subscriber = userService.get(user)
        label = subscriber.subscriptions[0].label
        restriction = subscriber.subscriptions[0].restrictions
        city = subscriber.subscriptions[0].cities

        # message
        update.message.reply_text('​Sei registrato alla ricerca di un appartamento a ' + city.name + ' in ' + label.name.lower() + ' che abbia almeno ' + str(restriction.minRooms) + ' stanze, ' + str(restriction.minSurface) + ' mq e che costi un massimo di ' + str(restriction.maxPrice) + ' Euro', reply_markup=ReplyKeyboardRemove())

        self.pushMatches(subscriber)

        return self.start(update, context)

    def pushMatches(self, user):
        self.apartmentService.save(apartment)
        self.db.commit()
        self.apartmentService.placeMatches(apartment, run)

    def cancel(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        self.log.info('User ' + user.full_name + ' canceled the conversation.')

        # message
        update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())

        return self.start(update, context)

    def help(self, update, context):
        message = update.message
        user = message.from_user

        if message.text == '/start':
            return self.start(update, context)

        self.log.info('User ' + user.full_name + ' asked help')

        update.message.reply_text('Ciao ' + user.first_name + ', scrivi /start per cominciare e benvenuto! Se dovessi non ricevere risposte, scrivi /start per ricominciare', reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def textMessage(self, update, context):
        request = apiai.ApiAI(self.config.get('dialogflow')['token']).text_request() # Dialogflow API Token
        request.lang = self.config.get('dialogflow')['language'] # Request language
        request.session_id = self.config.get('dialogflow')['name'] # ID dialog session (for bot training)
        request.query = update.effective_message.text # Send request to AI II with the user message
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech'] # Take JSON answer
        if response:
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Si è verificato un errore inaspettato. Scrivi /start per ricominciare. Mi scuso per l\'inconveniente')
            self.log.error(context)

    def error(self, update, context):
        """Log Errors caused by Updates.""" 

        message = update.message
        user = message.from_user    
        
        self.log.warning('Update ' + update + ' caused error ' + context.error)

        update.message.reply_text('Si è verificato un errore inaspettato. Scrivi /start per ricominciare. Mi scuso per l\'inconveniente', reply_markup=ReplyKeyboardRemove())

    def push(self, recipients, message):
        users = []
        if not isinstance(recipients, list):
            users.append(recipients)
        else:
            users = recipients

        for user in users:
            if user is not None and hasattr(user, 'telegram') and user.telegram is not None:
                try:
                    self.updater.bot.sendMessage(chat_id=user.telegram, text=message)
                except Exception as e:
                    self.log.error(str(e))
            
            if user is not None and hasattr(user, 'first_name'):
                try:
                    self.updater.bot.sendMessage(chat_id=user.id, text=message)
                except Exception as e:
                    self.log.error(str(e))

    def isMaxSubscription(self, user):
        parameters = ParameterService(self.db)
        MAX_LIMIT_SUBSCRIPTIONS = parameters.get('MAX_LIMIT_SUBSCRIPTIONS', 999999)

        userService = UserService(self.db)
        allUsers = userService.getUsers()

        if len(allUsers) >= int(MAX_LIMIT_SUBSCRIPTIONS):
            self.push(user, 'Mi dispiace ' + user.first_name + ', è stato raggiunto il numero massimo di iscrizioni per questa finestra di registrazioni. Ti invierò un messaggio alla prossima finestra. Saluti, Donata')
            return True
        else:
            return False

    def main(self, database):
        cityService = CityService(self.db)
        cities = cityService.all()

        labelService = LabelService(self.db)
        labels = labelService.all()

        dispatcher = self.updater.dispatcher

        feedback_handler = ConversationHandler(
            entry_points = [
                CommandHandler('feedback', self.feedback)
            ],

            states = {
                self.FEEDBACK: [
                    MessageHandler(Filters.text, self.feedback)
                ],
                self.GETFEEDBACK: [
                    MessageHandler(Filters.text, self.getFeedback)
                ],
            },

            fallbacks = [
                CommandHandler('cancel', self.cancel)
            ]
        )

        conv_handler = ConversationHandler(
            entry_points = [
                CommandHandler('start', self.start)
            ],

            states = {
                self.MENU: [
                    MessageHandler(Filters.regex('^(-Registrati-|-Statistiche-|-Annulla iscrizione-|-Modifica criteri di ricerca-)$'), self.menu)
                ],
                self.UNSUBSCRIBE: [
                    MessageHandler(Filters.text, self.unsubscribe)
                ],
                self.EDITMODE: [
                    MessageHandler(Filters.regex('^(' + '|'.join('-' + getattr(label, 'name') + '-' for label in labels) + ')$'), self.editMode)
                ],
                self.EDITCITY: [
                    MessageHandler(Filters.regex('^(' + '|'.join('-' + getattr(city, 'name') + '-' for city in cities) + ')$'), self.editCity)
                ],
                self.EDITROOMS: [
                    MessageHandler(Filters.text, self.editRooms)
                ],
                self.EDITSURFACE: [
                    MessageHandler(Filters.text, self.editSurface)
                ],
                self.EDITPRICE: [
                    MessageHandler(Filters.text, self.editPrice)
                ]
            },

            fallbacks = [
                CommandHandler('cancel', self.cancel)
            ]
        )

        dispatcher.add_handler(conv_handler)
        dispatcher.add_handler(feedback_handler)
        dispatcher.add_handler(CommandHandler('help', self.help))        

        # log all errors
        dispatcher.add_error_handler(self.textMessage)

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()