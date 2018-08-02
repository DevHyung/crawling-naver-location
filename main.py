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
'cookie': 'NNB=TGCBYRVSAFFVW; npic=Atbb0OFzirfYV1bptFCF2Zksn4Io9jVyOlMe2APKL/yZRj0SNGVsURuwvsJFwSZ+CA==; nx_ssl=2; _ga=GA1.2.598604263.1531729296; ASID=79a9092c00000164a28e4df600011423; nid_inf=1712338304; NID_AUT=zrtcDyq8sRXzCec2+ux+pALLzMLowrq8I8dJOqZXn0PsvrBugd2hdbD+CunTDt3m; NID_JKL=Ogb63rach1eJbzeaz1g0Q5173Ia0UrQjfLZT6gKSnzM=; BMR=s=1533173042812&r=https%3A%2F%2Fm.post.naver.com%2Fviewer%2FpostView.nhn%3FvolumeNo%3D16419411%26memberNo%3D217736&r2=https%3A%2F%2Fwww.facebook.com%2F; _naver_usersession_=xANqIUkZlbf8Jwu/91nEcg==; cq4BSUuVCb72BE4Whr1UrPbpuKM="g1SFVBbKL0nCWfk0fadE1tRORy0=|ZubMy6uPVGYdq03D|1533196800000"; JmXtJZ2gh08IjL5t1FH0v4azmg="ieP6cHoTPZ8KzKHg9fyphbqhyJM=|zScYWLiSyGJKImLW|1533200400000"; NID_SES=AAABkpv8wAKWwdDG1psG88Ofqvk3vrgeAWyDjA+OpxGWLr4O4zdRW8iPz/6kIfMoYVIjTdP2ElPmpZxTw9mOapoRwYONXHqajoYkSqECa2iv8HUPwrSMXmO68IL8d/iIy5OCq79ZHyz3ArnxHELPDDJ54ccjgPNdw7nfth53zrr6Drw421xRkKSWfx6c5oNEJtfkyDZjbPvdDqq5s+jhHZOaQW4hZNd0e1MLHCZ/6akF4fWCqeZmkUE/MoEJYHbn9pUoEyLgfLmXKmbVPq7aksILis4yMCEzJRtOES5pmYA2Jn+VpXzhi5wEbzDDbMlMB+5D5fahtGXVyhYRjEjMgULq2vRCYD6If/2UIvIcPZOZmj+/Uvj4dGMEZNGMNrAALwuR25PJhCXYGciWsabFc5LMm+Mi6kj6QI2SHOJXafPEx2oyk6tArRX9/d6viklyqkqoxOfKpQNL/fGRGbDfbnlG0RbA2A0On58TCgw7W5mFpnztKfn46zKevvfhX1gki0CdTm2aziBkbpZyDsFkl4T75j1N6++MB3IrfCC++Tbr5aP3; JSESSIONID=524CCC28AD9D733016F6C993864F7F42; tOscRBjfs6Ik94toZwAqzMgAk="EQdMQ23d+Hc3U9uh/oW7VRN8yvM=|AKb76EhZafgrZJiR|1533202200000"; page_uid=T274espy71wssvuoP9Cssssss4C-372484',
'referer': 'https://map.naver.com/',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}
FILENAME = "서울특별시-2300~2679.xlsx"
def get_data_by_json():
    global row
    for idx in range(230,269):
        print(">>> {} 페이지 진행중".format(idx))
        url = 'https://map.naver.com/search2/local.nhn?query=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=129.0569331%3B35.2033752&sm=clk&mpx=09170131%3A37.5305562%2C127.003086%3AZ8%3A0.2624685%2C0.1200371'
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
    @진행중 - 데
경기도2428
https://map.naver.com/search2/local.nhn?query=%EA%B2%BD%EA%B8%B0%EB%8F%84+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=128.606002%3B35.8497761&sm=clk&mpx=09620735%3A37.4469136%2C126.9422732%3AZ6%3A1.0490796%2C0.4796013

@@
대전356
https://map.naver.com/search2/local.nhn?query=%EB%8C%80%EC%A0%84%EA%B4%91%EC%97%AD%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=126.8701467%3B37.4905294&sm=clk&mpx=07170640%3A36.362109%2C127.3866083%3AZ7%3A0.5157685%2C0.2418416

@@
부산737
https://map.naver.com/search2/local.nhn?query=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=127.3983317%3B36.3376508&sm=clk&mpx=08470670%3A35.1673569%2C129.0940294%3AZ7%3A0.5028415%2C0.2489653

@진행중 - 맥
서울특별시2679
https://map.naver.com/search2/local.nhn?query=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=129.0569331%3B35.2033752&sm=clk&mpx=09170131%3A37.5305562%2C127.003086%3AZ8%3A0.2624685%2C0.1200371

@@
울산191
https://map.naver.com/search2/local.nhn?query=%EC%9A%B8%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=126.9876557%3B37.5647091&sm=clk&mpx=10200123%3A35.5695689%2C129.3672211%3AZ7%3A0.5043986%2C0.2501370

@@
인천534
https://map.naver.com/search2/local.nhn?query=%EC%9D%B8%EC%B2%9C%EA%B4%91%EC%97%AD%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=129.3349824%3B35.5579063&sm=clk&mpx=11177670%3A37.4642075%2C126.6931803%3AZ7%3A0.5254392%2C0.2386918

@@
전라남도211
https://map.naver.com/search2/local.nhn?query=%EC%A0%84%EB%9D%BC%EB%82%A8%EB%8F%84+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=126.6922987%3B37.4937981&sm=clk&mpx=12790340%3A34.8869477%2C127.0650024%3AZ5%3A2.0291921%2C0.9621535

@@
전라북도269
https://map.naver.com/search2/local.nhn?query=%EC%A0%84%EB%9D%BC%EB%B6%81%EB%8F%84+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=127.0466822%3B34.907989&sm=clk&mpx=13210380%3A35.8923889%2C126.915576%3AZ7%3A0.5141107%2C0.2398453

@@
제주특별자치도 110
https://map.naver.com/search2/local.nhn?query=%EC%A0%9C%EC%A3%BC%ED%8A%B9%EB%B3%84%EC%9E%90%EC%B9%98%EB%8F%84+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=126.923108%3B35.8803574&sm=clk&mpx=14110122%3A33.3846441%2C126.5061557%3AZ6%3A0.9996891%2C0.4768548

___

@@
충청남도346
https://map.naver.com/search2/local.nhn?query=%EC%B6%A9%EC%B2%AD%EB%82%A8%EB%8F%84+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=126.5311802%3B33.3807418&sm=clk&mpx=15200330%3A36.8089314%2C127.0846328%3AZ8%3A0.2598459%2C0.1202489

@@
충청북도293
https://map.naver.com/search2/local.nhn?query=%EC%B6%A9%EC%B2%AD%EB%B6%81%EB%8F%84+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=126.9000289%3B36.8378355&sm=clk&mpx=16113700%3A36.6452635%2C127.4728307%3AZ9%3A0.1293456%2C0.0605510


@@
세종특별자치도42
https://map.naver.com/search2/local.nhn?query=%EC%84%B8%EC%A2%85%ED%8A%B9%EB%B3%84%EC%9E%90%EC%B9%98%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=127.6857879%3B36.7841415&sm=clk&mpx=17110114%3A36.4967709%2C127.2689324%3AZ9%3A0.1292559%2C0.0603316

    """

