from core.services.service import Service
from database.models.page import Page

class PageService(Service):

    def save(self, page):
        self.db.pages.save(page)
        self.db.commit()

    def getByUrl(self, url):
        return self.db.pages.getbyUrl(url)

    def generateCurrentPage(self, pageUrl, pageNo, publisherId):
        page = Page()
        page.id = self.utils.toHash(str(pageNo) + str(publisherId))
        page.number = pageNo
        page.url = pageUrl
        page.publisherId = publisherId

        return page