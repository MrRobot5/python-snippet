import smtplib

from email.mime.text import MIMEText
from email.header import Header

"""
使用 python 脚本，实现 plain-text 邮件发送。
使用场景： 定时任务通知

@since: 2023年11月7日10:34:26
@author: chat-gpt 
"""

SMTP_PORT = 25

SMTP_SERVER = "smtp.163.com"

# password 参考 https://github.com/MrRobot5/chocolate-factory/blob/master/src/main/resources/application-mail.yml
USERNAME = "18801021018@163.com"

PASSWORD = "foo"


def send_email(subject, message, to_addr):
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = Header(USERNAME)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(subject)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, [to_addr], msg.as_string())
    server.quit()


if __name__ == '__main__':
    send_email(subject="Hello", message="This is a test email", to_addr="1050335971@qq.com")

