import requests
import json

from django.conf import settings


# access_token 발급
def get_access_token():
    # API키 & API secret
    access_data = {
        'imp_key': settings.IAMPORT_KEY,
        'imp_secret': settings.IAMPORT_SECRET
    }
    # 요청 보낼 url
    url = "https://api.iamport.kr/users/getToken"
    # /users/getToken 로 POST 요청
    req = requests.post(url, data=access_data)
    # 결과값 json 형태로 할당
    access_res = req.json()
    # 요청에 성공했을 경우("code": 0) 토큰값 반환
    if access_res['code'] is 0:
        return access_res['response']['access_token']
    else:
        return None


# 결제검증단계: 유저가 요청한 금액과 아임포트에 있는 결제 금액이 일치하는지 검증
# 사전등록된 가맹정 주문번호(merchant_uid)에 대해
# IMP.requests_pay()에 전달된 merchant_uid가 일치하는 주문의 결제금액이 다른 경우
# PG사 결제창 호출이 중단
def validation_prepare(merchant_id, amount, *args, **kwargs):
    # 토큰값 받기
    access_token = get_access_token()

    # 토큰값이 있을 경우
    if access_token:
        access_data = {
            'merchant_uid': merchant_id,
            'amount': amount
        }

        url = "https://api.iamport.kr/payments/prepare"

        headers = {
            'Authorization': access_token
        }

        req = requests.post(url, data=access_data, headers=headers)
        res = req.json()
        # code 0 : 요청에 성공
        # code 1 : 결제정보 사전등록에 실패하였습니다(이미 등록된 merchant_uid입니다).
        # code -1 : Unauthorized
        if res['code'] is not 0:
            raise ValueError("API 연결에 문제가 생겼습니다.")
    else:
        raise ValueError("인증 토큰이 없습니다.")


def get_transaction(merchant_id, *args, **kwargs):
    # 토큰값 받기
    access_token = get_access_token()

    if access_token:
        url = "https://api.iamport.kr/payments/find/" + merchant_id

        headers = {
            'Authorization': access_token
        }

        req = requests.post(url, headers=headers)
        res = req.json()

        if res['code'] is 0:
            context = {
                'imp_id': res['response']['imp_uid'],
                'merchant_id': res['response']['merchant_uid'],
                'amount': res['response']['amount'],
                'status': res['response']['status'],
                'type': res['response']['pay_method'],
                'receipt_url': res['response']['receipt_url']
            }
            return context
        else:
            return None

    else:
        raise ValueError("인증 토큰이 없습니다.")