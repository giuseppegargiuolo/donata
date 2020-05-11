from core.parser import Parser
from database.database import Apartment

# Vendita: https://www.immobiliare.it/vendita-case/bologna/
# Affitto: https://www.immobiliare.it/affitto-case/bologna/
class ImmobiliareItParser(Parser):
    
    def onGetNextPage(self, url):
        return self.xPath(dataType='URL', path='//ul[@class="pull-right pagination"]//a[@title="Pagina successiva"]/@href')

    def onGetAds(self, page):
        xpath = [
            '//ul[@class="annunci-list"]/li[contains(@class, "js-row-detail")]',
            # '//ul[@class="annunci-list"]//div[@class="properties__list"]//div[contains(@class, "properties__item js-more-row")]//p[@class="properties__typo"]'
        ]
        return self.xPath(path='|'.join(xpath), dataType='LIST')

    def onGetAd(self, page, ad):
        return Apartment(
            title = self.xPath(element=ad, dataType='CHAR', path='.//p[@class="titolo text-primary"]/a/text()'),
            subtitle = self.xPath(element=ad, dataType='CHAR', path='.//div[@class="descrizione__titolo"]/text()'),
            description = self.xPath(element=ad, dataType='CHAR', path='.//p[@class="descrizione__truncate"]/text()'),
            rooms = self.xPath(element=ad, dataType='NUMBER', path='.//div[text()="locali"]/preceding-sibling::div/span/text()'),
            surface = self.xPath(element=ad, dataType='NUMBER', path='.//div[text()="superficie"]/preceding-sibling::div/span/text()'),
            price = self.xPath(element=ad, dataType='MONEY', path='.//li[@class="lif__item lif__pricing"]/text()'),
            url = self.xPath(element=ad, dataType='URL', path='.//p[@class="titolo text-primary"]/a/@href')
        )

    def onGetApartment(self, apartment):
        apartment.refNo = self.xPath(dataType='CHAR', path='//dt[text()="Riferimento e Data annuncio"]/following-sibling::dd[1]/text()', explode='" ", 0')
        
        return apartment