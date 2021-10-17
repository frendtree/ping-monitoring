import datetime
import os
import smtplib
from email.mime.text import MIMEText

import pings
from pytz import timezone

# Settings
PING_HOST = os.environ['PING_HOST']
MAIL_SMTP_HOST = os.environ['MAIL_SMTP_HOST']
MAIL_SMTP_PORT = int(os.environ['MAIL_SMTP_PORT'])
MAIL_ACCOUNT = os.environ['MAIL_ACCOUNT']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAIL_FROM = os.environ['MAIL_FROM']
MAIL_TO = os.environ['MAIL_TO']
MAIL_CC = os.environ.get('MAIL_CC', '')


def send_mail_when_succeeded():
    subject = '[OK] PING succeeded ' + PING_HOST
    body = 'PING to {0} succeeded at {1:%Y-%m-%d %H:%M:%S}'.format(PING_HOST, get_datetime_now())
    send_mail(subject, body)


def send_mail_when_failed():
    subject = '[CRITICAL] PING failed ' + PING_HOST
    body = 'PING to {0} failed at {1:%Y-%m-%d %H:%M:%S}'.format(PING_HOST, get_datetime_now())
    send_mail(subject, body)


def send_mail(subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = MAIL_TO
    msg['Cc'] = MAIL_CC
    server = smtplib.SMTP(MAIL_SMTP_HOST, MAIL_SMTP_PORT)
    server.starttls()
    server.login(MAIL_ACCOUNT, MAIL_PASSWORD)
    server.send_message(msg)
    server.quit()


def get_datetime_now():
    return datetime.datetime.now(timezone('Asia/Tokyo'))


def main():
    print('PING to {0} at {1:%Y-%m-%d %H:%M:%S}'.format(PING_HOST, get_datetime_now()))
    ping = pings.Ping()
    response = ping.ping(PING_HOST, 2)
    if response.is_reached():
        print('Success!\n')
        send_mail_when_succeeded()
    else:
        print('Failed!\n')
        send_mail_when_failed()
    exit()


if __name__ == '__main__':
    main()
