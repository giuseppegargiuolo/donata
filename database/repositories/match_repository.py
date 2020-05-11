from core.database.repository import Repository

from database.models.apartment import Apartment
from database.models.batch import Batch
from database.models.match import Match
from database.models.subscription import Subscription
from database.models.user import User

from sqlalchemy.dialects import mysql

class MatchRepository(Repository):

    def all(self):
        return self.session.query(Match).all()

    def wasMatch(self, apartment, subscription):
        match = self.session.query(Match).filter(Match.apartmentId == apartment.id).filter(Match.subscriptionId == subscription.id).first()
        
        if match is None: # this match is found for the first time
            return False
        else:
            return True

        # return self.session.query(Match).filter(Match.subscriptionId == subscription.id).filter(Match.apartmentId == apartment.id).count() > 0

    def getAllByUser(self, subscription):
        return self.session.query(Match).join(Apartment).join(User).filter(Match.apartmentId == Apartment.id).filter(Match.subscriptionId == Subscription.id).filter(User.id == user.id).all()

    def pendingMatches(self):
        return self.session.query(Batch).join(Match).join(Subscription).join(User).filter(Batch.isProcessed == False).filter(Batch.isLocked == False).first()

    def addBatch(self, batchId):
        batch = Batch()
        batch.id = batchId

        self.save(batch)
        self.session.commit()