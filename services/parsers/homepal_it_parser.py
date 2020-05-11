from core.parser import Parser
from database.models.apartment import Apartment

# Vendita: https://homepal.it/privati/vendita/case/Bologna
# Affitto: https://homepal.it/privati/affitto/case/Bologna
class HomepalItParser(Parser):

    def onGetNextPage(self, url):
        return self.xPath(dataType='URL', path='//a[@class="pagingItem pagingSelectedItem"]/following-sibling::a/@href')
    
    def onGetAds(self, page):
        return self.xPath(path='//div[@class="ricercaFotoItemContainer risultati-ricerca-list"]/div[@class="annuncio-list-detail" and contains(@id, "ricercannuncio_")]', dataType='LIST')
    
    def onGetAd(self, page, ad):
        urlToken = self.xPath(element=ad, dataType='CHAR', path='.//img/parent::li/@onclick')
        starturl = urlToken.find('(\'')
        endurl = urlToken.find('\')')

        return Apartment(
            title = self.xPath(element=ad, dataType='CHAR', path='.//div[@class="body-descrizione"]/h4/text()'),
            subtitle = self.xPath(element=ad, dataType='CHAR', path='.//div[@class="body-descrizione"]/div[@class="ricercaListitemAddress"]/text()'),
            description = self.xPath(element=ad, dataType='CHAR', path='.//div[@class="body-descrizione"]/div[@class="ricercaListitemDesc hideResponsive"]/text()'),
            price = self.xPath(element=ad, dataType='MONEY', path='.//span[@class="priceSpan"]/text()'),
            rooms = self.xPath(element=ad, dataType='NUMBER', path='.//span[contains(text(), " Locali")]/span/text()'),
            surface = self.xPath(element=ad, dataType='NUMBER', path='.//span[contains(text(), " Mq")]/span/text()'),
            url = self.baseWeb + urlToken[starturl + 2 : endurl],
        )