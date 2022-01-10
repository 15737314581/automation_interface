# coding = utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class SendMail(object):
    def __init__(self, mail_host):
        self.mail_host = mail_host

    def send(self, title, content, sender, auth_code, receivers):
        message = MIMEText(content, "html", "utf-8")
        message["From"] = "{}".format(sender)
        message["To"] = ",".join(receivers)
        message["Subject"] = title
        try:
            smtp_obj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用ssl发信，端口一般为465
            smtp_obj.login(sender, auth_code)  # 登录
            smtp_obj.sendmail(sender, receivers, message.as_string())


        except Exception as e:
            print(e)


if __name__ == '__main__':
    mail = SendMail("smtp.126.com")
    sender = "jjf15737314581jjf@126.com"
    receivers = ["1065109432@qq.com"]
    title = "接口自动化测试demo"
    content = """
    小滴课堂 邮件测试gt
    <a href="https://xdclass.net">进入小滴课堂官网</a>
    """
    # 授权码
    auth_code = "KVBMWYLGZYEKWQGZ"
    mail.send(title, content, sender, auth_code, receivers)
