from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Service 객체 추가
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass

import os
from glob import glob
from PyPDF2 import PdfMerger

result_dir="C:/Data_Files"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", {
  "download.default_directory": r"C:\Data_Files"
  })

#dashboard_url = input("url : ")
quicksight_id = input("ID : ")
pswd = getpass.getpass('Password:')



page_str="https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/a7adfe68-ab7e-45f4-a988-94bc41cf9c53/views/035c3ebe-9250-4dac-8cca-efdd94c3df10"

## Clean dir
filelist = glob(os.path.join(result_dir, "*.pdf"))
for f in filelist:
    os.chmod(f, 0o777)
    os.remove(f)

## function download
def quicksigt_login(driver,qid,qpwd):
    driver.get("https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/a7adfe68-ab7e-45f4-a988-94bc41cf9c53/views/035c3ebe-9250-4dac-8cca-efdd94c3df10")
    driver.implicitly_wait(3)

    driver.find_element(By.ID,'account-name-input').send_keys('volkswagenkorea')
    driver.find_element(By.ID,'account-name-submit-button').click()
    
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username-input")))
    driver.find_element(By.ID,'username-input').send_keys(qid)
    driver.find_element(By.ID,'username-submit-button').click()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "awsui-input-0")))

    driver.find_element(By.ID,'awsui-input-0').send_keys(qpwd)
    driver.find_element(By.ID,'password-submit-button').click()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="내보내기"]')))
    return driver

def quicksight_download(driver,total_page,url):
    
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="내보내기"]')))
    
    done_count=0
    driver.find_element(By.XPATH, '//button[@aria-label="내보내기"]').click()
    driver.find_element(By.XPATH, '//li[@data-automation-id="navbar_export_pane_toggle_open"]').click()
    sleep(1)
    for i in range(1,total_page+1):
        driver.find_element(By.XPATH,f'//*[@id="application-content"]/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div[{i}]').click()
        sleep(3)
        driver.find_element(By.XPATH, '//button[@aria-label="내보내기"]').click()
        driver.find_element(By.XPATH, '//li[@title="PDF 생성"]').click()
        sleep(1)

    sleep(30)

    while done_count<total_page:
        try:
            driver.find_element(By.ID,'alertCloseButton').click()
            done_count+=1
        except:
               pass
        finally:
            sleep(1)
            print(f"Wait for done! ({done_count}/{total_page}) : {round((done_count/total_page)*100,2)}%")

    for i in range(1,total_page+1):
        driver.find_element(By.XPATH, f'//*[@id="vega-right-pane"]/div/div/div/div[{i}]/div[2]/p[2]/div').click()
    
    return driver

#login
# driver = webdriver.Chrome(executable_path='chromedriver.exe',options=options)
# driver.implicitly_wait(3)
# driver = quicksigt_login(driver,quicksight_id,pswd)
chromedriver_path = '/Users/mzc01-pch/Desktop/백업/project/메가존/폭스바겐/pdf생성코드/pdf_downloader/lambda/src/chromedriver'  # 경로를 실제 위치로 수정하세요
service = Service(executable_path=chromedriver_path)  # Service 객체로 변경
driver = webdriver.Chrome(service=service, options=options)  # service 인자로 전달
driver.implicitly_wait(3)
driver = quicksigt_login(driver, quicksight_id, pswd)

# ##Dashboard 1_1 Page Download   

# d1_url="https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/a7adfe68-ab7e-45f4-a988-94bc41cf9c53/views/035c3ebe-9250-4dac-8cca-efdd94c3df10"
# page_d1=18
# driver = quicksight_download(driver,page_d1,d1_url)
# sleep(30)

# ##Dashboard 1_2 Page Download   

# d2_url="https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/7b03e7cf-3485-4610-ab1f-b4a3a7c6ca1e/views/a07f7b18-7a72-4546-860a-1b395ad9a85f"
# page_d2= 7
# driver = quicksight_download(driver,page_d2,d2_url)
# sleep(30)

# ##Cover Page Download   

# cover_url='https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/09acf2c8-158d-47b2-b63a-8cbfd183ad1e/views/60e4100a-7bd1-4890-b56c-b430890bf3ab'
# page_c= 8
# driver = quicksight_download(driver,page_c,cover_url)
# sleep(30)