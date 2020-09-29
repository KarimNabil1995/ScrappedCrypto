from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import json
import selenium.common.exceptions as exception

from selenium.common.exceptions import TimeoutException


webdriver = '/Users/karimnabil/projects/selenium_js/chromedriver-1'
driver = Chrome(webdriver)
driver.implicitly_wait(5)

url = 'https://acceptedhere.io/catalog/company/'
driver.get(url)


btc = driver.find_element_by_xpath("//ul[@role='currency-list']/li[1]/a")
btc.click()
time.sleep(1)

eth = driver.find_element_by_xpath("//ul[@role='currency-list']/li[2]/a")
eth.click()
time.sleep(1)

bch = driver.find_element_by_xpath("//ul[@role='currency-list']/li[3]/a")
bch.click()
time.sleep(1)

all_categories = driver.find_element_by_xpath("//div[@class='dropdownMenu']/ul/li[1]")
all_categories.click()

time.sleep(1)
maximum_number = 620

companies_list = []
names_list = []
focus_list = []
location_list = []
coins_list = []



while True:

    wait = WebDriverWait(driver, 2)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='row search-result']/div[3]/button")))
    show_more = driver.find_element_by_xpath("//div[@class='row search-result']/div[3]/button")

    # WebDriverWait.
    elements = driver.find_elements_by_xpath("//div[@class='row desktop-results mobile-hide']/div")
    if len(elements) > maximum_number:
        break
    show_more.click()
    time.sleep(1)


    
wait = WebDriverWait(driver, 2)
wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='row desktop-results mobile-hide']/div/div/div/div[2]/div/div/div[1]/a")))

company_links = driver.find_elements_by_xpath("//div[@class='row desktop-results mobile-hide']/div/div/div/div[2]/div/div/div[1]/a")
for link in company_links:
    try:
        companies_list.append(link.get_attribute('href'))
    except exception.StaleElementReferenceException:
        print('stale element')

with open("companies_list.json", "w") as f:
    json.dump(companies_list, f)

with open("companies_list.json", "r") as f:
    companies_list = json.load(f)



for company in companies_list:
    try:  
        driver.get(company)
    except:
        pass
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//h1/span")))
        name = driver.find_element_by_xpath("//h1/span").text
    except:
        pass

    try:
        locations = driver.find_element_by_xpath("//div[@class='breadcrumbs']").text
    except:
        print('Unknown location')

    try:
        focuses = []
        categories = driver.find_elements_by_xpath("//div[@class='card-category']/a")
        for category in categories:
            focuses.append(category.text)
    except:
        print('Category not foound')

    try:
        coins = []
        accepted_crypto = driver.find_elements_by_xpath("//a[contains(@class, 'accepted-here-details')]")
        for coin in accepted_crypto:
            coins.append(coin.text)
    except:
        print('no coins found')


    try:
        print('company name is: {}'.format(name))
        print('location registered is in:{}'.format(locations))
        print('Categories registed are: {}'.format(focuses))
        print('Accepted Crypto is : {}'.format(coins))
    except:
        pass
    time.sleep(2)
    try:
        names_list.append(name)
        focus_list.append(focuses)
        location_list.append(locations)
        coins_list.append(coins)
    except:
        pass



df = pd.DataFrame(list(zip(names_list, location_list, focus_list, coins_list)), columns=['Company name', 'Registered Location', 'Focus', 'Accepted Crypto' ])

Accepted_here_Data = df.to_csv('Accepted_Here5.csv', index=False) 
    
    