import json
class QuickSightElement:
    url=''  
    _path=''

    def __init__(self):                                # 클래스의 초기화
        self.url=self.getUrlfromJson()
        self.getElemPathfromJson()                     

    def getUrlfromJson(self) -> dict:                  # JSON 파일에서 URL 정보를 가져와 반환
        with open('conf/page.json') as f:
            url = json.load(f)['phase1_items']
        return url

    def getElemPathfromJson(self) -> dict:             # json파일에서 _path에 저장
        with open('conf/webelem.json') as f:
            self._path= json.load(f)
    
    def explainElem(self,ElemId: str ='') -> str:      # 특정 웹 요소의 설명을 가져옵니다. 웹 요소의 ID를 매개변수로 받고, 해당 요소의 설명을 반환합니다.
        return self._path[ElemId]['__comment__']
    
    def getElemInfo(self,ElemId: str ='') -> list:     # ElemId를 매개변수로 받고, 해당 요소의 클래스 및 경로 정보를 리스트로 반환합니다.
        elem_class = self._path[ElemId]['class']
        elem_path = self._path[ElemId]['path']

        return elem_class,elem_path

if __name__=='__main__':          
    qse = QuickSightElement()                    
    print(qse.getUrlfromJson('phase1_items'))
