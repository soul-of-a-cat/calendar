from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import pymorphy2
import requests
import time
import os


opts = FirefoxOptions()
opts.add_argument("--no-sandbox")
opts.add_argument("--headless")
opts.add_argument("--disable-gpu")
opts.add_argument("--window-size=1920,1080")
driver = webdriver.Firefox(options=opts)
morph = pymorphy2.MorphAnalyzer()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'}
text = '''"Календарь"
Сегодня '''

url_events = 'https://kakoysegodnyaprazdnik.ru/'
while True:
    try:
        driver.get(url_events)
        main_page = driver.window_handles[0]
        driver.switch_to.window(main_page)
        time.sleep(5)
        break
    except Exception:
        driver.quit()
        driver = webdriver.Firefox(options=opts, executable_path=os.getcwd() + '/geckodriver')
web_events = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()
display.stop()

url_weather_spb = 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/?ysclid=lmhwisjcfq453695344'
response2 = requests.get(url_weather_spb, headers=headers)
web_weather_spb = BeautifulSoup(response2.text, 'lxml')

url_weather_syzran = 'https://www.gismeteo.ru/weather-syzran-4448/'
response3 = requests.get(url_weather_syzran, headers=headers)
web_weather_syzran = BeautifulSoup(response3.text, 'lxml')

today = web_events.find('h2', attrs={'class': 'mainpage'})
today = today.text.split()
data = ' '.join(today[:3])
day = today[-1]
text += f'{data}, {day}.\n'

astro_times = web_weather_spb.find('div', attrs={'class': 'astro-times'}).find_all('div')
times = '\n'.join([astro_times[1].text, astro_times[2].text])

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

weather_syzran = web_weather_syzran.find('div', attrs={'class': 'chart'}).find_all('span', attrs={
    'class': 'unit_temperature_c'})
for i in range(len(weather_syzran)):
    weather_syzran[i] = int(weather_syzran[i].text[1:])
text += f'\nПогода в Сызрани: +{max(weather_syzran)}°С\nВ. И. Ленин спит? Да, спит.'
