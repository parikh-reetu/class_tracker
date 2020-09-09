import os
import requests
from bs4 import BeautifulSoup
import smtplib
import time
from dotenv import load_dotenv  # for python-dotenv method
load_dotenv()  # for python-dotenv method


def checkStatus(count, dept, num):
    url = 'https://classes.cornell.edu/search/roster/FA20?q=' + dept + \
        num + '&days-type=any&crseAttrs-type=any&breadthDistr-type=any&pi='
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, features="lxml")

    status = soup.find(class_='group heavy-left').find_next('ul').find_next('ul').find(
        class_='open-status').find(class_='tooltip-iws').get('data-content').lower()
    print(count, status)

    return status


def textSender(status, count):
    gmail_user = os.environ.get('GMAIL')
    gmail_password = os.environ.get('PASSWORD')

    sms_gateway = os.environ.get('GATEWAY')
    sms = 'ENROLL\nStatus: {}\nCount: {}'.format(status, count)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, sms_gateway, sms)
        server.quit()

        print('-----------------------Text sent!-----------------------')
    except:
        print('Something went wrong...')


if __name__ == "__main__":
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    dept = input("Please enter department name: ")
    num = input("Please enter course number: ")
    count = 0
    status = 'closed'
    while (status == 'closed'):
        count += 1
        if count % 3 == 0:
            textSender(status, count)
        status = checkStatus(count, dept, num)
        time.sleep(5)

    if (status != 'closed'):
        textSender(status, count)
