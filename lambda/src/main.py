import json,os
from time import sleep,time
from datetime import datetime
from PyPDF2 import PdfMerger

from selenium.webdriver.common.by import By

from util.CustomBoto3 import CustomBoto3
from util.CustomWebdriver import CustomWebdriver
from util.CustomOSUtil import CustomOSUtil
from util.CustomLogger import CustomLogger
from util.QuickSightElement import QuickSightElement



account_name = 'volkswagenkorea'
result_dir = "/tmp/pdf_path"

bucket = os.environ['bucket']
level_str = os.environ['log_level']

QE = QuickSightElement() # 퀵사이트 요소 선택기 객체 생성
Logger = CustomLogger(level=level_str).getLogger() # 로깅 객체 생성
CustomWebdriver = CustomWebdriver(result_dir=result_dir,logger=Logger) # 웹드라이버 객체 생성
CustomOSUtil = CustomOSUtil() # OSUtill 객체 생성
CustomBoto3 = CustomBoto3() # Boto3 객체 생성

Urls = QE.getUrlfromJson()

# 퀵사이트 로그인 코드
def quicksigt_login(id:str,pw:str):  
    """quick sight login function
    
    :param id: QuickSight user id
    :param pw: QuickSight user password
    :return: None 
    """

    CustomWebdriver.movePage(Urls['pid1']['url'])  # phase 1페이지 url로 이동
    Logger.info("Driver Start!")

    CustomWebdriver.sendKeysElement(key='login_eid1',keys=account_name)
    CustomWebdriver.clickWebDriver(key='login_eid2')                        # account 입력 확인 버튼 클릭
    Logger.info("account pass!")
    
    CustomWebdriver.sendKeysElement(key='login_eid3',keys=id)
    CustomWebdriver.clickWebDriver(key='login_eid4')                        # username 입력 확인 버튼 클릭
    Logger.info("user-id pass!")

    CustomWebdriver.sendKeysElement(key='login_eid5',keys=pw)
    CustomWebdriver.clickWebDriver(key='login_eid6')                        # password 입력 확인 버튼 클릭
    Logger.info("password pass!")


# 퀵사이트 다운로드 시작 코드
def runDownloadQuickSightPDF(url:str):              # QuickSight 웹 페이지에서 PDF를 다운로드합니다.
    """run quick sight pdf download function
    
    :param url: page url
    :return: None
    """

    bf_log_str = ""                             
    Logger.info(f"Move to Page : {url}")         
    page_list=[]                                 
    CustomWebdriver.movePage(url)                # 지정된 URL로 페이지를 이동합니다.

    CustomWebdriver.openDownloadToggle()         # 다운로드 토글을 클릭
    Logger.info(f"Page Moved : {url}")           # 페이지 이동 로그를 기록합니다.

    total_page=len(CustomWebdriver.getListElements(key='download_eid2'))    # 다운로드할 탭의 개수. 
    Logger.info(total_page)                      # 총 페이지 수를 로그로 기록합니다

    for idx in range(1,total_page+1):            # 1페이지 순서부터 반복
        pass_pdf=False                           # PDF를 통과할지 여부를 나타내는 변수를 초기화합니다.
        page_str=CustomWebdriver.findElement(key='download_eid10',idx=idx,mode='text')           # 페이지의 문자열을 가져옵니다.
        Logger.debug(CustomWebdriver.clickWebDriver(key='download_eid10',idx=idx))               # 디버그 로그를 기록하고, 페이지를 클릭합니다.
        page_list.append(page_str)               # 페이지 목록에 페이지 문자열을 추가합니다.
        
        while pass_pdf == False:                    # PDF가 생성되어 .True가 될때까지 반복 호출
            CustomWebdriver.clickGeneratePDF()      # PDF 생성 버튼을 클릭합니다.
            check_pdf=CustomWebdriver.getListElements(key='download_eid11',path_str=page_str)    # PDF가 준비되었는지 확인하기 위해 페이지의 요소를 가져옵니다.
            for elem in check_pdf:         # PDF 요소를 확인합니다.
                    if elem.text.split(' ')[2] == page_str:               # 페이지 문자열이 PDF와 일치하는지 확인합니다.
                        Logger.info(f"Click Generate PDF : {page_str}")   # PDF 생성을 로그로 기록합니다.
                        pass_pdf=True   
                    else:
                        pass
            
    start_time=time()     # 시간 측정을 시작합니다.
    while True:          
        elems=CustomWebdriver.getListElements(key = "download_eid12")     # 다운로드된 페이지 요소를 가져옵니다.
        if len(page_list)==len(elems)  :            # 다운로드된 페이지 수가 전체 페이지 수와 같은지 확인합니다.
            Logger.info("Download Ready!")          # 다운로드가 준비되었음을 로그로 기록합니다.
            break
        
        elif time()-start_time > 120 :                         # 다운로드가 너무 오래 걸리는 경우
            Logger.warning("Ready too Long!")                  # 오랜 시간이 소요된 경우를 로그로 기록
            raise Exception('Timeout error Please retry!')     # 예외를 발생
        
        else :
            if bf_log_str != f"{len(elems)} / {len(page_list)} is ready.. " :   # 이전 로그 문자열과 현재 로그 문자열을 비교합니다.
                bf_log_str = f"{len(elems)} / {len(page_list)} is ready.. "     # 현재 로그 문자열을 저장합니다.
                Logger.info(bf_log_str)                        # 다운로드 상황을 로그로 기록합니다.
    
    CustomWebdriver.clickAlertCloseButton()
    clickDownload()                                 # 클릭 다운로드 호출

    return page_list

