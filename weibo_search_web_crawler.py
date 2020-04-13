import requests
from urllib.parse import urlencode, quote
import pandas as pd
import re
from pyquery import PyQuery as pq
import time
import string
import json


def get_page(base_url, refer, headers, page):
    params = {
        'sudaref': 'login.sina.com.cn',
        'display': '0',
        'retcode': '6102',
        'page': page
    }
    url = refer + urlencode(params)
    print("url: ", url)
    try:
        while True:
            response = requests.get(url, headers=headers)
            print("response.status_code: ", response.status_code)
            if response.status_code == 200:
                return response.json()
            else:
                continue
    except requests.ConnectionError as e:
        print("Error", e.args)


def time_change(in_time, starttime):
    if "今天" in in_time:
        thisStartTime = time.localtime(float(starttime))
        otherStyleTime = str(time.strftime("%Y‐%m‐%d", thisStartTime))
        creatTime = otherStyleTime + " " + in_time.split(" ")[1] + ":00"
        return creatTime
    elif "昨天" in in_time:
        thisStartTime = time.localtime(float(starttime - 86400))
        otherStyletime = str(time.strftime("%Y-%m-%d", thisStartTime))
        creatTime = otherStyletime + " " + in_time.split(" ")[1] + ":00"
        return creatTime
    elif "前天" in in_time:
        thisStartTime = time.localtime(float(starttime - 86400 * 2))
        otherStyletime = str(time.strftime("%Y‐%m‐%d", thisStartTime))
        creatTime = otherStyletime + " " + in_time.split(" ")[1] + ":00"
        return creatTime
    elif "刚刚" in in_time:
        thisStartTime = time.localtime(float(starttime))
        otherStyletime = str(time.strftime("%Y‐%m‐%d %H:%M:%S", thisStartTime))
        return otherStyletime
    elif "分钟前" in in_time:
        creatTime = 60 * float(in_time.strip("分 钟 前"))
        thisStartTime = time.localtime(float(starttime) - creatTime)
        otherStyletime = str(time.strftime("%Y‐%m‐%d %H:%M:%S", thisStartTime))
        return otherStyletime
    elif "小时前" in in_time:
        creatTime = 3600 * float(in_time.strip("小 时 前"))
        thisStartTime = time.localtime(float(starttime) - creatTime)
        otherStyletime = str(time.strftime("%Y‐%m‐%d %H:%M:%S"), thisStartTime)
        return otherStyletime
    else:
        return "2018‐" + in_time + ":00"


def remove_emoji(text):
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00‐\ude4f])|"  # emoticons 
        u"(\ud83c[\udf00‐\uffff])|"  # symbols & pictographs (1 of 2) 
        u"(\ud83d[\u0000‐\uddff])|"  # symbols & pictographs (2 of 2) 
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0‐\uddff])"  # flags (iOS) 
        "+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def parse_page(json, df, page, result):
    r1 = u'[’"$%&\'()*+‐/<=>?@￿、...【】《》[\\]^_`{|}~]+'
    r2 = re.compile(u'[\U00010000‐\U0010ffff]')
    if json:
        try:
            starttime = json.get('data').get('cardlistInfo').get('starttime')
        except:
            print("Gettimeerror")
        else:
            items = json.get('data').get('cards')
            for i, item1 in enumerate(items):
                try:
                    item2 = item1.get('mblog')
                #                     print("item2:", item2)
                except:
                    continue
                else:
                    weibo = {}
                    try:
                        # 这 一 部 分 的 内 容 需 要 根 据 自 己 的 需 求， 观 察Preview中 的 数 据 结 构 进 行 适 当 的 修 改
                        weibo['user'] = item2.get('user')['screen_name']
                        weibo['time'] = time_change(item2.get('created_at'), starttime)
                        weibo['text'] = re.sub(r1, "", pq(item2.get('text')).text())
                        weibo['text'] = remove_emoji(weibo['text'])
                        weibo['text'] = r2.sub('', weibo['text'])
                        weibo['attitudes'] = item2.get('attitudes_count')
                        weibo['comments'] = item2.get('comments_count')
                        weibo['reposts'] = item2.get('reposts_count')
                        df.loc[i + 1 + (page - 1) * 10] = [weibo['user'], weibo['time'],
                                                           weibo['text'], weibo['attitudes'],
                                                           weibo['comments'], weibo['reposts']]
                    except:
                        continue
                    else:
                        result.append(weibo)
                        continue


def weibo_parse(parse_word, max_page, result):
    count = 0
    base_url = 'https://m.weibo.cn/api/container/getIndex?'
    refer = r'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D' + parse_word + '&page_type=searchall'
    refer = quote(refer, safe=string.printable)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) '
                      'Chrome/17.0.963.56 Safari/535.11',
        'Host': 'm.weibo.cn',
        'Referer': refer,
        'X-Requested-With': 'XMLHttpRequest',
    }

    df = pd.DataFrame(columns=['user', 'time', 'text', 'attitudes', 'comments', 'reports'])
    df.index = range(len(df))

    for page in range(max_page + 1):
        print("yes")
        json = get_page(base_url, refer, headers, page)
        print("ok")
        parse_page(json, df, page, result)
        time.sleep(1)


keywords = "疫情"  # 修改要搜索的关键字
max_page = 30  # 设置的最大页数
result = []  # 设置生成结果容器

weibo_parse(keywords, max_page, result)

filename = 'data/weibo_search_result.json'
with open(filename, 'w', encoding='utf-8') as file_obj:
    json.dump(result, file_obj, ensure_ascii=False)
