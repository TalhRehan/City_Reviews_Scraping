from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def manual_facebook_login():
    # Launch Chrome with Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.facebook.com/login")
    print("Please log in to Facebook manually in the browser window...")
    time.sleep(90)  # Give user time to log in
    print("If logged in, you can continue. Browser will now remain open for navigation.")
    return driver
