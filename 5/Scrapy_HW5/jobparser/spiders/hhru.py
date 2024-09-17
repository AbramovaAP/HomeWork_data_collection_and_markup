import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from datetime import datetime # библиотека для работы с форматами дат, нужна для преобразования из строк
import locale # библиотека для работы с локализацией, необходима для правильного преобразования русских месяцев
locale.setlocale(locale.LC_TIME, 'ru_RU.utf8') # указываю русскую локализацию, для преобразования месяцев


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    # start_urls = [
    #     "https://korolev.hh.ru/search/vacancy?text=Python&area=2090&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"]

    start_urls = [
        "https://korolev.hh.ru/vacancies/programmist?customDomain=1"]


    def parse(self, response: HtmlResponse):

        # Сначала проверяем наличие ссылки на след страницу, чтобы сократить время работы
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()

        # если ссылка на следующую страницу есть, то переходим на нее и снова выполняем эту  функцию (def parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        #блок, который отвечает за сбор данных на первой странице сайта
        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        vacancy_title = response.xpath('//h1[@data-qa="vacancy-title"]/text()').get()
        try:
            vacancy_salary = response.xpath('.//div[@data-qa="vacancy-salary"]//text()').getall()
            vacancy_salary = [x.strip() for x in vacancy_salary]
            vacancy_salary = [x.replace('₽', 'руб.') for x in vacancy_salary]
            vacancy_salary[1] = int(vacancy_salary[1].replace('\xa0', ''))
            vacancy_salary[3] = int(vacancy_salary[3].replace('\xa0', ''))
        except:
            vacancy_salary = []
        vacancy_experience = response.xpath(".//p[@class='vacancy-description-list-item']//text()").getall()
        vacancy_experience = [x for x in vacancy_experience if x != ', ' and x != ': ']
        company_name = response.xpath('.//a[@data-qa="vacancy-company-name"]/span/text()').getall()
        company_name = list(set([x.replace('\xa0', '') for x in company_name]))
        description = response.xpath(".//div[@data-qa='vacancy-description']//text()").getall()
        description = [x.replace('\xa0', '') for x in description if x != ', ' and x != ' ' and x != ' ']
        vacancy_link = response.url
        vacancy_skills = response.xpath('.//div[@class="bloko-tag-list"]//text()').getall()
        _id = int(vacancy_link.split('/')[-1].split('?')[0])
        yield JobparserItem(_id=_id, vacancy_title=vacancy_title, vacancy_salary=vacancy_salary, vacancy_experience=vacancy_experience, 
                            company_name=company_name, description=description, 
                            vacancy_link=vacancy_link, vacancy_skills=vacancy_skills)
        print()

