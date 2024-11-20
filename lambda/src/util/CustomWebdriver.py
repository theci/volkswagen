from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import *
from tempfile import mkdtemp
from util.QuickSightElement import QuickSightElement

class CustomWebdriver:
    driver = None
    logger = None
    def __init__(self,result_dir,logger):
        """initialize webdriver
        :param result_dir: download directory
        :param logger: logger object
        """

        self.options = webdriver.ChromeOptions() 
        self.service = webdriver.ChromeService("/opt/chromedriver")
        self.options.binary_location = "/opt/chrome/chrome"
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--single-process")
        self.options.add_argument("--no-zygote")
        self.options.add_argument("--disable-dev-tools")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument(f"--user-data-dir={mkdtemp()}")
        self.options.add_argument(f"--data-path={mkdtemp()}")
        self.options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        self.options.add_argument("--remote-debugging-port=9230")
        self.options.add_experimental_option("prefs", {"download.default_directory": result_dir})
        self.QE = QuickSightElement()
        self.elemtype = {"ID":By.ID, "XPATH":By.XPATH, "CSS":By.CSS_SELECTOR }

        self.driver = webdriver.Chrome(service=self.service ,options=self.options)
        self.driver.implicitly_wait(30)
        self.errors = [NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException]
        self.wait_5s = WebDriverWait(self.driver, timeout=5, poll_frequency=.2, ignored_exceptions=self.errors)
        self.wait_1s = WebDriverWait(self.driver, timeout=1, poll_frequency=.2, ignored_exceptions=self.errors)
        self.logger = logger

    def getDriver(self) -> None:
        """get Selenium WebDriver
        :return: webdriver Object
        """
        return self.driver

    # 웹 경로(key)를 사용하여 해당 웹 요소를 찾고, 선택적으로 idx를 사용하여 여러 요소 중 특정 인덱스의 요소를 클릭합니다. 
    # idx가 없으면 첫 번째 요소를 클릭하고, idx가 있으면 그 인덱스에 맞는 요소를 클릭합니다. 클릭이 성공적으로 이루어지면 True를 반환하고, 그렇지 않으면 False를 반환합니다.
    def clickWebDriver(self, key:str ,idx:str=None) -> bool:
        """click element

        :param key: get Web path with key param
        :param idx: Default is None if idx not none change web_path string with idx param
        :return bool
        """

        by,web_path = self.getPathInfo(key)  # key를 받아서 해당하는 웹 경로(web_path)와 찾을 방법(예: By.ID, By.XPATH, By.CSS_SELECTOR 등을 반환합니다).
        self.logger.debug(f"{by} | {web_path} | {idx}") # 디버그 로그를 남깁니다. 이 로그에는 by (경로 방법), web_path (경로 값), 그리고 idx (인덱스)가 기록됩니다
        if idx == None: # idx가 제공되지 않으면 web_path를 그대로 사용하여 요소를 찾습니다.
            return self.wait_1s.until(lambda d : d.find_element(self.elemtype[by], web_path).click() or True) # by와 web_path를 사용하여 웹 요소를 찾습니다. self.elemtype[by]는 By.ID, By.XPATH 등으로 해당 방법을 지정합니다.
        else :
            return self.wait_1s.until(lambda d : d.find_element(self.elemtype[by], web_path.format(idx=idx)).click() or True)

    def sendKeysElement(self, keys:str, key) -> None:
        """send keys to element

        :param keys: send keys
        :param key: get Web path with key param
        :return None
        """

        by,web_path = self.getPathInfo(key)                     # 주어진 키에 해당하는 웹 경로를 가져옵니다.
        self.logger.debug(f"{by} | {web_path} | {keys}")
        self.wait_1s.until(lambda d : d.find_element(self.elemtype[by],web_path).send_keys(keys) or True)

    def getListElements(self,key,path_str=None) -> list:
        """get list elements

        :param key: get Web path with key param
        :param path_str: Default is None if idx not none change web_path string with idx param
        :return list
        """

        by,web_path = self.getPathInfo(key)
        self.logger.debug(f"{by} | {web_path} | {path_str}")
        if path_str == None:
            return self.driver.find_elements(self.elemtype[by],web_path)
        else :
            return self.driver.find_elements(self.elemtype[by],web_path.format(page_str=path_str))
    
    def findElement(self,mode:str,key:str,idx:str=None) -> None:  
        """find element with mode param and key param

        :param mode: text or not
        :param key: get Web path with key param
        :param idx: Default is None if idx not none change web_path string with idx param
        :return None
        """

        by,web_path = self.getPathInfo(key)                     # 주어진 키에 해당하는 웹 경로를 가져옵니다.
        self.logger.debug(f"{by} | {web_path} | {idx}")         # 디버그용으로 로그를 기록합니다.
        try:                                            
            if mode == 'text' and idx == None:          
                return self.wait_1s.until(lambda d : d.find_element(self.elemtype[by],web_path).text)
            elif mode != 'text' and idx == None:
                return self.wait_1s.until(lambda d : d.find_element(self.elemtype[by],web_path) or True)
            elif mode == 'text' and idx != None: 
                return self.wait_1s.until(lambda d : d.find_element(self.elemtype[by],web_path.format(idx=idx)).text)
            elif mode != 'text' and idx != None:
                return self.wait_1s.until(lambda d : d.find_element(self.elemtype[by],web_path.format(idx=idx)) or True)
        
        except:
            self.logger.error(f"{by} | {web_path} | {idx}")
        
    def getPathInfo(self,key:str=''):   # class와 path를 반환하는 함수
        """get Web path with key param

        :param key: get Web path with key param
        :return tuple(by,web_path)
        """

        by,web_path = self.QE.getElemInfo(key)        # class와 path를 변수로 가져옴 
        self.logger.debug(f"{by} | {web_path}")
        return by,web_path

    #movie method
    def movePage(self,url:str):
        """
        move page to url

        :param url:
        :return: None
        """
        self.driver.implicitly_wait(10)
        self.wait_5s.until(lambda d : d.get(url) or True)
        self.driver.implicitly_wait(10)

    def clickGeneratePDF(self) -> None:
        """
        click generate pdf button

        :return: None
        """

        try:
            self.wait_5s.until(lambda d : d.find_element(By.XPATH, '//button[@aria-label="Export"]').click() or True)
            self.wait_5s.until(lambda d : d.find_element(By.XPATH, '//li[@title="Generate PDF"]').click() or True)
        except:
            self.clickAlertCloseButton()

    def openDownloadToggle(self):
        """
        open download toggle

        :return: None
        """
        
        self.wait_5s.until(lambda d : d.find_element(By.XPATH, '//button[@aria-label="Export"]').click() or True)
        self.wait_5s.until(lambda d : d.find_element(By.XPATH, '//li[@data-automation-id="navbar_export_pane_toggle_open"]').click() or True)

        return True

    def clickAlertCloseButton(self) -> None:
        """
        click alert close button

        :return: None
        """
        
        elems=self.driver.find_elements(By.ID,'alertCloseButton')
        for elem in elems:
            try:
                elem.click()
            except:
                pass

        return True
        