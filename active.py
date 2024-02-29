from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.binary_location = '/usr/bin/chromium-browser'

driver = webdriver.Chrome(options=options)
driver.get("https://ipg-clone.streamlit.app/")
time.sleep(5)
print("5 secs - igp")
print(driver.title)
driver.quit()



driver = webdriver.Chrome(options=options)
driver.get("https://imporatations-peru-calculator.streamlit.app/")
time.sleep(5)
print("5 secs - calculator")
print(driver.title)
driver.quit()
