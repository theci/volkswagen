FROM public.ecr.aws/lambda/python:3.11-x86_64 as build                  # Lambda Python 런타임 환경에서 시작하여 "build" 스테이지로 지정된 이미지를 빌드합니다. 
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip" && \         # curl 명령어를 사용하여 ChromeDriver를 다운로드하고 /tmp/chromedriver.zip에 저장합니다.
    curl -Lo "/tmp/chrome-linux.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chrome-linux64.zip" && \               # curl 명령어를 사용하여 Chrome을 다운로드하고 /tmp/chrome-linux.zip에 저장합니다.
    unzip /tmp/chromedriver.zip -d /opt/ && \                               # unzip 명령어를 사용하여 /tmp/chromedriver.zip의 내용을 /opt/ 디렉토리에 압축 해제합니다.
    unzip /tmp/chrome-linux.zip -d /opt/                                    # unzip 명령어를 사용하여 /tmp/chrome-linux.zip의 내용을 /opt/ 디렉토리에 압축 해제합니다.

FROM public.ecr.aws/lambda/python:3.11-x86_64                               # 이 라인부터 새로운 이미지 빌드를 시작합니다. 앞서 정의된 "build" 스테이지와 별도로, 새로운 베이스 이미지로 빌드합니다.
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \                 # Selenium 및 관련 라이브러리를 설치하기 위해 YUM을 사용하여 여러 패키지를 설치합니다.
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y                         
RUN mkdir -p /tmp/pdf_path                                                  # 디렉토리를 생성합니다. 이 디렉토리는 나중에 Lambda 함수에서 PDF 파일을 저장하는 데 사용될 것입니다.
RUN mkdir -p /tmp/html                                                      # 디렉토리를 생성합니다. 이 디렉토리는 나중에 Lambda 함수에서 HTML 파일을 저장하는 데 사용될 것입니다.
RUN mkdir -p /var/task/pdf_merged                                           # 디렉토리를 생성합니다. 이 디렉토리는 나중에 Lambda 함수에서 병합된 PDF 파일을 저장하는 데 사용될 것입니다.
COPY src/requirements.txt  ./                                               # Lambda 함수에 필요한 Python 패키지들의 목록을 포함하는 requirements.txt 파일을 현재 디렉토리로 복사합니다.
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"        # requirements.txt에 명시된 Python 패키지들을 설치합니다. ${LAMBDA_TASK_ROOT}에 설치됩니다.
COPY --from=build /opt/chrome-linux64 /opt/chrome                           # 이전 스테이지에서 다운로드된 Chrome을 현재 이미지로 복사합니다.
COPY --from=build /opt/chromedriver-linux64 /opt/                           # 이전 스테이지에서 다운로드된 ChromeDriver를 현재 이미지로 복사합니다.
COPY src/main.py "${LAMBDA_TASK_ROOT}"                                      # Lambda 함수의 메인 코드 파일인 main.py를 ${LAMBDA_TASK_ROOT}로 복사합니다.
COPY src/util/ "${LAMBDA_TASK_ROOT}"/util/                                  # Lambda 함수에서 사용될 유틸리티 파일들을 ${LAMBDA_TASK_ROOT}/util/로 복사합니다.
COPY src/conf/ "${LAMBDA_TASK_ROOT}"/conf/                                  # Lambda 함수에서 사용될 설정 파일들을 ${LAMBDA_TASK_ROOT}/conf/로 복사합니다.
CMD [ "main.handler" ]                                                      # 컨테이너가 시작될 때 실행되는 기본 명령을 정의합니다. 여기서는 main.py 파일에 있는 handler 함수가 호출됩니다.


