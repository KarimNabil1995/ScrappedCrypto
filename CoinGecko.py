from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import selenium.common.exceptions as exception



options = Options()
options.headless = True

webdriver = 'C:\\Users\Karim\Desktop\Python\Projects\CoinGecko\chromedriver.exe'
driver = Chrome(webdriver)



num_of_pages = 4
exchanges_list = []
names_list = []
websites_list = []
emails_list = []
years_list = []
countries_list = []
twitter_list = []

# Visit the following link and fully iterate through the 4 pages list of exchanges listed on the website 
# & save them into the links variable 

for i in range(num_of_pages):

    url = 'https://www.coingecko.com/en/exchanges?page=' + str(i+1)
    driver.get(url)
    driver.manage().windows().maximize()


    links = driver.find_elements_by_xpath("//tbody[@data-target='exchanges-list.tableRows']/tr/td[2]/div/span[2]/a")
    links = [url.get_attribute('href') for url in links]
    time.sleep(0.5)

    # Visit the captured href of each crawled entity -- from previous homepage -- to scrap further data data points.
    # First find tab labelled "about", click on it to land on the page providing further details about each exchange
    

    for link in links:
        time.sleep(1)
        driver.get(link)
        try: 
            wait = WebDriverWait(driver, 4)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '#about')]")))
            driver.execute_script("arguments[0].scrollIntoView()", element)
            element.click()
        except:
            pass
        
        # once navigated to the 'about' tab, start scraping desired data points -->
        # entity name, url, email, year established, incorporated country, twitter handle 

        try:
            time.sleep(1)
            name = driver.find_element_by_xpath("//div[@class='exchange-details-header-content']/div/h1").text
            website = driver.find_element_by_xpath("//div[@class='row no-gutters']/div[8]/a").get_attribute('href')
            email = driver.find_element_by_xpath("//div[@class='row no-gutters']/div[9]/a").get_attribute('href')
            year_est = driver.find_element_by_xpath("//div[@class='row no-gutters']/div[10]").text
            Inc_country = driver.find_element_by_xpath("//div[@class='row no-gutters']/div[12]").text
            twitter = driver.find_element_by_xpath("//div[@class='row no-gutters']/div[16]/div[2]/div[2]/a").get_attribute('title')
            time.sleep(1)

        except:
            pass
        try:
            
            print('exchange name is : {}'.format(name))
            print('exchange website is : {}'.format(website))
            print('exchange email is : {}'.format(email))
            print('exchange established in year: {}'.format(year_est))
            print('exchange incorporated in : {}'.format(Inc_country))
            print('exchange twitter handle is: {}'.format(twitter))
            print('---------------')
        except:
            pass

        try:
            names_list.append(name)
            websites_list.append(website)
            emails_list.append(email)
            years_list.append(year_est)
            countries_list.append(Inc_country)
            twitter_list.append(twitter)
        except:
            pass
        
# Once all data is retreieved, save gathered info into a pandas Dataframe, 
# & convert into an excel spreadsheet that will be utilised for further analysis


df = pd.DataFrame(list(zip(names_list, websites_list,emails_list, years_list, countries_list, twitter_list)), columns=['Ex_Names', 'Website', 'Support Email', 'Inc Year', 'Inc Country', 'Twitter Handle' ])

CoinGecko2_data = df.to_csv('CoinGecko5.csv', index=False) 

 
  