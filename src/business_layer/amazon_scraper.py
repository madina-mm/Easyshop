from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def get_url(search_term):
    # generate a url from search term
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"
    search_term = search_term.replace(' ', '+')
    return template.format(search_term)


def extract_records(item):
    atag = item.h2.a
    name = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        price = "no price"

    try:
        rating = item.i.text
    except AttributeError:
        rating = "no rating"

    result = {
        'name': name,
        'price': price,
        'rating': rating,
        'url': url
    }

    return result


def amazon_scraper(search_item):
    path = "C:\\Program Files (x86)\\chromedriver.exe"
    driver = webdriver.Chrome(path)

    url = get_url(search_item)
    records = []

    driver.get(url)
    while True:
        try:
            driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='a-last']/a"))))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.find_all('div', {'data-component-type': 's-search-result'})

            for item in results:
                record = extract_records(item)
                records.append(record)
            driver.find_element_by_xpath("//li[@class='a-last']/a").click()
        except (TimeoutException, WebDriverException) as e:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.find_all('div', {'data-component-type': 's-search-result'})

            for item in results:
                record = extract_records(item)
                records.append(record)
            break
    driver.quit()

    return records


if __name__ == '__main__':
    amazon_scraper()
