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


webdriver = 'C:\\Users\Karim\Desktop\Python\Projects\CryptoSlate\chromedriver.exe'
driver = Chrome(webdriver)
driver.implicitly_wait(5)

# Visit following page
url = 'https://www.cryptoatlas.io/rankings'
driver.get(url)
driver.implicitly_wait(5)


links_list = []
all_names = []
all_urls = []
all_categories = []
all_twitter = []

# Grab the href link of each of the categories listed -- Venture Capital firms, exchanges, etc ..
# and save them to an array for which it will be iterated over next

try:
    rankings_links = driver.find_elements_by_xpath("(//div[@class='container'])[2]/div/div/section/div/div/a")
    for link in rankings_links:
        links_list.append(link.get_attribute('href'))
except:
    pass


# Visit corresponding URL of each of the categories to begin scraping seperate href for each company/entity

for category in links_list:
    driver.get(category)
    time.sleep(2)

    wait = WebDriverWait(driver, 4)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ProductsList_title')]/a")))
    companies = driver.find_elements_by_xpath("//div[contains(@class, 'ProductsList_title')]/a")
    companies = [company.get_attribute('href') for company in companies]
    time.sleep(2)
    
    # once hrefs are loaded, visit each one respetively and begin extracting required data points 
    for company in companies:
        categories_list = []
        names_list = []
        driver.get(company)
        wait = WebDriverWait(driver, 4)
        
        #Company's name
        name = driver.find_element_by_xpath("//div[contains(@class, 'ProductHero_titleLine')]/h5").text

        # Company Website
        url = driver.find_element_by_xpath("//div[contains(@class, 'ProductHero_socialProfiles')]/a").text

        # Company social profiles if exist
        try:
            twitter_handle = driver.find_element_by_xpath("//div[contains(@class, 'ProductHero_socialProfiles')]/a[2]").get_attribute('href')
        except:
            twitter_handle = 'Not known'

        # Company Focuses or categories
        categories_list = []
        categories = driver.find_elements_by_xpath("//div[contains(@class, 'ProductHero_titleLine')]/div[2]/a/div")
        for focus in categories:
            categories_list.append(focus.text)


        print('Company name is : {}'.format(name))
        print('Company website is: {}'.format(url))
        print('Company focus is : {}'.format(categories_list))
        print('Company Twitter Handle is: {}'.format(twitter_handle))
        print('------')
        time.sleep(2)

        try:
            all_names.append(name)
            all_categories.append(categories_list)
            all_urls.append(url)
            all_twitter.append(twitter_handle)
        except:
            pass
# Save extracted data into a DataFrame, convert to CSV to prepare for further analysis down the road

df = pd.DataFrame(list(zip(all_names, all_categories, all_urls, all_twitter)), columns=['Company Name', 'Categories', 'URLs', 'Twitter Handle' ])

CryptoSlate_Data = df.to_csv('CryptoSlate_data.csv', index=False)
       
        

