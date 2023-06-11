import base64
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
import os, requests, base64

apiHost = 'https://api.tilko.net/'
apiKey = 'a379ba7545364b1a8e5b4c4ee040aef7'

# AES 암호화 함수
def aesEncrypt(key, iv, plainText):
    def pad(text):
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)

        if amount_to_pad == 0:
            amount_to_pad = AES.block_size

        pad = chr(amount_to_pad)

        result = None
        try:
            result = text + str(pad * amount_to_pad).encode('utf-8')
        except Exception as e:
            result = text + str(pad * amount_to_pad)

        return result

    if type(plainText) == str:
        plainText = plainText.encode('utf-8')

    plainText = pad(plainText)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    if (type(plainText) == bytes):
        return base64.b64encode(cipher.encrypt(plainText)).decode('utf-8')
    else:
        return base64.b64encode(cipher.encrypt(plainText.encode('utf-8'))).decode('utf-8')


# RSA 암호화 함수(RSA 공개키로 AES키 암호화)
def rsaEncrypt(publicKey, aesKey):
    rsa = RSA.importKey(base64.b64decode(publicKey))
    cipher = PKCS1_v1_5.new(rsa.publickey())
    aesCipherKey = cipher.encrypt(aesKey)
    return aesCipherKey

# RSA 공개키(Public Key) 조회 함수
def getPublicKey():
    headers = {'Content-Type': 'application/json'}
    response = requests.get(apiHost + "/api/Auth/GetPublicKey?APIkey=" + apiKey, headers=headers)
    return response.json()['PublicKey']


# RSA Public Key 조회
rsaPublicKey = getPublicKey()
print(f"rsaPublicKey: {rsaPublicKey}")

# AES Secret Key 및 IV 생성
aesKey = os.urandom(16)
aesIv = ('\x00' * 16).encode('utf-8')

# AES Key를 RSA Public Key로 암호화
aesCipherKey = base64.b64encode(rsaEncrypt(rsaPublicKey, aesKey))
print(f"aesCipherKey: {aesCipherKey}")

# API URL 설정
url = apiHost + "api/v1.0/hirasimpleauth/simpleauthrequest"

# API 요청 파라미터 설정
options = {
"headers": {
    "Content-Type": "application/json",
    "API-KEY": apiKey,
    "ENC-KEY": aesCipherKey
},

"json": {
    "PrivateAuthType": "4",
    "UserName": aesEncrypt(aesKey, aesIv, '임민섭'),
    "BirthDate": aesEncrypt(aesKey, aesIv, '19980102'),
    "UserCellphoneNumber": aesEncrypt(aesKey, aesIv, '01095567172'),
    "IdentityNumber": aesEncrypt(aesKey, aesIv, '9801021074031'),
},
}

res = requests.post(url, headers=options['headers'], json=options['json'])

# RSA Public Key 조회
rsaPublicKey = getPublicKey()
print(f"rsaPublicKey: {rsaPublicKey}")

# AES Secret Key 및 IV 생성
aesKey = os.urandom(16)
aesIv = ('\x00' * 16).encode('utf-8')

# AES Key를 RSA Public Key로 암호화
aesCipherKey = base64.b64encode(rsaEncrypt(rsaPublicKey, aesKey))
print(f"aesCipherKey: {aesCipherKey}")

# API URL 설정
url = apiHost + "api/v1.0/hirasimpleauth/hiraa050300000100"

# 간편인증 요청 후 받은 값 정리
reqData = res.json()["ResultData"]
print(f'reqData: {reqData}')

# API 요청 파라미터 설정
options = {
    "headers": {
        "Content-Type": "application/json",
        "API-KEY": apiKey,
        "ENC-KEY": aesCipherKey
    },

    "json": {
        "IdentityNumber": aesEncrypt(aesKey, aesIv, '9801021074031'),
        "CxId": reqData["CxId"],
        "PrivateAuthType": reqData["PrivateAuthType"],
        "ReqTxId": reqData["ReqTxId"],
        "Token": reqData["Token"],
        "TxId": reqData["TxId"],
        "UserName": aesEncrypt(aesKey, aesIv, reqData["UserName"]),
        "BirthDate": aesEncrypt(aesKey, aesIv, reqData["BirthDate"]),
        "UserCellphoneNumber": aesEncrypt(aesKey, aesIv, reqData["UserCellphoneNumber"]),
    },

}

# API 호출
result = requests.post(url, headers=options['headers'], json=options['json'])
print(result.json())
resultList = result.json()["ResultList"]

# 지난 1년 처방이력 출력
for i in resultList:
    print(f"조제일자: {i['DateOfPreparation']}")
    for j in i['DrugList']:
        ediCode = j['Code']
        print(j)
