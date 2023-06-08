import time
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.common.by import By


class ChmiLocationRecord(object):
    def __init__(self, location):
        self.location = location
        self.temperatures = []


class ChmiYearRecord(object):
    def __init__(self, year):
        self.year = year
        self.locations = []


class Records(object):
    def __init__(self):
        self.years = []

    def save_record(self):
        for y in self.years:
            with open('./data/%s' % y) as f:
                pass


class ChmiScaper(object):
    CHMI_DATA_MAIN_URL = \
        'https://www.chmi.cz/historicka-data/pocasi/uzemni-teploty'

    def __init__(self):
        self._driver = webdriver.Chrome()
        self._executor = ThreadPoolExecutor(max_workers=5)

    def scrape(self):
        year_links = self._get_years_links()
        data = self._scrape_year_page(year_links)

    def _scrape_year_page(self, year_links):
        year_rec = ChmiYearRecord(year_links[0].text)
        year_links[0].click()

        element = self._driver.find_element(By.ID, 'loadedcontent')
        table = element.find_element(By.TAG_NAME, 'table')
        trs = table.find_elements(By.XPATH, "//tr[@class='nezvyraznit']")

        i = 0
        location_rec = None
        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME, 'td')
            if i % 3 == 0:
                location_rec = ChmiLocationRecord(tds[0].text)
                print(tds[0].text)
                for td in tds[2:]:
                    print(td.text)
                    location_rec.temperatures.append(td.text)

        time.sleep(100)
        return table

    def _get_years_links(self):
        self._driver.get(self.CHMI_DATA_MAIN_URL)
        element = self._driver.find_element(By.ID, 'loadedcontent')
        elements = element.find_elements(By.XPATH, "//table[@cellspacing='2']")

        tab1 = elements[0]
        tab2 = elements[1]
        links1 = tab1.find_elements(By.TAG_NAME, 'a')
        links2 = tab2.find_elements(By.TAG_NAME, 'a')

        return links1 + links2
