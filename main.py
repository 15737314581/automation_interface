# coding = utf-8
from case.api_test import CommonTestCase
from config.excel_reader import ExcelReader
from config.readconfig_yaml import ReadConfigYaml

if __name__ == '__main__':
    config_yaml = ReadConfigYaml()
    # 读取此次需要执行的用例sheet名称
    case_name = config_yaml.get_db('Excel-Config', 'case_name')
    app = CommonTestCase()
    reader = ExcelReader()
    # 加载全部用例models
    models = reader.reader(case_name)
    # 执行全部用例
    app.runAllcase(case_name,models)