#-*- coding: utf-8 -*-
import unittest

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests import Env4Dev
from tests import SharedFunc


class LoginTestCase(unittest.TestCase):
    xpath_logoutbtn = "(//button[@type='button'])[2]"
    css_loginbtn = ".MuiButton-label"
    css_welcomemsg = ".sc-fFSRdu"
    # css_failmsg = "p:nth-child(0)"
    xpath_failmsg = "//div[@id='root']/div/div/form/div[3]/p"
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = SharedFunc.getDriverAndOpen()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        # TODO 대상 브라우저 종류와 버전 정보에 따라 driver 로드
        # 로그아웃 버튼이 보이면, 로그아웃 수행
        elements = self.driver.find_elements(By.XPATH, self.xpath_logoutbtn)
        if len(elements) > 0:
            elements[0].click()

    def tearDown(self):
        # TODO 테스트 수행 후 브라우저를 닫을 것인지를 별도 변수를 통해
        # TODO 매 로그인 테스트 수행 후 로그아웃을 해 놓을 것인지
        # self.driver.quit()
        print("Tests tearDown")

    def test_login_200ok(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)
        # 1) 로그인 페이지인지 확인 - TODO 보다보니 GCM 전체 타이틀이 동일한 것 같음
        wait.until(EC.title_is("Lunit INSIGHT Gateway Configuration Manager"))
        self.assertIn(
            "Lunit INSIGHT Gateway Configuration Manager", driver.title)

        # 2) 비로그인 상태인지(아이디 입력 필드) 확인
        element = driver.find_element(By.ID, "email")
        self.assertIsNotNone(element, "로그인을 할 수 없습니다")

        # 3) 아이디, 비밀번호 넣고 로그인 시도
        driver.find_element(By.ID, "email").send_keys(Env4Dev.EMAILID)
        driver.find_element(By.ID, "password").send_keys(Env4Dev.PASSWD)
        driver.find_element(By.CSS_SELECTOR, self.css_loginbtn).click()

        # 4) 로그인 성공 확인
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.css_welcomemsg)))
        self.assertEqual("Welcome, lunit!", driver.find_element(
            By.CSS_SELECTOR, self.css_welcomemsg).text)

    def test_login_wrongpw(self):
        driver = self.driver
        wait = WebDriverWait(driver, 4)
        # 1) 로그인 페이지인지 확인 - TODO 보다보니 GCM 전체 타이틀이 동일한 것 같음
        wait.until(EC.title_is("Lunit INSIGHT Gateway Configuration Manager"))
        self.assertIn(
            "Lunit INSIGHT Gateway Configuration Manager", driver.title)

        # 2) 비로그인 상태인지(아이디 입력 필드) 확인
        element = driver.find_element(By.ID, "email")
        self.assertIsNotNone(element, "로그인을 할 수 없습니다")

        # 3) 아이디, 비밀번호 넣고 로그인 시도
        driver.find_element(By.ID, "email").send_keys(Env4Dev.EMAILID)
        driver.find_element(By.ID, "password").send_keys("wrong_passwd!@")
        driver.find_element(By.CSS_SELECTOR, self.css_loginbtn).click()

        # 4) 실패 메시지 영역, 텍스트 확인 <- TODO 테스트를 짧은 시간에 반복 수행시 실패 메시지 내용이 바뀔 수 있음. 발생시 수정 검토
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath_failmsg)))
        self.assertEqual("Please enter the correct email and password for an account. Note that both fields may be case-sensitive.", driver.find_element(By.XPATH, self.xpath_failmsg).text)

    def test_login_accountlock(self):
        driver = self.driver
        xpath_failmsg = self.xpath_failmsg

        wait = WebDriverWait(driver, 5)
        ##### 1번째 틀린 비밀번호 #####
        # 1) 로그인 페이지인지 확인 - TODO 보다보니 GCM 전체 타이틀이 동일한 것 같음
        wait.until(EC.title_is("Lunit INSIGHT Gateway Configuration Manager"))
        self.assertIn(
            "Lunit INSIGHT Gateway Configuration Manager", driver.title)
        # 2) 비로그인 상태인지(아이디 입력 필드) 확인
        element = driver.find_element(By.ID, "email")
        self.assertIsNotNone(element, "로그인을 할 수 없습니다")
        # 3) 아이디, 비밀번호 넣고 로그인 시도
        driver.find_element(By.ID, "email").send_keys(Env4Dev.EMAILID)
        driver.find_element(By.ID, "password").send_keys("wrong_passwd!@")
        driver.find_element(By.CSS_SELECTOR, self.css_loginbtn).click()
        # 4) 실패 메시지 영역, 텍스트 확인 <- TODO 테스트를 짧은 시간에 반복 수행시 실패 메시지 내용이 바뀔 수 있음. 발생시 수정 검토
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_failmsg)))
        self.assertEqual("Please enter the correct email and password for an account. Note that both fields may be case-sensitive.", driver.find_element(By.XPATH, xpath_failmsg).text)
        
        ##### 2번째 틀린 비밀번호 #####
        element = driver.find_element(By.ID, "email")
        element.clear()
        element.send_keys(Env4Dev.EMAILID)
        driver.find_element(By.ID, "password").send_keys("wrong_passwd!@")
        driver.find_element(By.CSS_SELECTOR, self.css_loginbtn).click()
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath_failmsg)))

        self.assertEqual("Please enter the correct email and password for an account. Note that both fields may be case-sensitive.", driver.find_element(By.XPATH, xpath_failmsg).text)
        ##### 3번째 틀린 비밀번호 #####
        element = driver.find_element(By.ID, "email")
        element.clear()
        element.send_keys(Env4Dev.EMAILID)
        driver.find_element(By.ID, "password").send_keys("wrong_passwd!@")
        driver.find_element(By.CSS_SELECTOR, self.css_loginbtn).click()
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_failmsg)))
        # assert 생략 

        # 4번째 틀린 비밀번호
        element = driver.find_element(By.ID, "email")
        element.clear()
        element.send_keys(Env4Dev.EMAILID)
        driver.find_element(By.ID, "password").send_keys("wrong_passwd!@")
        driver.find_element(By.CSS_SELECTOR, self.css_loginbtn).click()
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_failmsg)))
        self.assertIsNotNone(element)
        # assert 생략, 바뀔 수 있음

        # 5번째 정상 로그인 시도
        element = driver.find_element(By.ID, "email")
        element.clear()
        element.send_keys(Env4Dev.EMAILID)
        element = driver.find_element(By.ID, "password")
        element.clear()
        element.send_keys(Env4Dev.PASSWD)
        driver.find_element(By.CSS_SELECTOR, self.css_loginbtn).click()
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_failmsg)))
        self.assertTrue('Please try again in 60 seconds and don’t refresh this page' in driver.find_element(By.XPATH, xpath_failmsg).text)
        self.assertIsNotNone(element)
        # assert 생략, 바뀔 수 있음
        
        # 61초 기다리고 정상 로그인 시도
        time.sleep(61)
        element = driver.find_element(By.ID, "email")
        element.clear()
        element.send_keys(Env4Dev.EMAILID)
        element = driver.find_element(By.ID, "password")
        element.clear()
        element.send_keys(Env4Dev.PASSWD)
        driver.find_element(By.CSS_SELECTOR, self.css_loginbtn).click()
        element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.css_welcomemsg)))
        self.assertEqual("Welcome, lunit!", element.text)


if __name__ == "__main__":
    unittest.main()
