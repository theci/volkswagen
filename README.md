
# QuickSight PDF Downloader

폭스바겐에서 고객사의 요구사항을 충족하고 보다 높은 만족도를 달성하기 위해서 개발한 프로그램입니다.

## Getting Started

버전은 Docker Container 및 로컬 Chrome Driver를 베이스로 한 노트북 파일 두가지가 존재하며 실제 람다에 반영되고 있는 소스는 '/lambda' 디렉토리 아래에 위치해 있습니다  
local 버전은 오로지 테스트 및 xpath 같은 파라미터를 케치하기 위해 사용하며 해당 버전의 코드의 경우 구조가 매우 다릅니다. 

Docker 버전의 경우 Docker 및 podman의 설치가 필요하며 아래와 같은 환경 변수로 실행해야 합니다.
```
podman build -t lambda-selenium-python .
podman run -e bucket=marketstatus-pdf -e AWS_ACCESS_KEY_ID=<key> -e AWS_SECRET_ACCESS_KEY=<access_key> -e log_level=INFO lambda-selenium-python
```
아래는 각 환경변수에 대한 설명입니다.
특이사항으로는 로컬에서 테스트하기 위해서는 lambda처럼 IAM롤을 붙힐수 없기 때문에 환경변수에 Access Key, Secert Access key 등록을 통해 가동을 해야하며  
해당 Key 정보는 QuickSight user를 불러오거나 S3에 저장되기 위해서 사용됩니다(폭스바겐유저의 정보가 필요합니다)  

* bucket : pdf가 병합되어 저장되어질 버킷의 경로입니다.
* AWS_ACCESS_KEY_ID : AWS Access Key입니다.
* AWS_SECRET_ACCESS_KEY : AWS Secret Access Key 입니다.
* log_level : Python logger Class에 로그 출력 레벨을 조절하기 위한 변수입니다.  
  
컨테이너가 정상 가동되었다면 컨테이너 터미널에 들어가서 아래의 명령어로 실행하면 됩니다.
```
python main.py
```
### Prerequisites

해당 요구사항은 현재 로컬의 개발버전 기준으로 작성되었으며 과거 버전 및 최신버전에 대한 실시간 확인은 어려운점 양해 부탁드립니다.

```
OS : Windows 11

Docker or Podman : v4.7.2(Podman)

Python : 3.10, 3.11 (anaconda 2023.09)

# 사용된 Python lib는 다음과 같습니다.
* selenium==4.15.2
* PyPDF2==3.0.1
* boto3>=1.*
* webdriver-manager==3.8.6
```

## Deployment

lambda에 해당 컨테이너 이미지를 배포하기 위해서는 먼저 ECR에 해당 컨테이너 이미지를 올릴 필요가 있습니다.  
ECR 디렉토리에 올리는 방법은 다음의 커맨드와 같습니다.
```
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 630190875472.dkr.ecr.ap-northeast-2.amazonaws.com

[docker | podman] build -t lambda-selenium-python .

[docker | podman] tag lambda-selenium-python:latest 630190875472.dkr.ecr.ap-northeast-2.amazonaws.com/lambda-selenium-python:latest

[docker | podman] push 630190875472.dkr.ecr.ap-northeast-2.amazonaws.com/lambda-selenium-python:latest

```

## Contributing

Please read [CONTRIBUTING.md](https://github.com/your/project/contributing.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.mzcloud.xyz/ctc/aws/sa-1-team/volkswagen/-/tags).

## Authors

* **EdwardKim** - *Initial work* - [EdwardArchive](https://github.com/EdwardArchive)

## Acknowledgments

* src 디렉토리에 존재하는 두개의 json파일은 보다 효과적인 코드변경을 위해 작성되었으며 각각은 아래의 용도로 사용됩니다.
    * page.json : 해당 pdf downloader에서 접근하여 pdf를 생성할 webpage를 저장한 JSON파일입니다.
    * webelem.json : 해당 webpage에서 로그인 및 pdf 다운로드를 하기 위해서 필요한 webelement의 XPATH등 위치를 저장한 JSON파일입니다.
* 일반적인 케이스에서는 위의 두가지의 변경으로만 이슈가 대응될수 있도록 기대되고 만들었으나 UI는 그대로이나 접근하는 주소가 바뀌는 경우만 대응이 가능하며  
UI를 접근하는 순서에 대한 로직이 변경될 경우에 대한 구조로는 동작하지 않음을 주의해야합니다.
* 기타 문의사항은 직접 문의주시길 바랍니다.
