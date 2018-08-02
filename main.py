import xlsxwriter
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import requests
import random
headers ={
'authority': 'map.naver.com',
'method':'GET',
'scheme': 'https',
'accept': 'application/json, text/javascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
'cookie': 'NNB=TGCBYRVSAFFVW; npic=Atbb0OFzirfYV1bptFCF2Zksn4Io9jVyOlMe2APKL/yZRj0SNGVsURuwvsJFwSZ+CA==; nx_ssl=2; _ga=GA1.2.598604263.1531729296; ASID=79a9092c00000164a28e4df600011423; nid_inf=1712338304; NID_AUT=zrtcDyq8sRXzCec2+ux+pALLzMLowrq8I8dJOqZXn0PsvrBugd2hdbD+CunTDt3m; NID_JKL=Ogb63rach1eJbzeaz1g0Q5173Ia0UrQjfLZT6gKSnzM=; BMR=s=1533173042812&r=https%3A%2F%2Fm.post.naver.com%2Fviewer%2FpostView.nhn%3FvolumeNo%3D16419411%26memberNo%3D217736&r2=https%3A%2F%2Fwww.facebook.com%2F; _naver_usersession_=xANqIUkZlbf8Jwu/91nEcg==; cq4BSUuVCb72BE4Whr1UrPbpuKM="g1SFVBbKL0nCWfk0fadE1tRORy0=|ZubMy6uPVGYdq03D|1533196800000"; NID_SES=AAABjBxb+u0U2cu0NgEvsuqa4B/sqYJIhulKqYPPEhlo+PPF1F4xqFeY6G1zI2QBz/OcqB7s6NM0JBGQ1Lwqx5ZNC+S9WeG6jmThsaE33XnzVux3lVD0ethPNIpn28AGp8NcayZTIHA5WObPfEcLBWlWLLjkNAsU0++TWAFrwfZDqxYHHtATKsMcIwGGxzE/aub89pthcl9OH8by55InbuB5CVA0iHjYq4ump5p+rqHp29exO9yn03dmMpb7i1yrc7cRqZtTZxG15kUTZkIID++aegcBtfwJ0KkUzDpgIEGCOR94c8jFRxduThyjO88jY6FykEpuP1v2gZyKlxULGsg/6f2UZYOT5Yhlnc57L37af3ThlJe4BJFKDXBKXmg6FkC+NDGuTwgtBdrmWI2GWryYWwsw2e38SMXuVIId96geiIRN+mVSf1xIaznjkY5H71Ne86/eijNlFeN80qxBp+Y329qeqF6SpG0VHJ2B1DfRnoujrW6FnQbGx0znH9wFcRggOkk6ALrL537xup4YmhRfo/8=; JSESSIONID=8ADECE8D6ACFFAC60487ED7EFBC8A673; page_uid=T27vwlpy72sssP/l2LRsssssseZ-157934; JmXtJZ2gh08IjL5t1FH0v4azmg="ieP6cHoTPZ8KzKHg9fyphbqhyJM=|zScYWLiSyGJKImLW|1533200400000"',
'referer': 'https://map.naver.com/',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}
FILENAME = "경기도-2428.xlsx"
def get_data_by_json():
    global row
    for idx in range(172,244):
        print(">>> {} 페이지 진행중".format(idx))
        url = 'https://map.naver.com/search2/local.nhn?query=%EA%B2%BD%EA%B8%B0%EB%8F%84+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=128.606002%3B35.8497761&sm=clk&mpx=09620735%3A37.4469136%2C126.9422732%3AZ6%3A1.0490796%2C0.4796013'
        html = requests.get(url.format(idx),headers=headers)
        jsonStr = json.loads(html.text)
        results = jsonStr['result']['site']['list']
        if len(results) != 0:
            for result in results:
                name = result['name']
                address = result['address']
                roadAddress = result['roadAddress']
                tel = result['tel']
                code = result['id'][1:]
                homepage =result['homePage']
                worksheet.write_row(row, 0, [name,roadAddress,address,tel,homepage,detailBaseUrl+code])
                row+=1
        else:
            print("끝")
            break
        time.sleep(random.randint(5,10))
def get_query_list():
    queryList = []
    tmp = 'code'
    bs4 = BeautifulSoup(tmp, 'lxml')
    lis = bs4.find_all('li')
    for li in lis:
        queryList.append(li.a['data-query'])
    return queryList
if __name__ == "__main__":
    # === GLOBAL
    detailBaseUrl = 'https://map.naver.com/local/siteview.nhn?code='
    #=== EXCEL
    workbook = xlsxwriter.Workbook(FILENAME)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['업소명', '도로명주소', '지번주소', '전화번호', '홈페이지1', '상세페이지'])
    row = 1
    col = 0
    #===PARSING
    try:
        get_data_by_json()
    except:
        pass
    #=== ~()
    workbook.close()
    """
    # 경기 강원ㅇ 경상남도 ㅇ 경상북도 ㅇ
    # 광주ㅇ,대구ㅇ,대전,부산,서울특별,울산,인천광역시
    # 전라남도 전라북도 제주특별자치
    # 충첨남도 충청북도 세종특별자치
    print (  2428 + 244 + 566 + 408 )
    print ( 285+ 507 + 356 + 736 + 2678 +  191 +533)
    print( 210+ 269 +110)
    print ( 347+293+42)
    
    print( 3646+5286+589+682)
    """

