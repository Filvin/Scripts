'''
Simple python script to poll a website at regular intervals, and search for a particular text.
Send email notifications based on search-text found/not found(configurable).

Eg:
Get to know when a out-of-stock product is available in flipkart.
Poll the url, and search 'Buy now' button, if found send notification, and exit, else keep polling. 

Usage: python poll_and_notify_script.py
'''

import smtplib
import requests
import time

################### CONFIG ###################
url = "https://www.flipkart.com/redmi-note-5-blue-32-gb/p/itmf3qsthbjgxsks?pid=MOBF28FTCDFR7VYZ&srno=s_1_1&otracker=search&lid=LSTMOBF28FTCDFR7VYZQPZAPY&fm=SEARCH&iid=f2cd18ac-8a79-431c-aea7-acee7d6884a3.MOBF28FTCDFR7VYZ.SEARCH&ppt=Homepage&ppn=Homepage&ssid=nghwhh8xio0000001535820399373&qH=1fd3c08a224c9dc8"
search_text = "BUY NOW"
poll_interval = 120  # seconds
health_notify_try_cnt = 10  # notify after n tries, just to make sure script is running fine.
# configure alerts
alert_search_text_found = True
alert_search_text_not_found = False
# configure when to stop
exit_when_found = False
exit_when_not_found = True
# configure email-notification
fromaddr = 'XXX@gmail.com'
toaddrs = 'XXX@gmail.com'
username = 'XXX@gmail.com'
password = 'XXX'

def send_mail(msg):
    msg = '''From: %s\nTo: %s\nSubject: Notification\n\n%s\n''' % (fromaddr, toaddrs, msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

if __name__ == "__main__":
    try_count = 1
    while 1:
        r = requests.get(url)
        if r.status_code != 200:
            exit(0)
        if r.text.rfind(search_text):
            print("%s found." % (search_text))
            if alert_search_text_found:
                send_mail("%s not found." % (search_text))
            if exit_when_found:
                exit(0)
        else:
            print("%s not found!!!" % (search_text))
            if alert_search_text_not_found:
                send_mail("%s not found!!!" % (search_text))
            if exit_when_not_found:
                exit(0)
        time.sleep(poll_interval)
        if try_count % health_notify_try_cnt == 0:
            send_mail("Total tries : %s" % (try_count))
        try_count += 1
