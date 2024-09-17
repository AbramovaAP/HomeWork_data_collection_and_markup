import json
from pymongo import MongoClient
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


DB = 'Scrapy_HW_5'
COLLECTION = 'hhru'


try:
    client = MongoClient('localhost', 27017)
    db = client[DB]
    collection = db[COLLECTION]
    documents = list(collection.find())
    print(f"Выгружено с БД {DB} коллекции {COLLECTION} {len(documents)} документов")

    file_path = f"{COLLECTION}.json"
    if os.path.exists(file_path):
        print(f"Предупреждение: файл {file_path} уже существует. Начинается перезапись даннных...")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)
    print(f"Сохранено в файл {file_path}")
except Exception as e:
    print(f"Error: {e}")

'''
Вывод:
PS C:\Users\79858\Desktop\Scrapy_HW5\jobparser> python download.py
Выгружено с БД Scrapy_HW_5 коллекции hhru 5 документов
Сохранено в файл hhru.json
PS C:\Users\79858\Desktop\Scrapy_HW5\jobparser> 


PS C:\Users\79858\Desktop\Scrapy_HW5\jobparser> python download.py
Выгружено с БД Scrapy_HW_5 коллекции hhru 52 документов
Предупреждение: файл hhru.json уже существует. Начинается перезапись даннных...
Сохранено в файл hhru.json
PS C:\Users\79858\Desktop\Scrapy_HW5\jobparser> 
'''