### 결제 기능을 위한 [iamport;](http://www.iamport.kr/) 테스트 코드

> 이 코드는 [[Django]Iamport 연동하기 - 1~4
](http://genius-project.postach.io/post/django-iamport-yeondonghagi-1) 를 보고 작성한 코드임을 밝힙니다.


수정 사항 
	
- `“TypeError: Unicode-objects must be encoded before hashing”` 해결을 위해 `models.py > PointTransactionManager` 에 `encode()` 추가

#### `SECRET_KEY`를 보안을 위한 프로젝트 레이아웃

```
iamport_test
    ├── .config_secret
    │   └── settings_common.json 👈
    └── django_app
        └── cofig
            └── settings.py 👈
        └── billing
            └──...
```
```
[.config_secret/settings_common.json]

{
  "django": {
    "secret_key": "Your django secret key"
  },
  "iamport": {
    "iamport_key": "Your REST API KEY",
    "iamport_secret": "Your REST API SECRET KEY"
  }
}
```

**settings.py** 에서 **.config_secret/settings\_common.json** 파일의 `REST API 키`, `REST API secret`, `Django SECRET_KEY`를 가져오기 위한 경로 설정

```
[config/settings.py]

...

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

CONFIG_SECRET_DIR = os.path.join(ROOT_DIR, '.config_secret')
CONFIG_SECRET_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')

config_secret_common = json.loads(open(CONFIG_SECRET_COMMON_FILE).read())

SECRET_KEY = config_secret_common['django']['secret_key']

# iamport; API KEY
IAMPORT_KEY = config_secret_common['iamport']['iamport_key']
IAMPORT_SECRET = config_secret_common['iamport']['iamport_secret']

...
```

**templates/billing/chare.html** 의 javascript에서 **가맹점 식별코드** 설정

```
[templates/billing/charge.html]

$(function(){
            var IMP = window.IMP;
            IMP.init('Your identifying code');
            ...
})
```

<br>

I'mport; 관리자페이지의 `가맹점 식별코드`, `REST API 키`, `REST API secret`, `Django SECRET_KEY` 만 변경하여 사용 가능

[IMP.request_pay() 파라메터 상세보기](https://github.com/iamport/iamport-manual/blob/master/%EC%9D%B8%EC%A6%9D%EA%B2%B0%EC%A0%9C/README.md)
