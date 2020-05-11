import traceback
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from core.log import Log
from services.run_service import RunService
from services.parser_service import ParserService
from database.database import Database
from database.database import ApartmentsDatabase

def main():
    #region Initialization
    log = Log.getInstance()
    database = ApartmentsDatabase()
    #endregion Initialization

    log.info('Scraping starts now...')
    runService = RunService(database)
    parserService = ParserService(database)

    try:
        with ProcessPoolExecutor(max_workers=10) as processor, ThreadPoolExecutor(max_workers=10) as threader:
            while 1 == 1:
                runService.connect()
                
                for publisher in parserService.getPublishers():
                    try:                    
                        parserService.run(publisher, threader)
                        # processor.submit(parserService.run, publisher.id)
                    except Exception as e:
                        log.error('Error while running', e)
                        log.error('Restarting in progress...')
                        traceback.print_exc()

                    time.sleep(2)

                runService.close()

    except Exception as ex:
        log.error('Unexpected error.', ex)
    except (KeyboardInterrupt, SystemExit):
        log.error('End.', exc)

    print('End.')

### Main ###########################
if __name__ == "__main__":
    main()