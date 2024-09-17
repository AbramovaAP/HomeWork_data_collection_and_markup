from scrapy.crawler import CrawlerProcess  #crawler – набор функций, который собирает на финальном этапе все модуль программного кода вместе
from scrapy.utils.reactor import install_reactor #импортируем функцию, которая запускает процесс нашего реактора, по сути ядра программного кода
from scrapy.utils.log import configure_logging #импортируем логи
from scrapy.utils.project import get_project_settings #импортируем функцию, которая отвечает за чтение настроек и превращение эти настройки в вид, позволяющий записать свойства в объект нашего паука
from jobparser.spiders.hhru import HhruSpider


if __name__ == "__main__":
    configure_logging()
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    process = CrawlerProcess(get_project_settings()) #запускаем процесс работы
    process.crawl(HhruSpider)
    process.start()
