import requests

def getPillInfo(pill_edi_code):
    url = 'http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01'
    params ={'serviceKey' : 'XhzWrdnyXRykvCEJSiPqWWjHuP7u5stjflVUZ81wQeY2mTRWNLloRMZsBTeiViMmiCjFw1xAxUfKf5FyXJaxuQ==', 'item_name' : '', 'entp_name' : '', 'item_seq' : '', 'img_regist_ts' : '', 'pageNo' : '1', 'numOfRows' : '3', 'edi_code' : pill_edi_code, 'type' : 'json' }

    response = requests.get(url, params=params).json()
    if response['body']['totalCount'] != 0:
        responseItem = response['body']['items'][0]
        print(f'{responseItem["COLOR_CLASS1"]} {responseItem["DRUG_SHAPE"]} ')