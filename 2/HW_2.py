'''
Урок 2. Парсинг HTML. BeautifulSoup
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ 
и извлечь информацию о всех книгах на сайте во всех категориях: 
название, цену, 
количество товара в наличии (In stock (19 available)) в формате integer, описание.

Затем сохранить эту информацию в JSON-файле.
'''
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import re

# Формирование исходных URL
base_url = "http://books.toscrape.com/"

# Формируем параметры и заголовки запроса:
ua = UserAgent()
headers = {"User-Agent": ua.random}  # Используем рандомный User-Agent
params = {"page": 1}

session = requests.Session()

all_books = []

# 1. Цикл для получения информации о книгах на странице
while True:
    print(f"Обрабатывается {params['page']} страница")

    response = session.get(base_url + "catalogue/page-" + str(params['page']) + ".html", headers=headers)
    if response.status_code != 200:
        break
    
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("h3")  # по тегу h3 определяем ссылку на страницу книги с полными данными
    
    # 1.1 обрабатываем книги в цикле for
    for book in books:
        # Поиск информации по книге
        book_info = book.find("a", href=True)
        # Создание ссылки на страницу книги
        book_url = base_url + "catalogue/" + book_info["href"]
        # Отправка запроса по ссылке на книгу
        book_response = session.get(book_url, headers=headers)
        # Парсинг личной страницы книги
        book_soup = BeautifulSoup(book_response.text, "html.parser")

        # 1.1.2 получаем данные:
        # Название:
        title_tag = book_soup.find("h1")
        title = title_tag.text.strip() if title_tag else "No title available"

        # Цена в фунтах стерлингов:
        price_tag = book_soup.find('p', {'class': 'price_color'})
        price = price_tag.text[2:] if price_tag else "No price available"

        # Количество в наличии
        stock_tag = book_soup.find('p', {'class': 'instock availability'})
        stock_number = int(re.search(r'\d+', stock_tag.text).group()) if stock_tag else 0

        # Описание
        description_tag = book_soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"].strip() if description_tag else 'No description available'

        # 1.1.3 Добавление книги в общий список
        all_books.append({
            "Название": title,
            "Цена в фунтах стерлингов": price,
            "Количество в наличии": stock_number,
            "Описание": description
        })
        print("Добавили книгу:", title)

    next_button = soup.find('li', {'class': 'next'})
        
    # Проверка, есть ли ссылка "next" на следующую страницу
    if next_button:
        params['page'] += 1
    else:
        break  # если ссылки нет - выходим из цикла while

# Сохраняем информацию в JSON-файле
with open('books_toscrape.json', 'w', encoding='utf-8') as file:
    json.dump(all_books, file, ensure_ascii=False, indent=4)
