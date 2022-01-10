# coding = utf-8
import logging


class Log():
    def __init__(self, level=logging.DEBUG):
        """初始化日志器"""
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

    def get_famtter(self):
        """创建格式器"""
        f1 = logging.Formatter(fmt='[%(filename)s]: [%(lineno)d] [%(levelname)s] [%(asctime)s] -->>%(message)s ',
                               datefmt='%Y-%m-%d %H:%M:%S')
        f2 = logging.Formatter(fmt='[%(levelname)s]: [%(asctime)s] -->>%(message)s ', datefmt='%Y-%m-%d %H:%M:%S')
        return f1, f2

    def add_StreamHandler(self, level=logging.INFO):
        """创建处理器，并添加到日志器中"""
        self.s_handler = logging.StreamHandler()
        self.s_handler.setLevel(level)
        self.s_handler.setFormatter(self.get_famtter()[1])
        self.logger.addHandler(self.s_handler)

    def add_FileHandler(self, file='./data.log', level=logging.DEBUG):
        """创建处理器，并添加到日志器中"""
        self.f_handler = logging.FileHandler(filename=file)
        self.f_handler.setLevel(level)
        self.f_handler.setFormatter(self.get_famtter()[0])
        self.logger.addHandler(self.f_handler)

    def get_log(self, file='./data/data.log'):
        """获取经过处理的日志器"""
        self.add_StreamHandler()
        self.add_FileHandler(file=file)
        return self.logger


if __name__ == '__main__':
    log = Log()
    logger = log.get_log()
    logger.critical('严重错误')
    logger.error('错误')
    logger.warning('警告')
    logger.info('信息')
    logger.debug('调试信息')
