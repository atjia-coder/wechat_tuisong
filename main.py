from time import time, localtime

import bs4
import requests

import cityinfo
import config
from requests import get, post
from datetime import datetime, date

# 想要获取的信息 --及其api
#22 - 12 -1 刷新Git提交第一次

# 封装Request
def get_ad():
    baseUrl = 'http://www.weather.com.cn/weather1d/'
    config_city = str(101180101)
    Url_A = baseUrl + config_city + '.shtml'
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                        '104.0.5112.102Safari / 537.36Edg / 104.0.1293.70 '
    }
    # url_request = urllib.request.Request(url=Url_A, headers=headers)
    content = requests.get(url= Url_A,headers=headers).content.decode('utf-8')
    # print(content)
    soup = bs4.BeautifulSoup(content, 'html.parser')
    condition = soup.select('.left-div .livezs .clearfix em')
    discription = soup.select('.left-div .livezs .clearfix span')
    advince = soup.select('.left-div .livezs .clearfix p')
    print(condition)
    print(discription)
    print(advince)
    return condition,discription,advince

def get_access_token():
    # appId
    app_id = config.app_id
    # appSecret
    app_secret = config.app_secret
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    access_token = get(post_url).json()['access_token']
    # print(access_token)
    return access_token


def get_weather(province, city):
    # 城市id
    city_id = cityinfo.cityInfo[province][city]["AREAID"]
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
      "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn


def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en



def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, note_ch, note_en,adjest_con,adjest_discr,adjest_advi):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday()]
    # 获取在一起的日子的日期格式
    love_year = int(config.love_date.split("-")[0])
    love_month = int(config.love_date.split("-")[1])
    love_day = int(config.love_date.split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取生日的月和日
    birthday_month = int(config.birthday.split("-")[1])
    birthday_day = int(config.birthday.split("-")[2])
    # 今年生日
    year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    data = {
        "touser": to_user,
        "template_id": config.template_id,
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": "#00FFFF"
            },
            "city": {
                "value": city_name,
                "color": "#808A87"
            },
            "weather": {
                "value": weather,
                "color": "#ED9121"
            },
            "min_temperature": {
                "value": min_temperature,
                "color": "#00FF00"
            },
            "max_temperature": {
              "value": max_temperature,
              "color": "#FF6100"
            },
            "Nolove_day": {
              "value": love_days,
              "color": "#87CEEB"
            },
            "birthday": {
              "value": birth_day,
              "color": "#FF8000"
            },
            "note_en": {
                "value": note_en,
                "color": "#173177"
            },
            "note_ch": {
                "value": note_ch,
                "color": "#173177"
            },
            "adjest_con0":{
                "value": adjest_con[0].string,
                "color": "#5455510"
            },
            "adjest_discr0": {
                "value": adjest_discr[0].string,
                "color": "#456177"
            },
            "adjest_advi0":{
                "value": adjest_advi[0].string,
                "color": "#512348"
            },
            "adjest_con1": {
                "value": adjest_con[1].string,
                "color": "#5455510"
            },
            "adjest_discr1": {
                "value": adjest_discr[1].string,
                "color": "#456177"
            },
            "adjest_advi1": {
                "value": adjest_advi[1].string,
                "color": "#512348"
            },
        }
    }
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data)
    print(response.text)

# 获取accessToken
accessToken = get_access_token()
# 接收的用户
user = config.user
# 传入省份和市获取天气信息
province, city = config.province, config.city
weather, max_temperature, min_temperature = get_weather(province, city)
# 获取词霸每日金句
note_ch, note_en = get_ciba()
#每日建议
adjest_con,adjest_discr,adjest_advi = get_ad()
# 公众号推送消息
send_message(user, accessToken, city, weather, max_temperature, min_temperature, note_ch, note_en,adjest_con,adjest_discr,adjest_advi)