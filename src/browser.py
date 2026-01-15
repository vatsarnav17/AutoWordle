from selenium import webdriver #engine that talks to browser
from selenium.webdriver.chrome.service import Service #chrome takes commands from driver, this gives location of driver.
from selenium.webdriver.chrome.options import Options #chrome opening options
from webdriver_manager.chrome import ChromeDriverManager #makes sure chrome sahi se chale

def create_driver():
    
    options=Options()
    options.add_argument("--start-maximised")
    options.add_argument("--disable-blink-features=AutomationControlled") #to avoid detection as bot

    service=Service(ChromeDriverManager().install()) #installs CDM, passes as Service() in variable service
    driver = webdriver.Chrome(service=service,options=options) # starts chrome
    return driver