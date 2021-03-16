import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests import Env4Dev

def getProductType(targetUrl):
    apiPath = "/gcm/product-type"
    response = requests.get(targetUrl + apiPath)
    if response.status_code != 200: 
        raise Exception("failed to check target server's product type - response is not 200 " + response.status_code)

    response_body = response.json()
    return response_body["product_type"]

def login(driver, email_id, pw):
    # todo 각 UI 엘리먼트의 속성 값을 한곳에서 
    css_loginbtn = ".MuiButton-label"
    css_welcomemsg = ".sc-fFSRdu"
    xpath_welcomemsg = "//div[@id='root']/div/p"

    # todo 현재가 로그인 페이지인지 확인하고 아니면 에러 던지기
    if driver.title != "Lunit INSIGHT Gateway Configuration Manager":
        raise Exception('Not login page!!')

    #이미 로그인 되어 있으면 바로 True 반환 
    element = driver.find_element(By.ID, "email")
    if element is None: 
        return True
    
    wait = WebDriverWait(driver, 5)
    driver.find_element(By.ID, "email").send_keys(email_id)
    driver.find_element(By.ID, "password").send_keys(pw)
    driver.find_element(By.CSS_SELECTOR, css_loginbtn).click()
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_welcomemsg))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, xpath_welcomemsg))).click()
    return True


def getDriverAndOpen():
    return getDriverAndOpenWithURL(Env4Dev.BASE_URL)

def getDriverAndOpenWithURL(toOpenURL):
    driver_path = '../drivers/chromedriver_86_win32.exe'
    if os.path.exists(driver_path):
        print(driver_path)
    else:
        driver_path = os.getcwd()+'/drivers/chromedriver_86_win32.exe'
        if os.path.exists(driver_path) == False:
            raise Exception("There is no web-driver file in " + str(driver_path))

    driver = webdriver.Chrome(driver_path)
        # os.getcwd() + '/drivers/chromedriver_86_win32.exe')
    driver.implicitly_wait(5)
    driver.get(toOpenURL)
    driver.maximize_window()

    return driver
