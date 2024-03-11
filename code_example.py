#scraper avec selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import requests as r

#for holding result
all_links = []
page_url = "https://xpareto.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}
req = r.get(page_url, headers=headers)
#scrap the first page using beautifulsoup and store all data to table
if req.status_code == 200:
    soup = BeautifulSoup(req.content, 'html.parser')
    #scrap the data relative to the url's
    adresses = []
    
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(page_url)
time.sleep(5)
next_page = driver.find_element(By.XPATH, '/html/body/div/div/form/big/div/table/tbody/tr/td[2]/div[1]/center/a[6]').click()

