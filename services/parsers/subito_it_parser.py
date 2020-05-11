from core.parser import Parser
from database.models.apartment import Apartment

# Vendita: https://www.subito.it/annunci-emilia-romagna/vendita/appartamenti/bologna/bologna/
# Affitto: https://www.subito.it/annunci-emilia-romagna/affitto/appartamenti/bologna/bologna/
class SubitoItParser(Parser):
    
    def onGetNextPage(self, url):
        return self.xPath(dataType='URL', path='//div[contains(@class, "pagination-container")]/a[last()]/@href')

    def onGetAds(self, page):
        return self.xPath(path='//div[contains(@class, "items__item")][a]', dataType='LIST')

    def onGetAd(self, page, ad):
        return Apartment(
            title = self.xPath(element=ad, dataType='CHAR', path='.//div[contains(@class, "upper-data-group")]/h2[contains(@class, "item-title")]/text()'),
            rooms = self.xPath(element=ad, dataType='NUMBER', path='.//p[contains(text(), " locali")]/text()'),
            surface = self.xPath(element=ad, dataType='NUMBER', path='.//p[contains(text(), " mq")]/text()'),
            price = self.xPath(element=ad, dataType='MONEY', path='.//div[contains(@class, "price")]/h6/text()'),
            url = self.xPath(element=ad, dataType='URL', path='.//a[contains(@class, "link")]/@href')
        )

    def onGetApartment(self, apartment):
        apartment.refNo = self.xPath(dataType='CHAR', path='.//li[text()="Riferimento Imm: "]/parent::li/b/text()', explode='" (", 0')
        return apartment