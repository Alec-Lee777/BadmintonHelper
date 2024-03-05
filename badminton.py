import base64
import json
from datetime import datetime, timedelta

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from retry import retry

code = ""  # 学号
password = ""  # 密码
site_no = 7
time = (("19:10", "20:10"), ("20:10", "21:10"))

session = requests.Session()


@retry(delay=5, jitter=(0, 5))
def login():
    url = "http://gym.hnu.edu.cn/gym/login"
    headers = {
        "Host": "gym.hnu.edu.cn",
        "Origin": "http://gym.hnu.edu.cn",
        "Referer": "http://gym.hnu.edu.cn/gym/book",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
    }
    session.get(url, headers=headers)
    url = "http://gym.hnu.edu.cn/gym/static/images/kaptcha.jpg"
    headers["Referer"] = "http://gym.hnu.edu.cn/gym/login"
    jpg = session.get(url, headers=headers).content
    b64 = base64.b64encode(jpg).decode()
    url = "http://api.jfbym.com/api/YmServer/customApi"
    payload = {
        "image": b64,
        "token": "Z77-bPX3ZDM0nwOIJbcvW95hLnhXbom5ah7X9bjy7Mc",
        "type": "10110"
    }
    resp = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    result = resp.json()
    if result["code"] != 10000:
        print(f"验证码识别失败: {result['msg']}")
        raise Exception
    url = "http://gym.hnu.edu.cn/gym/weixin/login/portal/login"
    captcha = resp.json()["data"]["data"]
    form_data = {
        "code": code,
        "password": password,
        "captcha": captcha,
        "flag": 1,
    }
    headers["Content-Type"] = "application/json; charset=UTF-8"
    with session.post(url, data=json.dumps(form_data), headers=headers) as resp:
        result = resp.json()
    if result["no"] != 2000:
        print(f"登录失败: {result['msg']}")
        raise Exception
    print("登录成功")


@retry(delay=5, jitter=(0, 5))
def book():
    url = "http://gym.hnu.edu.cn/gym/api/gym/order/create"
    site_id = 309 + site_no
    site_name = f"{site_no}号场"
    now = datetime.now()
    dt = now + timedelta(days=1)
    tomorrow = dt.strftime("%Y-%m-%d")
    form_data = {
        "account": code,
        "clientType": 1,
        "goods": [],
        "gymBooking": [
            {
                "startTime": f"{tomorrow} {start_time}:00",
                "endTime": f"{tomorrow} {end_time}:00",
                "gymSite": {
                    "id": site_id,
                    "name": site_name,
                },
            } for start_time, end_time in time
        ],
        "gymVenues": {
            "id": 68,
            "name": "南校区羽毛球馆",
        },
        "paymentType": 1,
    }
    headers = {
        "Host": "gym.hnu.edu.cn",
        "Origin": "http://gym.hnu.edu.cn",
        "Referer": "http://gym.hnu.edu.cn/gym/order/submit",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "Content-Type": "application/json; charset=UTF-8"
    }
    with session.post(url, data=json.dumps(form_data), headers=headers) as resp:
        result = resp.json()
    if result["no"] != 2000:
        print(f"预约失败: {result['msg']}")
        raise Exception
    print("预约成功")


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    now = datetime.now()
    dt = now.replace(hour=21, minute=58, second=0, microsecond=0)
    scheduler.add_job(login, "date", run_date=dt)
    dt = dt.replace(minute=59)
    scheduler.add_job(book, "date", run_date=dt)
    scheduler.start()
