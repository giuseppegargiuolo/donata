import requests
import lxml.html
import traceback
from core.utils import Utils
from core.log import Log

from services.page_service import PageService
from database.models.page import Page

class Parser:

    def __init__(self, url, database):
        self.log = Log.getInstance()

        self.page = None
        self.pages = []

        self.ad = None
        self.ads = []
        
        self.apartment = None
        self.apartments = []

        self.utils = Utils()
        self.domain = self.utils.toDomain(url)
        self.moduleName = self.utils.toModule(url)
        self.className = self.utils.toClassName(url)
        self.baseWeb = self.utils.toBaseWeb(url)
        self.db = database

    def wget(self, url):
        self.parser = None

        try:
            headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36" }
            self.url = self.utils.toNormalizedUrl(self.baseWeb, url)
            page = requests.get(self.url, headers=headers)
            self.parser = lxml.html.fromstring(page.content)
        except Exception as ex:
            self.log.error('Error while parsing url ' + url or self.url, ex)

        return self.parser

    def xPath(self, path, element=None, pos=0, dataType=None, explode=None):
        try:
            if element is None:
                element = self.parser
            
            result = element.xpath(path)

            if isinstance(result, list) == False or dataType == 'LIST':
                return result
            if isinstance(result, list) == False or dataType == 'LISTURL':
                normalizedResult = []
                for url in result:
                    normalizedResult.append(self.utils.toNormalizedUrl(self.baseWeb, url))

                return normalizedResult
            else:
                if not result is None and len(result) > pos:
                    el = result[pos]
                    if dataType == 'MONEY' or dataType == 'NUMBER':
                        el = self.utils.toMoney(el)
                    if dataType == 'CHAR':
                        el = self.utils.toChar(el)
                    if dataType == 'URL':
                        el = self.utils.toNormalizedUrl(self.baseWeb, el)

                    if explode is not None:
                        separator, index = explode.split(',', 1)
                        separator = separator.replace('"', '', 9999)
                        index = int(index.strip())
                        return el.split(separator)[index]

                    return el
                else:
                    return None
        except:
            return None

    def getNextPage(self, page):
        pageService = PageService(self.db)        

        self.wget(page.url)
        nextPage = self.onGetNextPage(page.url)

        if nextPage is not None:
            page.number = page.number + 1
            self.page = pageService.generateCurrentPage(nextPage, page.number, page.publisherId)
            pageService.save(self.page)
        else:
            self.page = nextPage

        return self.page

    def onGetNextPage(self, url):
        return ''

    def getAds(self, page):
        count = 0

        self.wget(page)

        self.ads.clear()
        self.ads = self.onGetAds(page)

        self.apartments.clear()
        for ad in self.ads:
            try:
                count = count + 1
                self.apartment = self.getAd(page, ad)
                self.apartments.append(self.apartment)
            except Exception as ex:
                self.log.error('Error occured on page ' + page + ', url ' + self.apartment.url, ex)
                self.log.error(traceback.format_exc())

        return self.apartments

    def onGetAds(self, page):
        return []

    def getAd(self, page, ad):
        self.apartment = self.onGetAd(page, ad)
        return self.apartment
    
    def onGetAd(self, page, ad):
        return ''
    
    def getApartment(self, apartment):
        self.wget(apartment.url)

        self.apartment = self.onGetApartment(apartment)
        return self.apartment

    def onGetApartment(self, apartment):
        return ''