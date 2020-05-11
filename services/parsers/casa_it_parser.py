from core.parser import Parser
from database.models.apartment import Apartment

# Vendita: https://www.casa.it/vendita/residenziale/bologna/
# Affitto: https://www.casa.it/affitto/residenziale/bologna/
class CasaItParser(Parser):
    
    def onGetNextPage(self, url):
        return self.xPath(dataType='URL', path='//a[@class="nextPage"]/@href')

    def onGetAds(self, page):
        xpath = [
            '//article[@class="srp-card gold null"]',
            '//article[@class="srp-card platinum null"]',
            '//article[@class="srp-card silver null"]',
            '//article[@class="srp-card bronze null"]',
            '//article[@class="srp-card standard null"]',
        ]
        return self.xPath(path='|'.join(xpath), dataType='LIST')

    def onGetAd(self, page, ad):
        return Apartment(
            title = self.xPath(element=ad, dataType='CHAR', path='.//p[@class="casaAdTitle"]/a/text()'),
            subtitle = self.xPath(element=ad, dataType='CHAR', path='.//div[@class="address"]/p[2]/text()'),
            rooms = self.xPath(element=ad, dataType='NUMBER', path='.//span[text()="locali"]/parent::li/text()'),
            surface = self.xPath(element=ad, dataType='NUMBER', path='.//span[text()="mq"]/parent::li/text()'),
            price = self.xPath(element=ad, pos=1, dataType='MONEY', path='.//div[@class="features"]/p/text()'),
            url = self.xPath(element=ad, dataType='URL', path='.//p[@class="casaAdTitle"]/a/@href')
        )

    def onGetApartment(self, apartment):
        apartment.refNo = self.xPath(dataType='CHAR', path='.//li[text()="Riferimento Imm: "]/parent::li/b/text()', explode='" (", 0')
        return apartment