from core.database.repository import Repository
from database.models.subscription import Subscription

class SubscriptionRepository(Repository):

    def last(self):
        return self.session.query(Subscription).order_by(Subscription.id.desc()).first()

    def get(self, id):
        return self.session.query(Subscription).filter(Subscription.id == id).first()

    def getByUser(self, user):
        return self.session.query(Subscription).filter(Subscription.userId == user.id).first()