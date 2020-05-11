import importlib
import sys
import traceback

from core.services.service import Service
from services.apartment_service import ApartmentService
from services.bot_service import BotService
from services.page_service import PageService
from services.run_service import RunService
from services.user_service import UserService

from database.database import ApartmentsDatabase

class ParserService(Service):

    def run(self, publisher, executor):
        self.userService = UserService(self.db)

        users = self.userService.anyUsersOnCityLabel(publisher.city, publisher.label)
        
        if users is None or len(users) == 0:
            return

        self.pageService = PageService(self.db)
        self.runService = RunService(self.db)
        self.apartmentService = ApartmentService(self.db)
        self.telegram = BotService(self.db)

        # users = self.userService.getUsers(publisher.city)
        run = self.runService.getCurrent()

        parser = self.getParser(publisher.url)

        # save first page
        pageNo = 1
        page = self.pageService.generateCurrentPage(publisher.url, pageNo, publisher.id)
        self.pageService.save(page)

        while page is not None and page.url is not None:

            try:            
                self.log.info('Parsing page at url ' + page.url)
                apartments = parser.getAds(page.url)

                for apartment in apartments:
                    try:
                        self.log.info('  Parsing apartment at ' + apartment.url)                    
                        apartment.runId = run.id
                        apartment.id = self.utils.toHash(apartment.url)
                        apartment.pageId = page.id                    

                        # self.findMatches(publisher, apartment, users, run)
                        executor.submit(self.findMatches, apartment, run)
                    except Exception as e:
                        self.db.rollback()
                        self.log.error('Error occured while scraping apartment at ' + apartment.url, e)
                        traceback.print_exc()

                # get and save next page
                page = parser.getNextPage(page)
            
            except Exception as ex:
                self.log.error('Error occured while scraping apartment at ' + page.url, ex)

    def getParser(self, url):
        # return self.utils.instantiate('services.parsers.' + self.utils.toModule(url) + '_parser', self.utils.toClassName(url) + 'Parser')

        moduleName = self.utils.toModule(url)
        className = self.utils.toClassName(url)

        module = importlib.import_module('services.parsers.' + moduleName + '_parser')
        class_ = getattr(module, className + 'Parser')
        return class_(url, self.db)

    def getPublishers(self):
        links = []
        publishers = self.db.publishers.all()

        for publisher in publishers:
            if publisher.url is not None and publisher.url != '' and publisher.isActive == True:
                links.append(publisher)

        return links

    def findMatches(self, apartment, run):
        db = ApartmentsDatabase()

        self.apartmentService.save(apartment, db)
        db.commit()

        self.apartmentService.placeMatches(apartment, run, db)

    '''
    def findMatches(self, publisher, apartment, users, run):
        for user in users:
            userName = user.name if hasattr(user, 'name') and user.name is not None else ''
            userSurname = user.surname if hasattr(user, 'surname') and user.surname is not None else ''
            for subscription in user.subscriptions:

                # is the current user subscribed the the current url?
                if subscription.labelId != publisher.labelId or subscription.cityId != publisher.cityId:
                    continue

                self.apartmentService.save(apartment)

                if self.apartmentService.matches(apartment, subscription.restrictions):
                    
                    # apartment matches the user restrictions                                    
                    # TODO: apartment = parser.getApartment(apartment)
                    if self.apartmentService.matches(apartment, subscription.restrictions):
                        isMatch = self.apartmentService.wasMatch(apartment, subscription)
                        
                        if isMatch == False:
                            self.log.info('  Found apartment + match at ' + apartment.url + ' for user ' + userName + ' ' + userSurname)
                            self.apartmentService.save(apartment)
                            self.apartmentService.saveMatch(subscription, run, apartment)
                            self.telegram.push(user, apartment.url)

        self.db.commit()
    '''