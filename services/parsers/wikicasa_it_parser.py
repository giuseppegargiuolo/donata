from core.parser import Parser
from database.models.apartment import Apartment

# Vendita: https://www.wikicasa.it/vendita-case/bologna/
# Affitto: https://www.wikicasa.it/affitto-case/bologna/
class WikicasaItParser(Parser):
    
    def onGetNextPage(self, url):
        return self.xPath(dataType='URL', path='//a[@aria-label="Next"]/@href')

    def onGetAds(self, page):
        return self.xPath('//ul[@id="list-properties"]/li/article', dataType='LIST')

    def onGetAd(self, page, ad):
        return Apartment(
            title = self.xPath(element=ad, dataType='CHAR', path='.//a[@class="title-link"]/text()'),
            subtitle = self.xPath(element=ad, dataType='CHAR', path='.//p[@class="f-12 text-uppercase mb-5"]/text()'),
            description = self.xPath(element=ad, dataType='CHAR', path='.//p[contains(@class, "description")]/text()'),
            rooms = self.xPath(element=ad, dataType='NUMBER', path='.//span[contains(text(), "Local")]/preceding-sibling::span/text()'),
            surface = self.xPath(element=ad, dataType='NUMBER', path='.//sup/parent::span/preceding-sibling::span/text()'),
            price = self.xPath(element=ad, pos=1, dataType='MONEY', path='.//span[@class="price"]/text()'),
            url = self.xPath(element=ad, dataType='URL', path='.//a[@class="title-link"]/@href')
        )

    def onGetApartment(self, apartment):
        return apartment