from core.parser import Parser
from database.models.apartment import Apartment

# Vendita: https://www.kijiji.it/case/vendita/annunci-bologna/
# Affitto: https://www.kijiji.it/case/affitto/annunci-bologna/
class KijijiItParser(Parser):
    
    def onGetNextPage(self, url):
        return self.xPath(dataType='URL', path='//nav[@class="pagination"]/a[@rel="next"]/@href')

    def onGetAds(self, page):
        return self.xPath(path='//ul[@id="search-result"]/li[@class="item result  gtm-search-result"]', dataType='LIST')

    def onGetAd(self, page, ad):
        return Apartment(
            title = self.xPath(element=ad, dataType='CHAR', path='.//h3[@class="title"]/a/text()'),
            description = self.xPath(element=ad, dataType='CHAR', path='.//p[contains(@class, "description")]/text()'),
            price = self.xPath(element=ad, dataType='MONEY', path='.//h4[@class="price"]/text()'),
            url = self.xPath(element=ad, dataType='CHAR', path='.//h3[@class="title"]/a/@href')
        )

    def onGetApartment(self, apartment):
        apartment.refNo = self.xPath(dataType='CHAR', path='.//li[text()="Riferimento Imm: "]/parent::li/b/text()', explode='" (", 0')
        return apartment