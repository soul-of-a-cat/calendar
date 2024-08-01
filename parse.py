from bs4 import BeautifulSoup
import pymorphy2
import requests

morph = pymorphy2.MorphAnalyzer()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
}
data = {
    'f026eed117': '36877',
    'name': '',
}
session = requests.session()
text = '''"Календарь"
Сегодня '''

url_events = 'https://kakoysegodnyaprazdnik.ru/'
response1 = session.post(url_events, headers=headers, data=data)
response1.encoding = 'utf-8'
web_events = BeautifulSoup(response1.text, 'lxml')

url_weather_spb = 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/?ysclid=lmhwisjcfq453695344'
response2 = session.get(url_weather_spb, headers=headers)
web_weather_spb = BeautifulSoup(response2.text, 'lxml')

url_weather_syzran = 'https://www.gismeteo.ru/weather-syzran-4448/'
response3 = session.get(url_weather_syzran, headers=headers)
web_weather_syzran = BeautifulSoup(response3.text, 'lxml')

today = web_events.find('h2', attrs={'class': 'mainpage'})
today = today.text.split()
data = ' '.join(today[:3]).lower()
day = today[-1]
text += f'{data}, {day}.\n'

astro_times = web_weather_spb.find('div', attrs={'class': 'astro-times'}).find_all('div')
for i in range(1, len(astro_times)):
    text_times = astro_times[i].text.split('—')
    for j in range(len(text_times)):
        text_times[j] = text_times[j].replace('\n', '').replace(' ', '')
    astro_times[i] = ' - '.join(text_times)
times = '\n'.join([astro_times[1], astro_times[2]])

text += f'\nСолнце:\n{times}\n\nСобытия:\n'

events = web_events.findAll('span', attrs={'itemprop': 'text'})

for i in range(len(events) - 2):
    q = events[i].text
    n = q.find('(')
    m = q.find(')')
    if n != -1:
        q = q[:n - 1] + q[m + 1:]
    text += f'* {q}\n'

text += '\nИменинники:\n'

r = events[-2].text.split()
for i in range(2, len(r)):
    t = r[i][:-1]
    word = morph.parse(t)[0]
    gent = word.inflect({'nomn'})
    gent = gent.word
    text += f'~ {gent.capitalize()}\n'

weather_syzran = web_weather_syzran.find('div', attrs={'class': 'chart'}).find_all('temperature-value')
values = []
for i in range(len(weather_syzran)):
    values.append(weather_syzran[i].get('value'))
text += f'\nПогода в Сызрани: +{max(values)}°С\nВ. И. Ленин спит? Да, спит.'
