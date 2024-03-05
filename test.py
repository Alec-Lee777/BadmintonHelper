from datetime import datetime, timedelta

import requests

url = "http://gym.hnu.edu.cn/gym/api/gym/order/create"
now = datetime.now()
dt = now + timedelta(days=1)
tomorrow = dt.strftime("%Y-%m-%d")
form_data = {
    "account": "S2310W1143",
    "clientType": 1,
    "goods": [],
    "gymBooking": [
        {
            "startTime": f"{tomorrow} 19:10:00",
            "endTime": f"{tomorrow} 20:10:00",
            "gymSite": {
                "id": 316,
                "name": "7号场",
            },
        },
        {
            "startTime": f"{tomorrow} 20:10:00",
            "endTime": f"{tomorrow} 21:10:00",
            "gymSite": {
                "id": 316,
                "name": "7号场",
            },
        },
    ],
    "gymVenues": {
        "id": 68,
        "name": "南校区羽毛球馆",
    },
    "paymentType": 1,
}
cookies = {"JSESSIONID": "B0B5442026A23364F0A7F8A230E8EAC2"}
headers = {
    "Host": "gym.hnu.edu.cn",
    "Origin": "http://gym.hnu.edu.cn",
    "Referer": "http://gym.hnu.edu.cn/gym/order/submit",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
    "Accept": "application/json, text/javascript, */*. g=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language":"zh-CN,zh;g=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Type": "application/json; charset=UTF-8"
}
resp = requests.post(url, data=form_data, cookies=cookies).content.decode("cp936")
print(resp)
