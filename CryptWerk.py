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
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


webdriver = 'C:\\Users\Karim\Desktop\Python\Projects\CryptoWerk\chromedriver.exe'
driver = Chrome(webdriver)
driver.implicitly_wait(2)
driver.maximize_window()

# Load up following URL

url = 'https://cryptwerk.com/companies/?coins=1,6,11,2,3,8,17,7,13,4,25,29,24,32,9,38,15,30,43,42,41,12,40,44,20'
driver.get(url)
links_list11 = []
coins_list = []


all_names = []
all_cryptos = []
all_links = []
all_twitter = []
all_locations = []
all_categories = []
all_categories2 = []
all_urls = []

# Continue scrolling to the end of page via a while loop. Clicks 'show more' button, waits 5 seconds and if maximum number hasn't been reached yet
# repeats the process until condition is fullfilled
# Stops scrolling and hitting the 'show more' button once the maximum number of company links have been retrieved -- 5930

maximun_number = 5900
c_number = 0
while True:
    try:
        wait = WebDriverWait(driver, 2)
        show_more = wait.until(EC.presence_of_element_located((By.XPATH, "//form[@class='paginator-infinity text-center text-muted']/button[@type='submit']")))
        elements = driver.find_elements_by_xpath("//div[contains(@class,'media item')]")
        if len(elements) > maximun_number:
            break
        show_more.click()
        wait.until(EC.url_to_be(url))
    except TimeoutException as ex:
        isrunning = 0
        print("Exception has been thrown. " + str(ex))
        


print('Proceeding to scrapping data points')

# Saving list of company hrefs in a json format due to the highly congested bandwidth of the website.
# More efficient to iterate through the json array of company links

try:
    company_links = driver.find_elements_by_xpath("//div[@class='companies-list items-infinity']/div[position() >3900 and position() <5900]/div[@class='media-body']/div[@class='title']/a")
    for link in company_links:
        links_list11.append(link.get_attribute('href'))
except:
    pass

try:
    with open("links_list11.json", "w") as f:
        json.dump(links_list11, f)

    with open("links_list11.json", "r") as f:
        links_list11 = json.load(f)
except:
    pass
    
try:
    for link in links_list11:
        driver.get(link)
        
        # visit scrapped internal url of each entity -- inside of cryptwerk 
        # then jump another latency point to reach the actual website of each correspoding for retireving the full link 
        # since its a redirect through the website's server

        try:
            website = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='company-website mt-2']/a"))).get_attribute("href")
            driver.get(website)
            company_url = driver.current_url
        except:
            pass
        try:
            driver.back()
            name = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='title']/h1"))).text
        except:
            pass

        # Click on show_more button to display full list of supported cryptocurrencies

        try:
            show_more_coins = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-original-title='Show more']")))
            show_more_coins.click()
        except:
            pass
        
        # Scrapping both instances of categories(Top-page // Bottom=page) OR industires on each corresponding page
        # as sometimes one were found and not the other

        try:
            categories = driver.find_elements_by_xpath("//div[contains(@class, 'categories-list')]/a")
            categories_list = []
            for category in categories:
                categories_list.append(category.text)
        except:
            pass
        try:
            top_page_categories = driver.find_elements_by_xpath("//ol[@class='breadcrumb']/li/a")
            top_page_categories_list = []
            for category in top_page_categories:
                top_page_categories_list.append(category.text)
        except:
            pass


        coins_links = driver.find_elements_by_xpath("//div[contains(@class, 'company-coins')]/a")
        all_coins = []
        for coin in coins_links:
            all_coins.append(coin.get_attribute('href'))
        try:
            location = driver.find_element_by_xpath("//div[@class='addresses mt-3']/div/div/div/div/a").text
        except:
            location = 'No location registered'
            pass

        try:
            twitter = driver.find_element_by_xpath("//div[@class='links mt-2']/a[2]").get_attribute('href')
        except:
            twitter = 'No handle found'
            pass
        c_number +=1
            
        try:
            print('-----------')
            print('Company number is {}'.format(c_number))
            print('company website is: {}'.format(company_url))
            print('Company name is: {}'.format(name))
            print('Potential Categories are: {}'.format(categories_list))
            print('Potential top page categories are: {}'.format(top_page_categories_list))
            print('Supporting Crypto is:{}'.format(all_coins))
            print('Registered location is: {}'.format(location))
            print('Company twitter profile is: {}'.format(twitter))
            time.sleep(1)
        except:
            pass

        all_names.append(name)
        all_urls.append(company_url)
        all_categories.append(categories_list)
        all_categories2.append(top_page_categories_list)
        all_cryptos.append(all_coins)
        all_twitter.append(twitter)
        all_locations.append(location)



except:
    pass


try:
    df = pd.DataFrame(list(zip(all_names, all_urls, all_categories, all_categories2, all_cryptos, all_twitter, all_locations)), columns=['Company name', 'Company Website', 'Categories1', 'Categories2', 'Supporting Crypto', 'Twitter Handle', 'Registered Location'])

    CryptoWerk_Data = df.to_csv('CryptoWerk-pls3.csv', index=False) 
except:
    pass
        




    