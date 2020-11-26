## 소개
URL: https://cvd2019.kr<br/>
<br/>코로나 보드를 참고하여 간단한 코로나 수치 통계 웹사이트를 만들어보았습니다.   
Django MVT 기반으로 제작한 개인 Python 웹 사이트입니다.  
<br/>![avatar](https://github.com/jeonghaknam/cvd2019_Python/blob/main/about/readme_images/20201124003622.png)<br/><br/>

## Frontend
+ HTML
+ CSS
+ JavaScrip
+ Echarts
+ Bootstrap

## Backend
+ Python-3.7.3
+ Django-2.2
+ [Newsapi-python-0.2.6](https://newsapi.org/)
+ Django-crontab-0.7.1
+ MySQL

## Server
+ CentOS 7.6
+ [宝塔面板(서버 관리 소프트웨어)](https://www.bt.cn/)
+ Nginx
+ uWSGI

## 사용방법 

+ ### 데이터베이스
  국가,도시 이름을 세가지 언어로 번역한 파일이 있습니다.   

  ``` project
  - about  
    |- KoreaName.sql  
    |- WorldName.sql
  ```
  테이블 생성뒤 해당 데이터를 입력 해주셔야 정상 가동됩니다.  
  + #### settings에서 DATABASES 설정  

    ``` python
    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': "test1",  #수정
          'USER': 'root',   #수정
          'PASSWORD': "mysql",  #수정
          'HOST': "127.0.0.1"
      }
    }
    ```
  + #### 테이블 생성
    1.첫번째
    ``` C
    python manage.py makemigrations
    ```
    2.두번째
    ``` C
    python manage.py migrate
    ```
    3.about 폴더로 이동
    ``` C
    cd about
    ```
    4.mysql 열기
    ``` C
    mysql -u아이디 -p패스워드
    ```
    ![avatar](https://github.com/jeonghaknam/cvd2019_Python/blob/main/about/readme_images/mysql1.png)<br/><br/>
    5.생성 확인후 데이터 입력
    ``` C
    source domesticname.sql
    ```
    ``` C
    source worldname.sql
    ```
    ![avatar](https://github.com/jeonghaknam/cvd2019_Python/blob/main/about/readme_images/mysql2.png)<br/><br/>
    <br/>![avatar](https://github.com/jeonghaknam/cvd2019_Python/blob/main/about/readme_images/name.png)<br/>

+ ### django crontab 설정
  자동화를 위하여 crontab을 이용하였습니다.  
  settings 129행 에서 설정하실수 있습니다.<br/><br/>
  ``` python
  CRONJOBS = [
    #  타이머 설정                #실행                  #로그파일 저장경로 수정     
    ('0 */2 * * *', 'cvd2019.views.create_static_page','>>/logs/update.log'),
    ('55 23 * * *', 'cvd2019.views.create_static_page', '>>/logs/update.log'),
  ]
  ```
  <br/>터머널에서 추가 및 확인
  ``` C
  python manage.py crontab add
  python manage.py crontab show
  ```
  ![avatar](https://github.com/jeonghaknam/cvd2019_Python/blob/main/about/readme_images/010141.png)<br/>

  <br/>아래와 같이 실행기록이 쌓이는것을 확인하실수 있습니다.

  ![avatar](https://github.com/jeonghaknam/cvd2019_Python/blob/main/about/readme_images/031114.png)<br/>
<br/>
<br/>
