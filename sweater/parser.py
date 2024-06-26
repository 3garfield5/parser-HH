import requests
from bs4 import BeautifulSoup
import time
import json

from sweater import ua

def get_links(text):
    data = requests.get(
        url = f'https://hh.ru/search/vacancy?text={text}&salary=&ored_clusters=true&area=113&page=1&customDomain=1',
        headers={'user-agent': ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        page_count = int(soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(
                url=f'https://hh.ru/search/vacancy?text={text}&salary=&ored_clusters=true&area=113&page=1&customDomain={page}',
                headers={'user-agent': ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for a in soup.find_all('a', attrs={'class': 'bloko-link'}):
                yield f'{a.attrs["href"].split("?")[0]}'

        except Exception as e:
            print(f'{e}')


def get_job(link):
    data = requests.get(
        url=link,
        headers={'user-agent': ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        name = soup.find(attrs={'data-qa': 'vacancy-title'}).getText()
    except:
        name = ''
    try:
        salary = soup.find(attrs={'class': 'magritte-text___pbpft_3-0-8 magritte-text_style-primary___AQ7MW_3-0-8 magritte-text_typography-label-1-regular___pi3R-_3-0-8'}).getText().replace("\xa0", '')
    except:
        salary = ''
    try:
        exp = soup.find(attrs={"data-qa": "vacancy-experience"}).getText()
    except:
        exp = ''
    try:
        chart = soup.find(attrs={'data-qa': 'vacancy-view-employment-mode'}).getText()
    except:
        chart = ''
    try:
        skills = [skill.text for skill in soup.find(attrs={'class': 'vacancy-skill-list--COfJZoDl6Y8AwbMFAh5Z'}).find_all(attrs={'class': 'magritte-tag__label___YHV-o_2-0-12'})]
        for i in range(len(skills)):
            if '\xa0' in skills[i]:
                skills[i] = skills[i].reaplce('\xa0', '')
    except:
        skills = ''
    try:
        address = soup.find(attrs={'data-qa': 'vacancy-view-raw-address'}).getText()
    except:
        address = ''

    resume = {
        'name':name,
        'salary': salary,
        'work experience': exp,
        'chart': chart,
        'skills': skills,
        'address': address
    }
    return resume

if __name__ == '__main__':
    for a in get_links('python'):
        if 'https://hh.ru/vacancy/' in a:
            print(get_job(a))