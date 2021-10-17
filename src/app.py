import datetime
import os
import smtplib
from email.mime.text import MIMEText

import pings
from pytz import timezone

# Settings
ping_host = os.environ['PING_HOST']
mail_smtp_host = os.environ['MAIL_SMTP_HOST']
mail_smtp_port = int(os.environ['MAIL_SMTP_PORT'])
mail_account = os.environ['MAIL_ACCOUNT']
mail_password = os.environ['MAIL_PASSWORD']
mail_from = os.environ['MAIL_FROM']
mail_to = os.environ['MAIL_TO']
mail_cc = os.environ.get('MAIL_CC', '')


def send_mail_when_succeeded():
    subject = '[OK] PING succeeded ' + ping_host
    body = 'PING to {0} succeeded at {1:%Y-%m-%d %H:%M:%S}'.format(ping_host, get_datetime_now())
    send_mail(subject, body)


def send_mail_when_failed():
    subject = '[CRITICAL] PING failed ' + ping_host
    body = 'PING to {0} failed at {1:%Y-%m-%d %H:%M:%S}'.format(ping_host, get_datetime_now())
    send_mail(subject, body)


def send_mail(subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Cc'] = mail_cc
    server = smtplib.SMTP(mail_smtp_host, mail_smtp_port)
    server.starttls()
    server.login(mail_account, mail_password)
    server.send_message(msg)
    server.quit()


def get_datetime_now():
    return datetime.datetime.now(timezone('Asia/Tokyo'))


def main():
    print('PING to {0} at {1:%Y-%m-%d %H:%M:%S}'.format(ping_host, get_datetime_now()))
    ping = pings.Ping()
    response = ping.ping(ping_host, 2)
    if response.is_reached():
        print('Success!\n')
        send_mail_when_succeeded()
    else:
        print('Failed!\n')
        send_mail_when_failed()
    exit()


if __name__ == '__main__':
    main()
