import logging
from datetime import datetime

from core.config import Config

class Log:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Log.__instance == None:
            Log()
        return Log.__instance 

    def __init__(self):
        terminal = Config().get('log')['terminal']
        """ Virtually private constructor. """
        if Log.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Log.__instance = self
            filename = datetime.now().strftime("%Y%m%d%H%M%S")
            logging.basicConfig(filename='logs/' + filename + '.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger('apartments')
            self.terminal = terminal

    def info(self, message):
        logging.info(message)
        self.onTerminal(message)

    def warning(self, message):
        self.logger.info(message)
        self.onTerminal(message)

    def error(self, message, ex=None):
        self.logger.error(message)
        self.logger.error(str(ex))
        self.onTerminal(message)
        self.onTerminal(str(ex))
    
    def onTerminal(self, message):
        if self.terminal == True:
            print(message)