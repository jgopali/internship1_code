import requests

import smtplib

from email.mime.text import MIMEText

import json

 

 

 

API_Key= ##add your uelscan app key

API_Endpoint="https://urlscan.io/user/quotas/"

SENDER = "randomemail@random.com"

SMTP_SERVER = "yoursmtpserver"

PORT = "25"

emails=["jgopali@citco.com"]

THRESHOLD = 0
def get_quota():

    headers={"API-Key": API_Key}

    response=requests.get(API_Endpoint, headers=headers)

    return response.json()if response.status_code==200 else None

 

def check_quota(priv, pub):

    msg = ""

    if priv >= THRESHOLD and pub >= THRESHOLD:

        msg = "Both private and public thresholds are hit"

    else:

        if priv >= THRESHOLD:

            msg = "Private hit the treshold"

        if pub >= THRESHOLD:

            msg = "Public hit the treshold"

        msg = "Both private and pblic didn't hit the threshold yet."

 

    return msg

 

 

def send_mail(emails, data):

    severity = 'info'

    msg_text = data

   

    msg = MIMEText(msg_text)

    msg['Subject'] = 'URL SCAN Quota: ' + severity

    msg['From'] = SENDER

    msg['To'] = ', '.join(emails)

 

    s = smtplib.SMTP(SMTP_SERVER, PORT)

    s.sendmail(SENDER, emails, msg.as_string())

    s.quit()

 

 

if __name__ == "__main__":

    ##main

    response = get_quota()

 

    if response:

        private_percentage_per_day = response['limits']['private']['day']['percent']

        public_percentage_per_day = response['limits']['public']['day']['percent']

 

        msg = check_quota(private_percentage_per_day, public_percentage_per_day)

 

        send_mail(emails, msg)

    else:

        print("There is an error")