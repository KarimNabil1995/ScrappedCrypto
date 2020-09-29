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


webdriver = 'C:\\Users\Karim\Desktop\Python\Projects\BlockSpot\chromedriver.exe'
driver = Chrome(webdriver)
driver.implicitly_wait(5)

# Open up webpage, 
url = 'https://blockspot.io/exchange/'
driver.get(url)


# Select "show all results"

all_results = driver.find_element_by_xpath("//div[@class='dataTables_length']/label/select/option[5]")
all_results.click()
time.sleep(1)

links_list = []
names_list = []
countries_list = []
types_list = []
websites_list = []
statuses_list = []
twitters_list = []


# Scrolling till end of the page, grabbing hrefs of each entity 

try:
    exchanges_links = driver.find_elements_by_xpath("//tbody/tr[@role='row']/td/a")
    for link in exchanges_links:
        links_list.append(link.get_attribute('href'))
except:
    pass

# Visiting each of the grabbed Hrefs in succession to capture several data points --> 
# Entity name, registered location, exchange type,
# URLs, opertional status, twitter handles

for exchange in links_list:
    driver.get(exchange)
    time.sleep(2)
    try:
        name = driver.find_element_by_xpath("//h1").text
        country = driver.find_element_by_xpath("(//div[@class='elementor-section-wrap'])[2]/section[3]/div/div/div[1]/div/div/div[2]/div/div/a").text
        exchange_type = driver.find_element_by_xpath("(//div[@class='elementor-section-wrap'])[2]/section[3]/div/div/div[1]/div/div/div[4]/div/div").text
        website = driver.find_element_by_xpath("(//div[@class='elementor-section-wrap'])[2]/section[3]/div/div/div[2]/div/div/div[2]/div/div/a").text
        status = driver.find_element_by_xpath("(//div[@class='elementor-section-wrap'])[2]/section[3]/div/div/div[2]/div/div/div[3]/div/div").text
        twitter = driver.find_element_by_xpath("(//div[@class='elementor-section-wrap'])[2]/section[3]/div/div/div[3]/div/div/div[2]/div/div/a").get_attribute('href')
    except:
        pass
    try:
        print('exchange name is: {}'.format(name))
        print('Registered Location is : {}'.format(country))
        print('exchange type is :{}'.format(exchange_type))
        print('Exchanges status is : {}'.format(status))
        print('exchange website is :{}'.format(website))
        print('exchange twitter handle is :{}'.format(twitter))
        print('--------------')
    except:
        pass

    try:
        names_list.append(name)
        countries_list.append(country)
        types_list.append(exchange_type)
        websites_list.append(website)
        statuses_list.append(status)
        twitters_list.append(twitter)
    except:
        pass

# Saving extracted data points into a Pandas Data Frame to prepare for further analysis over the next stage

df = pd.DataFrame(list(zip(names_list, countries_list, types_list, websites_list, statuses_list, twitters_list)),
    columns=['Name', 'Country', 'Exchange Type', 'URLs', 'Service Status', 'Twitter Handle' 
 ])

Blockspot_Data = df.to_csv('Blockspot2_data.csv', index=False)




