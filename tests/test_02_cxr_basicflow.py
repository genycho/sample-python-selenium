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


class CXR3BasicFlowTestCase(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        productType = SharedFunc.getProductType(Env4Dev.BASE_URL)
        if(productType != 'cxr3'):
            raise Exception("대상 사이트가 cxr3가 아니어서 테스트 수행이 불가합니다. productType = " + productType)

        cls.driver = SharedFunc.getDriverAndOpen()
        SharedFunc.login(cls.driver, Env4Dev.EMAILID, Env4Dev.PASSWD)

    @classmethod
    def tearDownClass(cls):
        # cls.driver.quit()
        print("The end")

    def setUp(self):
        element = self.driver.find_element(By.CSS_SELECTOR, "div.MuiButtonBase-root > svg")
        if element != None: 
            element.click()

    # def tearDown(self):

    def test_basicflow_01(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)
        # 1) Network
        xpath_title = "//div[@id='root']/div/div[2]/form/div/p"
        xpath_modality_title = "//div[@id='root']/div/div[2]/form/div/p[2]"
        xpath_insightapp_title = "//div[@id='root']/div/div[2]/form/div/p[3]"
        xpath_destination_title = "//div[@id='root']/div/div[2]/form/div/p[4]"

        wait.until(EC.title_is("Lunit INSIGHT Gateway Configuration Manager"))
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_title)))
        self.assertEqual("Identify your network setting", element.text)
        # 1-1) Modality allowlist
        element = driver.find_element(By.XPATH, xpath_modality_title)
        # TOCHECK : allow modality count가 -1인 경우는 해당 영역이 표시되지 않음
        print("Modality allowlist area checking..." + element.text)
        if element.text == "Where does Lunit GW receive the DICOM to analyze from?": 
            print("modality allowlist exist.")
            element = driver.find_element(By.ID, "modalityAllowList[0].aeTitle")
            element.clear()
            element.send_keys("LUNIT1")
            element = driver.find_element(By.ID, "modalityAllowListp0].ipAddress")
            element.clear()
            element.send_keys("10.120.0.11")
        else: 
            print("no modal settings")

        # 1-2) Insight APP server info
        # NOTFOUND http 콤보 잘못찾아짐
        # element = driver.find_element(By.XPATH, "//div[@id='menu-inferenceServer.insightApiProtocol']/div")
        # element.click()
        # 임시. 데모용 1초 보여주기
        time.sleep(1)
        element = driver.find_element(By.ID, "inferenceServer.insightApiHost")
        element.clear()
        element.send_keys("10.120.0.11")
        element = driver.find_element(By.ID, "inferenceServer.insightApiPort")
        element.clear()
        element.send_keys("8001")
        element = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/div[2]/ul/li[4]/button/span")
        element.click()
        # TODO: check the msg box success 
        element = driver.find_element(By.XPATH, "//div[@id='root']/div/div[3]/div")
        if element != None:
            self.assertEqual("INSIGHT API server is found successfully.", element.text)

        element = driver.find_element(By.ID, "inferenceServer.insightApiKey")
        element.clear()
        element.send_keys("test_key")
        
        # 1-3) output 
        element = driver.find_element(By.ID, "aeTitle")
        element.clear()
        element.send_keys("LUNIT2")
        element = driver.find_element(By.ID, "ipAddress")
        element.clear()
        element.send_keys("10.120.0.11")
        element = driver.find_element(By.ID, "port")
        element.clear()
        element.send_keys("30001")
        # 포커스 아웃을 위한 임의 클릭 추가
        driver.find_element(By.XPATH, xpath_destination_title).click()
        
        xpath_first_nextbtn = "//div[@id='root']/div/div[2]/form/button/span"
        element = driver.find_element(By.XPATH, xpath_first_nextbtn)
        # 왜 클릭이 안 되지??? 
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_first_nextbtn)))
        element.click()
        
        # 2) Output DICOM
        wait.until(EC.presence_of_element_located((By.NAME, "dicomFormat.createSc")))
        # sc 체크박스
        element = driver.find_element(By.NAME, "dicomFormat.createSc")
        if element.is_selected() != True:
            element.click()

        element = driver.find_element(By.NAME, "dicomFormat.scHeatmapType")
        element = driver.find_element(By.XPATH, "(//input[@name='dicomFormat.scHeatmapType'])[4]")
        if element.is_selected() != True:
            element.click()
        ### DISPLAY MODE ###
        element = driver.find_element(By.NAME, "cxrScFormat.scTypes.map")
        if element.is_selected() != True:
            element.click()
        element = driver.find_element(By.NAME, "cxrScFormat.scTypes.report")
        if element.is_selected() != True:
            element.click()

        element = driver.find_element(By.NAME, "dicomFormat.createGsps")
        if element.is_selected() != True:
            element.click()

        element = driver.find_element(By.NAME, "dicomFormat.createGsps")
        if element.is_selected() != True:
            element.click()
        # 언어 선택 콤보박스... NOTFOUND - body 가 잡힘
        # element = driver.find_element(By.XPATH, "//div[@id='menu-languageType']/div")
        # from selenium.webdriver.support.select import Select
        # select_fr = Select(driver.find_element_by_xpath("//div[@id='menu-languageType']/div"))
        # select_fr.select_by_index(5)

        # 병증 선택.... lesion names 영역 확인
        lesion_title_area = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/div[3]/p")
        if lesion_title_area == None:
            raise Exception("There is no lesion names title area!!")

        # element = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/div[3]/div/div/label/span[2]/span")
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'atelectasis')]")
        if element != None and element.is_selected() != True:
            element.click()
        # element = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/div[3]/div/div/label[3]/span[2]/span")
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'calcificatio')]")
        if element != None and element.is_selected() != True:
            element.click()
        # element = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/div[3]/div/div/label[5]/span[2]/span")
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'consolidation')]")
        if element != None and element.is_selected() != True:
            element.click()
        # element = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/div[3]/div/div/label[5]/span[2]/span")
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'nodule')]")
        if element != None and element.is_selected() != True:
            element.click()
        # element = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/div[3]/div/div/label[7]/span[2]/span")
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'pneumothorax')]")
        if element != None and element.is_selected() != True:
            element.click()
        # element = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/div[3]/div/div/label[9]/span[2]/span")
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'pneumoperitoneum')]")
        if element != None and element.is_selected() != True:
            element.click()
        
        # 포커스 아웃을 위한 임의 클릭 
        # lesion_title_area.click()
        xpath_second_nextbtn = "//div[@id='root']/div/div[2]/form/div[2]/button[2]/span"
        # wait.until(EC.element_to_be_clickable((By.XPATH, xpath_second_nextbtn)))
        element = driver.find_element(By.XPATH, xpath_second_nextbtn)
        element.click()
        
        # 3) Output DICOM
        # 웨이트 살짝? 
        # include에 한건 선택
        # exclude에 한건 선택
        # exclude에 추가된 것 확인 
        # include 삭제
        # exclude 삭제
        xpath_filter_text_area = "//div[@id='root']/div/div[2]/form/div/p[2]"

        id_include_address = "include.address"
        id_include_value = "include.value"
        xpath_include_addbtn = "xpath=(//button[@type='button'])[3]"
        
        id_exclude_address = "id=exclude.address"
        id_exclude_value = "id=exclude.address"
        xpath_exclude_addbtn = "xpath=(//button[@type='button'])[4]"

        
        xpath_added_includelist = "//div[@id='root']/div/div[2]/form/div/ul[2]/li"
        xpath_added_includelist_tag = "//div[@id='root']/div/div[2]/form/div/ul[2]/li/span"
        xpath_added_includelist_value = "//div[@id='root']/div/div[2]/form/div/ul[2]/li/span[2]"

        xpath_added_excludelist = "//div[@id='root']/div/div[2]/form/div/ul[4]/li"
        xpath_added_excludelist_tag = "//div[@id='root']/div/div[2]/form/div/ul[4]/li/span"
        # //div[@id='root']/div/div[2]/form/div/ul[4]/li[2]/span
        xpath_added_excludelist_value = "//div[@id='root']/div/div[2]/form/div/ul[4]/li/span[2]"
        # //div[@id='root']/div/div[2]/form/div/ul[4]/li[2]/span[2]
        
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_filter_text_area)))
        # 현재 include 필터 갯수 체크
        include_ulelement = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/ul[2]")
        count_included_element = self.li_count(include_ulelement)
        
        # include 추가
        element = driver.find_element(By.ID, id_include_address)
        element.send_keys("00010001")
        element = driver.find_element(By.ID, id_include_value)
        element.send_keys("test")
        element = driver.find_element(By.XPATH, xpath_include_addbtn)
        element.click()

        # exclude 추가
        element = driver.find_element(By.ID, id_exclude_address)
        element.send_keys("00010001")
        element = driver.find_element(By.ID, id_exclude_value)
        element.send_keys("test")
        element = driver.find_element(By.XPATH, xpath_exclude_addbtn)
        element.click()

        # 현재 exclude 필터 갯수 체크
        exclude_ulelement = driver.find_element(By.XPATH, "//div[@id='root']/div/div[2]/form/div/ul[4]")
        count_excluded_element = self.li_count(exclude_ulelement)


        # include, exclude삭제


        # Next




        print("Debugging...")

    def li_count(self, ul_element):
        li_elements = ul_element.find_elements_by_tag_name("li")
        count_li_elements = 0
        if li_elements != None:
            count_li_elements = len(li_elements)
        return count_li_elements

if __name__ == "__main__":
    unittest.main()
