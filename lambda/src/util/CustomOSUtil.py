import os
from glob import glob

# 주어진 디렉터리에서 pdf확장자인 파일을 삭제하는 기능을 제공합니다.
class CustomOSUtil:
    def cleanDirectory(self,directory: str,glob_pattern: str="*.pdf") -> None:
        # directory: 파일을 삭제할 디렉터리의 경로를 입력합니다. 예: '/tmp/pdf_path'.
        # glob_pattern: 삭제할 파일의 패턴을 정의하는 문자열입니다. 기본값은 "*.pdf", 즉 모든 PDF 파일을 의미합니다.
        """
        Delete file parttern *.pdf from Directory 

        param dir: clean directory if you want, like '/tmp/pdf_path'
        return Ture if worked, False then not worked
        """
        filelist = glob(os.path.join(directory, glob_pattern)) # 주어진 디렉터리 내에서 glob_pattern과 일치하는 파일을 찾습니다.
        for f in filelist:
            os.chmod(f, 0o777) # 찾은 파일들의 권한을 변경합니다. (이는 파일에 대한 쓰기 권한을 부여하기 위함입니다.)
            os.remove(f) # 해당 파일을 삭제합니다.

    # 주어진 디렉터리 내에서 특정 파일이 존재하는지 확인하는 기능을 제공합니다.
    def getFileExists(self,dir: str,file_type: str,file_name: str ='') -> bool:
        """
        Get file in 'dir' location contain 'file_name' and 'file_type' pdf from Directory 

        param dir: clean directory if you want, like '/tmp/pdf_path'
        param dir: string file Type to find(pdf,csv,txt...)
        param file_name: string file name to find
        return Ture if worked, False then not worked
        """

        if len(glob(f"{dir}/{file_name}*.{file_type}")) >=1:
            return True

        else :
            return False
        
    def getFileName(self,dir: str ,file_name: str='' ,glob_pattern: str='[pP]*',file_type: str='pdf') -> str:
        """
        Get file name in 'dir' location contain 'file_name' pdf from Directory 

        param dir: clean directory if you want, like '/tmp/pdf_path'
        param glob_pattern : some glob pattern if you needed
        param file_type : string file type to find
        param file_name: string file name to find
        return file_name string
        """
        
        result = ''
        result = glob(f"{dir}/{file_name}{glob_pattern}.{file_type}")[0]
        
        return result 