import requests
from bs4 import BeautifulSoup


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
                if 'https://hh.ru/vacancy' in a.attrs["href"].split("?")[0]:
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
        name = 'Данные отсутсвуют'
    try:
        salary = soup.find(attrs={'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-label-1-regular___pi3R-_3-0-9'}).getText().replace("\xa0", '')
    except:
        salary = 'Данные отсутсвуют'
    try:
        exp = soup.find(attrs={"data-qa": "vacancy-experience"}).getText()
        if '–' in exp:
            exp = exp.split(' ')[0]

    except:
        exp = 'Данные отсутсвуют'
    try:
        chart = soup.find(attrs={'data-qa': 'vacancy-view-employment-mode'}).getText()
    except:
        chart = 'Данные отсутсвуют'
    try:
        skills = [skill.text for skill in soup.find(attrs={'class': 'vacancy-skill-list--COfJZoDl6Y8AwbMFAh5Z'}).find_all(attrs={'class': 'magritte-tag__label___YHV-o_3-0-0'})]
        ski = ''
        for i in range(len(skills)):
            if '\xa0' in skills[i]:
                skills[i] = skills[i].reaplce('\xa0', '')

            ski = ski + skills[i] + ', '
        ski = ski[:-2]
    except:
        ski = 'Данные отсутсвуют'
    try:
        address = soup.find(attrs={'data-qa': 'vacancy-view-raw-address'}).getText().split(',')[0]
    except:
        address = 'Данные отсутсвуют'

    resume = {
        'name': name,
        'salary': salary,
        'work experience': exp,
        'chart': chart,
        'skills': ski,
        'address': address
    }
    return resume

if __name__ == '__main__':
    count = 0
    for a in get_links('python'):
        count += 1
        print(f'{count} - {get_job(a)}')

        if count == 10:
            break