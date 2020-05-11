from openpyxl import Workbook

class ExcelService:

    def __init__(self):
        pass

    def open(self, file)
        self.workbook = xlsxwriter.Workbook(file)

    def getSheets(self):
        pass

    def write(self):
        self.worksheet.write('A1', 'Hello world')

    def close(self):
        self.workbook.close()