def clickDownload():
    """click download button function
    """

    for Webelem in CustomWebdriver.getListElements(key = "download_eid9"):
            Webelem.click()
            sleep(0.2)


def checkDownload(result_dir:dict,page_list:list) -> bool:    # 함수를 정의합니다. 
    # 이 함수는 다운로드된 PDF 파일이 있는지 확인하고, 모든 페이지가 다운로드될 때까지 기다립니다. 
    # 반환값은 성공 여부를 나타내는 불리언(Boolean)입니다.
    """check download file
    
    :param result_dir: download directory
    :param page_list: total page list
    :return: True if download success, False if not. 
    """
    try:
        for file_name in page_list:       # 페이지 목록에 대해 반복합니다.
            start = time()                # 시간 측정을 시작합니다.
            before_print=False            # 이전에 로그를 출력하지 않았음을 나타내는 변수를 초기화합니다.
            while True:                   # 무한 루프를 시작합니다.
                end = time()              # 현재 시간을 측정합니다.
                if CustomOSUtil.getFileExists(result_dir,'pdf',file_name) == True:   # 파일이 다운로드되었는지 확인합니다.
                    Logger.info(f"{file_name} pdf download complete")     # PDF 파일 다운로드가 완료되었음을 로그로 기록합니다.
                    break                     # 파일이 다운로드되었으므로 무한 루프를 종료합니다.
                elif before_print==False :    # 이전에 로그를 출력하지 않았다면:
                    Logger.info(f"Checking for {file_name} Download file..")   # 파일 다운로드 상태를 확인 중임을 로그로 기록합니다.
                    before_print = True       # 이제 로그를 출력했음을 표시합니다.
                elif end - start > 30:        # 다운로드가 오랜 시간 동안 완료되지 않았다면:
                    clickDownload()           # 다운로드 버튼을 클릭합니다.
                else: pass                    # 그렇지 않으면 아무 작업도 하지 않고 다음 반복을 진행합니다.
        Logger.info("Download Done!")         # 모든 파일이 다운로드되었음을 로그로 기록합니다.
        return True             # 모든 파일이 다운로드되었으므로 True를 반환합니다.
    
    except :
        return False            # 다운로드 중 오류가 발생하거나 시간이 초과되었을 경우 False를 반환합니다.
    

