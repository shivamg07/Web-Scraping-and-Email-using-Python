from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage

print('Put some skills that you are not familiar with:')
unfamiliar_skills = [str.strip().lower() for str in input('>').split(',')]
print('Filtering out', unfamiliar_skills)

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=').text

    soup =  BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for job in jobs:
        published_date = job.find('span', class_='sim-posted').span.text
        skills = [str.strip().lower() for str in job.find('span', class_='srp-skills').text.replace('  ', '').strip().split(',')]

        if 'few' in published_date and all(not(element in skills) for element in unfamiliar_skills):
            company_name = job.find('h3', class_='joblist-comp-name').text.strip()
            more_info = job.header.h2.a['href']

            with open('Job_Listings.txt', 'a') as f:
                f.write(f"\n\nCompany Name: {company_name}")
                f.write(f'\nSkills: {skills}')
                f.write(f'\nMore Info: {more_info}')

def notify():
    smtp_server = 'smtp.gmail.com'
    port = 465
    Sender = 'xxxxxxx'
    Receiver = 'xxxxxx'
    password = 'xxxxxxx'

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(Sender, password)

    msg = EmailMessage()
    msg['From'] = Sender
    msg['To'] = Receiver
    msg['Subject'] = 'New Jobs Alert!'
    msg.set_content('PFA')

    with open('Job_Listings.txt', 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file_name)

    server.send_message(msg)
    

find_jobs()
notify()
print('Mail Sent')
    