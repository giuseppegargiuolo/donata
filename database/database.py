from core.database.base import Base
from core.database.database import Database

# repositories
from database.repositories.apartment_repository import ApartmentRepository
from database.repositories.batch_repository import BatchRepository
from database.repositories.city_repository import CityRepository
from database.repositories.group_repository import GroupRepository
from database.repositories.label_repository import LabelRepository
from database.repositories.match_repository import MatchRepository
from database.repositories.page_repository import PageRepository
from database.repositories.parameter_repository import ParameterRepository
from database.repositories.publisher_repository import PublisherRepository
from database.repositories.restriction_repository import RestrictionRepository
from database.repositories.run_repository import RunRepository
from database.repositories.subscription_repository import SubscriptionRepository
from database.repositories.user_repository import UserRepository

# models
from database.models.apartment import Apartment
from database.models.batch import Batch
from database.models.city import City
from database.models.group import Group
from database.models.label import Label
from database.models.match import Match
from database.models.page import Page
from database.models.publisher import Publisher
from database.models.restriction import Restriction
from database.models.run import Run
from database.models.subscription import Subscription
from database.models.user import User

class ApartmentsDatabase(Database):
    def __init__(self):
        Database.__init__(self)

        self.apartments = ApartmentRepository(self.engine, self.session)
        self.batches = BatchRepository(self.engine, self.session)
        self.cities = CityRepository(self.engine, self.session)
        self.groups = GroupRepository(self.engine, self.session)
        self.labels = LabelRepository(self.engine, self.session)
        self.matches = MatchRepository(self.engine, self.session)
        self.pages = PageRepository(self.engine, self.session)
        self.parameters = ParameterRepository(self.engine, self.session)
        self.restrictions = RestrictionRepository(self.engine, self.session)
        self.runs = RunRepository(self.engine, self.session)
        self.subscriptions = SubscriptionRepository(self.engine, self.session)
        self.publishers = PublisherRepository(self.engine, self.session)
        self.users = UserRepository(self.engine, self.session)