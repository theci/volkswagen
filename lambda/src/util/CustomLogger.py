import logging

class CustomLogger:
    _logger = None

    def __init__(self,level: str="INFO") -> None:
        level_dict={"INFO": logging.INFO, "DEBUG" :  logging.DEBUG, "WARNING" : logging.WARNING,"ERROR" : logging.ERROR}
        self._logger = logging.getLogger()  # 로그 생성
        self._logger.setLevel(level_dict[level])
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')  #log 출력 형식
        stream_handler = logging.StreamHandler()        # log를 console에 출력
        stream_handler.setFormatter(formatter)  
        self._logger.addHandler(stream_handler)
    
    def getLogger(self):
        return self._logger

if __name__ == 'main':
    logger = CustomLogger('INFO').get_logger()
    logger.info("test logger class")