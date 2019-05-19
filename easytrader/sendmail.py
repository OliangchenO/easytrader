import smtplib
from email.mime.text import MIMEText
import logging


class MailUtils:
    def __init__(self, debug=True):
        # 设置服务器所需信息
        # aliyun邮箱服务器地址
        self.mail_host = 'smtp.aliyun.com'
        # aliyun邮箱用户名
        self.mail_user = 'liang_chen@aliyun.com'
        # 密码(部分邮箱为授权码)
        self.mail_pass = '19891121Lc'
        # 邮件发送方邮箱地址
        self.sender = 'liang_chen@aliyun.com'
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        self.receivers = ['593705862@qq.com']

        self.log_level = logging.DEBUG if debug else logging.INFO

    def send_email(self, receivers, subject, content):
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = subject
        # 发送方信息
        message['From'] = self.sender
        # 接受方信息
        message['To'] = receivers
        # 登录并发送邮件
        try:
            smtp_obj = smtplib.SMTP()
            # 连接到服务器
            smtp_obj.connect(self.mail_host, 25)
            # 登录到服务器
            smtp_obj.login(self.mail_user, self.mail_pass)
            # 发送
            smtp_obj.sendmail(
                self.sender, receivers, message.as_string())
            # 退出
            smtp_obj.quit()
            print('success')
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误
