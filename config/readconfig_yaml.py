# coding = utf-8
import yaml
import os


class ReadConfigYaml(object):
    """
    定义一个读取配置文件的类
    """

    def __init__(self, filepath=None):
        if filepath:
            self.read_path = filepath
        else:
            # 获取当前文件所在目录的上一级目录，即项目所在目录
            self.read_path = os.path.join(os.getcwd(), "./config.yaml")
        with open(self.read_path, 'r', encoding='utf-8') as f:
            self.content = yaml.load(f,Loader=yaml.FullLoader)

    def get_db(self, sections, param):
        value = self.content[sections][param]
        return value


if __name__ == '__main__':
    test = ReadConfigYaml()
    print(test.get_db("Mail-Config", "mail_receivers"))
