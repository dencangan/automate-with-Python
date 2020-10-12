"""
Script to scrape amazon deals.
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class AmazonDeals:

    def __init__(self, num_pages, search_product):
        """Class containing parameters

        Args
            num_pages (int): Number of pages to scrape
            search_product (str): Product to search
        """

        self.search_product = search_product
        self.num_pages = num_pages
        self.amazon_link = 'https://www.amazon.co.uk/'

    def run(self):
        """Full run on scraping product details, returns pandas data frame"""

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(r"C:\Users\Dencan Gan\AppData\Local\selenium_driver\chromedriver.exe",
                                  options=options)

        driver.get(self.amazon_link)
        element = driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_product)
        element.send_keys(Keys.ENTER)

        self.num_pages += 2
        lst_pages = [x for x in list(range(self.num_pages))][2:]

        full_lst = []

        for page in lst_pages:
            driver.get(driver.current_url + "&page=" + str(page))

            for i in driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]'):

                counter = 0

                for element in i.find_elements_by_xpath(
                        '//div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div/a'):

                    name = i.find_elements_by_tag_name('h2')[counter].text

                    price = element.find_element_by_class_name('a-price').text.replace('\n', '.')

                    link = i.find_elements_by_xpath('//h2/a')[counter].get_attribute("href")

                    try:
                        prev_price = element.find_element_by_class_name('a-text-price').text.replace('\n', '.')

                    except NoSuchElementException:
                        prev_price = 'None'

                    data = [name, price, prev_price, link]
                    full_lst.append(data)

                    counter += 1

        full_lst = [j for i in full_lst for j in i]

        data = {}
        for i, e in enumerate(['Name', 'Current Price', 'Previous Price', 'Link']):
            data[e] = full_lst[i::4]

        df = pd.DataFrame(data)
        driver.close()
        return df


if __name__ == '__main__':

    deals = AmazonDeals(num_pages=1, search_product='skipping ropes')
    df = deals.run()