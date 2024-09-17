'''
                    Домашнее задание 4. Парсинг HTML. XPath
Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:

Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
Комментарии для объяснения цели и логики кода.

Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.
'''

import requests
from lxml import html
import csv

# URL веб-сайта
url = 'https://news.mail.ru'

# Заголовки HTTP-запроса, включая строку агента пользователя
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Отправка GET-запроса и получение HTML-содержимого страницы
response = requests.get(url, headers=headers)
response.raise_for_status()  # Проверка на ошибки HTTP

# Парсинг HTML с использованием lxml
tree = html.fromstring(response.content)

# Выражения XPath для извлечения данных из новостей
# Предположим, что новости находятся в блоках с определенным классом
news_blocks_1 = tree.xpath('//span[contains(@class, "js-topnews__item")]')
news_blocks_2 = tree.xpath('//span[contains(@class, "list__item__inner")]')

# НЕ получается выбрать необходимую область таким образом, хоть рекламу (@class, "owk4d9zkb") и убрала, но почему-то не удается 
# вывести правильный набор данных..
# news_blocks = tree.xpath('//div[contains(@class, "js-module") and not(contains(@class, "owk4d9zkb"))]') 

# Список для хранения данных таблицы
data = []

try:
    data.append([' '])
    data.append(['Данные имеют фото на сайте:'])
    data.append([' '])
    # 1. Извлечение данных из каждого СВО блока новости с фото
    for block_1 in news_blocks_1:
        # 1. Перебираем СВО новости с фото:
        # Предположим, что каждый блок содержит заголовок новости и ссылку на новость
        title_foto = ''.join(block_1.xpath('.//span[contains(@class, "photo__captions")]//text()')).strip()
        
        # Извлечение ссылки на новость
        link_element = block_1.xpath('.//a[contains(@class, "link-holder")]')
        if link_element:
            link_foto = link_element[0].get('href')
        else:
            link_foto = ''
        
        # Добавление данных в список
        data.append([title_foto, link_foto])

    data.append([' '])
    data.append(['Данные без фото на сайте:'])
    data.append([' '])

    # 2. Извлечение данных из каждого СВО блока новости без фото
    for block_2 in news_blocks_2:
        # # Предположим, что каждый блок содержит заголовок новости и ссылку на новость
        title = ''.join(block_2.xpath('.//a[contains(@class, "list__text")]//text()')).strip()
        # link = block.get('href')

        # # Извлечение ссылки на новость
        link_element = block_2.xpath('.//a[contains(@class, "list__text")]')
        if link_element:
            link = link_element[0].get('href')
        else:
            link = ''
        
        # Добавление данных в список
        data.append([title, link])

    # 3. Сохранение данных в CSV-файл
    with open('news_data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Заголовок', 'Ссылка'])  # Заголовки столбцов
        writer.writerows(data)

# проверки
except requests.HTTPError as e:
    print(f"Ошибка запроса HTTP: {e}")
except requests.RequestException as e:
    print(f"Ошибка запроса: {e}")
except html.etree.ParserError as e:
    print(f"Ошибка парсинга HTML: {e}")
except Exception as e:
    print(f"Ошибка: {e}")

print("Данные успешно сохранены в файл news_data.csv")



