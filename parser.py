import requests
import bs4


def parser(znak):

    ru_eng_znak = {'Овен': 'oven', 'Телец': 'telec',
                   'Близнецы': 'bliznecy', 'Рак': 'rak',
                   'Лев': 'lev', 'Дева': 'deva',
                   'Весы': 'vesy', 'Скорпион': 'skorpion',
                   'Стрелец': 'strelec', 'Козерог': 'kozerog',
                   'Водолей': 'vodoley', 'Рыбы': 'ryby'}

    if znak == '':
        return ''
    url = f"https://my-calend.ru/goroskop/{ru_eng_znak[znak]}"
    response = requests.get(url)
    if response:
        page = bs4.BeautifulSoup(response.content, 'html5lib')
        texts = page.find_all('p')
        text = texts[0]
        text = str(text)[3:-4]
        return text
