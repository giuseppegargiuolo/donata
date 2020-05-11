import importlib
import hashlib

class Utils:

    def instantiate(self, moduleName, className):
        module = importlib.import_module(moduleName)
        class_ = getattr(module, className)
        return class_()

    def toDomain(self, url):
        if url.find('www') != -1:
            start = url.index('.') + 1
        else:
            start = url.index('//') + 2
        end = url[start:].index('/')
        return url[start:start+end]

    def toModule(self, url):
        domain = self.toDomain(url)
        return domain.replace('.', '_')

    def toClassName(self, url):
        domain = self.toDomain(url)
        classNames = domain.split('.')
        return classNames[0].capitalize() + classNames[1].capitalize()

    def toBaseWeb(self, url):
        end = url.find('www.')
        pos = 4

        if end == -1:
            end = url.find('//')
            pos = 2


        http = url[:end + pos]
        return http + self.toDomain(url)

    def toNormalizedUrl(self, baseWeb, url):
        if url.find(baseWeb) == -1:
            if url.startswith('/') == True:
                url = baseWeb + url
            else:
                url = baseWeb + '/' + url
        return url

    def toMoney(self, value):
        if value is None:
            return None
        else:
            return ''.join(i for i in value if i.isdigit())

    def toChar(self, value):
        if value is None:
            return None
        else:
            return value.strip()

    def toHash(self, value):        
        return hashlib.md5(value.encode('utf8')).hexdigest()