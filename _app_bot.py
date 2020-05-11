from database.database import ApartmentsDatabase
from services.bot_service import BotService

def main():
    database = ApartmentsDatabase()
    bot = BotService(database)
    bot.main(database)

### Main ###########################
if __name__ == '__main__':
    main()