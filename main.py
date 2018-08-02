import xlsxwriter
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import requests
"""
workbook = xlsxwriter.Workbook('헬스장.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write_row(0,0,['업소명','도로명주소','지번주소','전화번호','홈페이지1','홈페이지2','상세페이지'])
row = 1
col = 0
#worksheet.write_row(row,col, [])
workbook.close()
"""
headers ={
'authority': 'map.naver.com',
'method':'GET',
'scheme': 'https',
'accept': 'application/json, text/javascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
'cookie': 'NNB=TGCBYRVSAFFVW; npic=Atbb0OFzirfYV1bptFCF2Zksn4Io9jVyOlMe2APKL/yZRj0SNGVsURuwvsJFwSZ+CA==; nx_ssl=2; _ga=GA1.2.598604263.1531729296; ASID=79a9092c00000164a28e4df600011423; nid_inf=1712338304; NID_AUT=zrtcDyq8sRXzCec2+ux+pALLzMLowrq8I8dJOqZXn0PsvrBugd2hdbD+CunTDt3m; NID_JKL=Ogb63rach1eJbzeaz1g0Q5173Ia0UrQjfLZT6gKSnzM=; BMR=s=1533173042812&r=https%3A%2F%2Fm.post.naver.com%2Fviewer%2FpostView.nhn%3FvolumeNo%3D16419411%26memberNo%3D217736&r2=https%3A%2F%2Fwww.facebook.com%2F; NID_SES=AAABi1Y9KD7P3wNCdYyoi7nmYi1O+GAL4tZTnDExr0Y+8BTmF7MiuKsCMl5rH3cc6d6dP6iEqDMa5il9hmO3ak2tYRjadJ1G30gyBhicv5Fu85C69aHGJ0QjxgEsfIqQ1k8t2XSG0BeY5iNcEspWMfY1Uw28ZfCgtWEntcEk47hDD+08ozZqzO/cLuqRLUtcTLeA/P5HOD6MSS49OMyqjk7R+1Ajuhzng5uqQaIbA5Nc6+GAM/cA77m/lIx0jWa8+h8qWOUQRZWa6kM7hyqMpjAQZWd0pncsGlJcuW2vF79My8OlFWNwSigEaLIOCIqIqOUzjm/8AemaHwaJhDXbWZTwdctlSdbjFuMhey+ZgMyk5K4iDrJT6HZKLdVg7HgBKx9B8QMW8fwgBPk+BMxjkhXTkXHD1lXgMtCjIYjTF8ERRVQJg3m9wSYrLtgncxdNI8Du0p9DOaKXFGWdWSZGfHLfuwM9/YMiomVfJ9yPODmD68ebm41I3pgNy9AUu6EZA+ZtQaSEAuq/+lEftZHDARmK2pg=; _naver_usersession_=xANqIUkZlbf8Jwu/91nEcg==; dNhxk7qHOpEEggfuhZfX4bO3G4="FNiU0gIQnFMr5lN64YllQED5d30=|X6rNeesZJuXPpTl5|1533186000000"; JSESSIONID=167D36B3C0FB5EE1463DB3124FE9F185; page_uid=T26KCspy724ss5rcX78ssssss48-099809',
'referer': 'https://map.naver.com/',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}
def get_data_by_json():
    url = 'https://map.naver.com/search2/local.nhn?query=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=127.034232%3B37.5225475&sm=clk&mpx=09230536%3A37.5756587%2C127.0242719%3AZ7%3A0.5251888%2C0.2401626'
    html = requests.get(url.format(5),headers=headers)
    jsonStr = json.loads(html.text)
    results = jsonStr['result']['site']['list']
    print(results[0])

def get_query_list():
    queryList = []
    tmp = '<ul class="sa_lst _sub_region_lists"><li><a href="#" class="nclicks(plc*Z.list)" title="강원도" data-query="강원도 헬스장">강원도</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="경기도" data-query="경기도 헬스장">경기도</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="경상남도" data-query="경상남도 헬스장">경상남도</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="경상북도" data-query="경상북도 헬스장">경상북도</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="광주광역시" data-query="광주광역시 헬스장">광주광역시</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="대구광역시" data-query="대구광역시 헬스장">대구광역시</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="대전광역시" data-query="대전광역시 헬스장">대전광역시</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="부산광역시" data-query="부산광역시 헬스장">부산광역시</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="서울특별시" data-query="서울특별시 헬스장">서울특별시</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="울산광역시" data-query="울산광역시 헬스장">울산광역시</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="인천광역시" data-query="인천광역시 헬스장">인천광역시</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="전라남도" data-query="전라남도 헬스장">전라남도</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="전라북도" data-query="전라북도 헬스장">전라북도</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="제주특별자치도" data-query="제주특별자치도 헬스장">제주특별자치...</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="충청남도" data-query="충청남도 헬스장">충청남도</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="충청북도" data-query="충청북도 헬스장">충청북도</a></li><li><a href="#" class="nclicks(plc*Z.list)" title="세종특별자치시" data-query="세종특별자치시 헬스장">세종특별자치...</a></li></ul>'
    bs4 = BeautifulSoup(tmp, 'lxml')
    lis = bs4.find_all('li')
    for li in lis:
        queryList.append(li.a['data-query'])
    return queryList
if __name__ == "__main__":
    get_data_by_json()
    exit(-1)
    """
    #경기 강원 경상남도 경상북도 
    # 광주,대구,대전,부산,서울특별,울산,인천광역시
    # 전라남도 전라북도 제주특별자치
    # 충첨남도 충청북도 세종특별자치
    print (  2428 + 244 + 566 + 408 )
    print ( 285+ 507 + 356 + 736 + 2678 +  191 +533)
    print( 210+ 269 +110)
    print ( 347+293+42)
    print( 3646+5286+589+682)
    """
    #=== GLOBAL
    detailBaseUrl = 'https://map.naver.com/local/siteview.nhn?code='