def mergePdf(tot_page:int,pdf_file_name:str,result_dir:str):    # 함수를 정의합니다. 이 함수는 PDF 파일을 병합하여 단일 PDF 파일을 생성합니다.

    """merge pdf file
    
    :param tot_page: total page count
    :param pdf_file_name: save pdf file name
    :param result_dir: result directory path
    :return: True if merge success, False if not.
    """

    try:
        merger = PdfMerger()   # PyPDF2의 PdfMerger 객체를 생성합니다. 이 객체는 PDF 파일을 병합하는 데 사용됩니다.
        for page_num in range(1,tot_page+1):   # 병합할 PDF 파일의 수만큼 반복합니다.
            try:
                merger.append(CustomOSUtil.getFileName(dir=result_dir,file_name=page_num))  # 지정된 디렉토리에서 지정된 파일 이름 패턴에 해당하는 PDF 파일을 병합합니다.
            except:
                Logger.error(f"Cannot Found File : {result_dir}/{page_num}[pP]*.pdf")   # 파일을 찾을 수 없는 경우 오류를 기록합니다.

        merger.write(f"/tmp/pdf_path/{pdf_file_name}.pdf")   # 병합된 PDF를 지정된 위치에 저장합니다.
        merger.close()         # PdfMerger 객체를 닫습니다.

        return True            # 병합이 성공적으로 완료되면 True를 반환합니다.
    
    except:
        return False           # 오류가 발생한 경우 False를 반환합니다.

def handler(event=None, context=None) -> dict:# 핸들러 함수를 정의합니다. 
    # 이 함수는 AWS Lambda에서 실행됩니다. event 및 context 매개변수를 받고, 딕셔너리를 반환합니다.
    """lambda handler function
    
    :param event: event
    :param context: context
    :return: None
    """

    CustomOSUtil.cleanDirectory(directory=result_dir)  # 주어진 디렉토리의 모든 파일을 삭제합니다.

    id,pw = CustomBoto3.getQuickSightUserFromSSM()     # SSM 에서 QuickSight ID, PW 함수 호출
    page_list = []
    tot_page = 0

    quicksigt_login(id,pw)
    Logger.info("Login Done")
    sleep(5)

    for url in Urls:                                                    # 모든 URL에 대해 반복합니다.
        page_list=runDownloadQuickSightPDF(url=Urls[url]['url'])        # QuickSight에서 PDF를 다운로드하고, 다운로드된 페이지 목록을 가져옵니다.
        checkDownload(result_dir=result_dir,page_list=page_list)        # 다운로드된 PDF 파일이 있는지 확인하고, 모든 페이지가 다운로드될 때까지 기다립니다.
        tot_page+=len(page_list)                                        # 전체 페이지 수를 업데이트합니다.

    CustomOSUtil.cleanDirectory(result_dir,"* ([1-9]).pdf")             # 다운로드된 PDF 파일 중 1부터 9까지의 페이지가 있는 파일을 삭제합니다.
    
    Logger.info("Merge & Upload pdf")                                   # PDF 파일을 병합하고 업로드하는 작업을 수행함을 로그로 기록합니다.

    ymdh_str = datetime.utcnow().strftime("%Y%m%d_%H")                  # 현재 날짜와 시간을 UTC로 가져옵니다.
    merge_pdf_name = "finalpdf_UTC"+ymdh_str                            # 병합된 PDF 파일의 이름을 생성합니다.
    mergePdf(tot_page,merge_pdf_name,result_dir)                        # 모든 페이지를 병합하여 단일 PDF 파일을 생성합니다.

    #logger.info("Upload PDF on S3")
    #CustomBoto3.uploadFileToS3(f"/tmp/pdf_path/{merge_pdf_name}.pdf",bucket,f"pdf_merged/{merge_pdf_name}.pdf")

    Logger.info("Download & Merge Done")
    CustomWebdriver.driver.quit()                                       # WebDriver를 종료합니다.

    return {
        "message" : "Lambda Pdf Downloader Work Done"                   # 작업이 완료되었음을 나타내는 메시지를 반환합니다.
    }

    

if __name__ == "__main__":   # __name__을 이용한 구문을 넣어주면 모듈이 임포트 되면서 실행되는 참사를 막을 수 있음
    handler()


for i in range(1,10):
    a.append(i)

a=[i for i in range(1,10)]