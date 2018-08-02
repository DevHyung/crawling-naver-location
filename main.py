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
'cookie': 'npic=Atbb0OFzirfYV1bptFCF2Zksn4Io9jVyOlMe2APKL/yZRj0SNGVsURuwvsJFwSZ+CA==; nx_ssl=2; _ga=GA1.2.598604263.1531729296; ASID=79a9092c00000164a28e4df600011423; nid_inf=1712338304; NID_AUT=zrtcDyq8sRXzCec2+ux+pALLzMLowrq8I8dJOqZXn0PsvrBugd2hdbD+CunTDt3m; NID_JKL=Ogb63rach1eJbzeaz1g0Q5173Ia0UrQjfLZT6gKSnzM=; BMR=s=1533173042812&r=https%3A%2F%2Fm.post.naver.com%2Fviewer%2FpostView.nhn%3FvolumeNo%3D16419411%26memberNo%3D217736&r2=https%3A%2F%2Fwww.facebook.com%2F; _naver_usersession_=xANqIUkZlbf8Jwu/91nEcg==; dNhxk7qHOpEEggfuhZfX4bO3G4="FNiU0gIQnFMr5lN64YllQED5d30=|X6rNeesZJuXPpTl5|1533186000000"; NID_SES=AAABkKfEEBtEpQjsT/I2pQngc0V2qUGcejeGC7zNkXft1f67+Xk/ViwDPevmQdDbN3MRU5gf02KmmQVyKTCmd9x8GRvdxFkY4/iIyOu++nahKe9b8EDUtkjfQ6jzUanuxpQ/A4YY7M3ZAcbY2huD3E5DBJy2UuB8mOxsk5TO7scbDv2aYbbdAWyU32DIK39IojBaBUe1lHMBG24Q/IDyPBmbmMrWu6TMCWfV6ePSMWzXZVDv14kwlo5S3L96jIW41YGDMSLP0zcLeu5NKTJ7sO3D5T7lm5yC6nNcPxCi0t2XzeXRPdSB2aPNCLxMDQ1GnjgGBEqzC3crJ6MVXcS/9UuOffL8aOMYyWEskj55w59+DeBk/yuyDMGoMJKA44f2Ma8d7wkfAZgQfa4lku/D2W/gNkfsC15PaY08qFO6t6eBRCiqj7hgA/eLq35rWsXBdxoqySiSTrx7ktyaF/6y6zwcqwsWQkJRn1Sfl2wEuPu3uIuCUWKhYBsuCqEKAxHO1hthYnViE1e20ZAUfhJWVx0uRfs=; JSESSIONID=F6C1F4514E8D23CFC6A980A9B3A22757; m4PGpz0VgtdSDwPOcG3X3ja31U="wsbrmg/p/Cr5hp2mtrp6sTVuTnM=|CVuuOv8f9BcaaPgy|1533191400000"; page_uid=T26knwpy71wssKl5u1ZssssssZd-408123',
'referer': 'https://map.naver.com/',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}
def get_data_by_json():
    global row
    for idx in range(1,1):
        url = 'https://map.naver.com/search2/local.nhn?query=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C+%ED%97%AC%EC%8A%A4%EC%9E%A5&page={}&type=SITE_1&queryRank=1&re=1&siteSort=0&menu=location&searchCoord=127.034232%3B37.5225475&sm=clk&mpx=09230536%3A37.5756587%2C127.0242719%3AZ7%3A0.5251888%2C0.2401626'
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
            break
        time.sleep(random.randint(4,7))
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
    workbook = xlsxwriter.Workbook('DATA.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['업소명', '도로명주소', '지번주소', '전화번호', '홈페이지1', '상세페이지'])
    row = 1
    col = 0
    #===PARSING
    get_data_by_json()
    #=== ~()
    workbook.close()
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

