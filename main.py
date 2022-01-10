# coding = utf-8
from case.api_test import CommonTestCase
from config.excel_reader import ExcelReader


if __name__ == '__main__':
    app = CommonTestCase()
    reader = ExcelReader()
    models = reader.reader('Sheet1')
    app.runAllcase('Sheet1',models)