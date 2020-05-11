from core.database.repository import Repository
from database.models.match import Match
from database.models.apartment import Apartment
from database.models.page import Page
from database.models.user import User

class PageRepository(Repository):

    def getbyUrl(self, page):
        return self.session.query(Page).filter(Page.url == page).first()