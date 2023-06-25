import time                                             # Para control de pausas
from bs4 import BeautifulSoup                           # Para hermosear HTMLs
from selenium import webdriver                          # Para realizar web scraping
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import uf
import producto

def outputHtml(sFile, lxmlData):
    fOutputHtml = open (sFile,'w')
    fOutputHtml.write(lxmlData.prettify())
    fOutputHtml.close()

def mySleep(nTimeOut):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    while (nTimeDifference < nTimeOut):
        nTimeDifference = time.time() - nTimeInit

# MAIN
if (__name__ == "__main__"):
    # Driver y carga de página
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://simple.ripley.cl/')
    mySleep(2)

    #
    # Obtener UF por content Selenium + lxml BeautifulSoup

    inputText = driver.find_element(By.XPATH, '/html/body/div[5]/header/section/nav/ul/li[1]/div/div[1]/input')
    inputText.send_keys('notebook hp')
    inputText.send_keys(Keys.ENTER)
    #
    mySleep(2)
    sXpath = '/html/body/div[9]/div[2]/div/div[2]/div[3]/section/div/div' 
    contentData = driver.find_element(By.XPATH, sXpath)
    htmlData = contentData.get_attribute('innerHTML')
    lxmlData = BeautifulSoup(htmlData, 'lxml')
    outputHtml('ripley.html', lxmlData)