import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(credentials, recipients, subject, content):
    account = credentials['account']
    password = credentials['password']
    smtp_host = credentials['host']
    smtp_port = credentials['port']

    message = MIMEMultipart()
    message['From'] = account
    message['To'] = recipients
    message['Subject'] = subject
    message.attach(MIMEText(content, 'html'))

    server = smtplib.SMTP_SSL(smtp_host, smtp_port)
    server.ehlo()
    server.login(account, password)
    server.sendmail(account, recipients, message.as_string())
    server.close()