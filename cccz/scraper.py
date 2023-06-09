import os
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
        self.year = int(year)
        self.locations = []

    def add_location_rec(self, location):
        self.locations.append(location)

    def save(self):
        y_str = ''
        for loc in self.locations:
            t_str = str(loc.temperatures)[1:-1]
            loc_str = ('%s,%s\n' % (loc.location, t_str)).replace(' ', '')
            y_str += loc_str

        with open('./data/%d.csv' % self.year, 'w') as f:
            f.write(y_str)


class ChmiScaper(object):
    CHMI_DATA_MAIN_URL = \
        'https://www.chmi.cz/historicka-data/pocasi/uzemni-teploty'

    def __init__(self):
        self._driver = None
        self._executor = ThreadPoolExecutor(max_workers=5)

    def scrape(self):
        self._driver = webdriver.Chrome()
        self._scrape_years_pages()

    def _scrape_years_pages(self):
        year_links = self._get_years_links()

        for i in range(len(year_links)):
            if not os.path.isfile('./data/%s.csv' % year_links[i].text):
                year_rec = ChmiYearRecord(year_links[i].text)

                print('scraping year %d' % year_rec.year)

                year_links[i].click()
                time.sleep(3)

                element = self._driver.find_element(By.ID, 'loadedcontent')
                table = element.find_element(By.TAG_NAME, 'table')
                trs = table.find_elements(By.XPATH,
                                          "//tr[@class='nezvyraznit']")

                for j, tr in enumerate(trs):
                    tds = tr.find_elements(By.TAG_NAME, 'td')
                    if tds[1].text == 'T':
                        location_rec = ChmiLocationRecord(tds[0].text)
                        year_rec.add_location_rec(location_rec)
                        for td in tds[2:]:
                            location_rec.temperatures.append(
                                float(td.text.replace(',', '.'))
                            )

                year_rec.save()

                year_links = self._get_years_links()

                time.sleep(3)
            else:
                print('Skipping %s...' % year_links[i].text)

        print('all done.')

    def _get_years_links(self):
        self._driver.get(self.CHMI_DATA_MAIN_URL)
        element = self._driver.find_element(By.ID, 'loadedcontent')
        elements = element.find_elements(By.XPATH, "//table[@cellspacing='2']")

        tab1 = elements[0]
        tab2 = elements[1]
        links1 = tab1.find_elements(By.TAG_NAME, 'a')
        links2 = tab2.find_elements(By.TAG_NAME, 'a')

        return links1 + links2
