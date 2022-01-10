import configparser
import os


class ReadConfig(object):
    """
    定义一个读取配置文件的类
    """

    def __init__(self, filepath=None):
        if filepath:
            self.read_path = filepath
        else:
            # 获取当前文件所在目录的上一级目录，即项目所在目录
            self.read_path = os.path.join(os.getcwd(), "./config.ini")

        self.config = configparser.ConfigParser()
        self.config.read(self.read_path)

    def get_db(self, sections, param):
        value = self.config.get(sections, param)
        return value


if __name__ == '__main__':
    test = ReadConfig()
    print(test.get_db("Mail-Config", "mail_receivers"))
