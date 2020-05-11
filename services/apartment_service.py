from datetime import datetime
import uuid

from database.models.apartment import Apartment
from database.models.match import Match

from core.services.service import Service
from database.database import ApartmentsDatabase
# from services.bot_service import BotService

class ApartmentService(Service):

    def matches(self, apartment, restriction):
        isPrice = apartment.price is not None and (int(apartment.price) <= int(restriction.maxPrice))
        isSurface = apartment.surface is not None and (apartment.surface is not None and int(apartment.surface) >= int(restriction.minSurface))
        isApartment = apartment.title is not None and (apartment.title is not None and not apartment.title.lower().startswith('box') and not apartment.title.lower().startswith('garage') and not apartment.title.strip().lower().startswith('magazzino') and not apartment.title.strip().lower().startswith('capannone') and not apartment.title.strip().lower().startswith('ufficio') and not apartment.title.lower().startswith('mansarda') and not apartment.title.lower().startswith('negozio') and not apartment.title.lower().startswith('terratetto') and not apartment.title.lower().startswith('rustico') and not apartment.title.lower().startswith('casale') and not apartment.title.lower().startswith('cascina') and not apartment.title.lower().startswith('alimentari') and not apartment.title.lower().startswith('tabaccheria'))
        isBareOwnership = apartment.title is not None and apartment.description is not None and (apartment.title.strip().lower().find('nuda propriet') > -1 or apartment.description.strip().lower().find('nuda propriet') > -1)

        return isPrice and isSurface and isApartment and not isBareOwnership

    def exists(self, apartment):
        if apartment.refNo is not None:
            return self.db.apartments.exists(apartment, 'refNo')
        else:
            return self.db.apartments.exists(apartment, 'url')

    def wasMatch(self, apartment, subscription):
        return self.db.matches.wasMatch(apartment, subscription)
    
    def all(self):
        return self.db.apartments.all()
        
    def save(self, apartment, db=None):
        if db is None:
            self.db.apartments.save(apartment)
        if db is not None:
            db.apartments.save(apartment)

    def saveMatch(self, subscription, run, apartment):        
        match = Match()
        match.subscriptionId = subscription.id
        match.runId = run.id
        match.apartmentId = apartment.id

        self.db.matches.save(match)

    def getLabel(self, name):
        name = name[1:-1]
        return self.db.labels.get(name)

    def isMatching(self, apartment):
        return self.db.users.matchesForUsers(apartment)

    def placeMatches(self, apartment, run, db):
        batchId = str(uuid.uuid1())

        db.matches.addBatch(batchId)
        db.commit()

        db.apartments.placeMatches(apartment, run, batchId)


    def notifyPendingMatches(self, db):
        users = db.matches.pendingMatches()
        
        # bot = BotService(self.db)
        # bot.push(users)

    def getPendingMatches(self):
        users = db.matches.pendingMatches()