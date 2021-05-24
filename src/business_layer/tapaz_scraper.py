from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_url(search_term):
    # generate a url from search term
    template = "https://tap.az/elanlar?utf8=%E2%9C%93&log=true&keywords={}&q%5Bregion_id%5D="
    search_term = search_term.replace(' ', '+')
    return template.format(search_term)


def extract_records(item):
    try:
        name = item.select('a > div')[2].text.strip()
    except AttributeError:
        name = "no name"
    except IndexError:
        name = "no name"

    try:
        url = 'https://www.tap.az' + item.get('href')
    except AttributeError:
        url = "no url"
    except IndexError:
        url = "no url"

    try:
        date = item.select('a > div')[3].text.strip()
    except AttributeError:
        date = "no date"
    except IndexError:
        date = "no date"

    try:
        price = item.select('a > div')[1].findChild('span').text.strip()
    except AttributeError:
        price = "no price"
    except IndexError:
        price = "no price"

    result = {
        'name': name,
        'price': price,
        'url': url,
        'date': date
    }

    return result


def tapaz_scraper(search_item):
    path = "C:\\Program Files (x86)\\chromedriver.exe"
    driver = webdriver.Chrome(path)

    url = get_url(search_item)
    records = []

    driver.get(url)
    time.sleep(10)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "products"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('a', {'class': 'products-link'})

        for item in results:
            record = extract_records(item)
            records.append(record)

    finally:
        driver.quit()

    return records


if __name__ == '__main__':
    tapaz_scraper()
