# WebScraping
import requests
import selectorlib
import smtplib, ssl
import os
import time
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
MY_CONTEXT = ssl.create_default_context()
PASSWORD = os.getenv("PASSWORD")
SENDER = os.getenv("USERNAME")
RECEIVER = os.getenv("USERNAME")
URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    # Scrape the page source from a URL
    # we are setting the User-Agent to make it look like we’re using a popular web browser via headers
    response = requests.get(url, headers=HEADERS)
    content = response.text
    return content

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(message):
    host = HOST
    port = int(PORT)
    username = SENDER
    password = PASSWORD
    receiver = RECEIVER
    context = MY_CONTEXT

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Mail was sent")

def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + '\n')

def read(extracted):
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="Hey, a new event was found")

        time.sleep(2)