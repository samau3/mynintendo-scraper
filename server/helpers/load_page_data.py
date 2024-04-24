from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def load_page_data(url, tag):
    """ Function to load a webpage and wait for a specific tag to load"""
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, tag)))

    return driver.page_source