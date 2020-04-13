import requests
from bs4 import BeautifulSoup
import csv


def get_movies():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) '
                      'Chrome/17.0.963.56 Safari/535.11',
        'Host': 'movie.douban.com'
    }
    movie_list = []
    for i in range(0, 10):
        link = 'https://movie.douban.com/top250?start=' + str(i * 25)
        r = requests.get(link, headers=headers, timeout=10)
        if r.status_code != 200:
            print('页面无响应')

        soup = BeautifulSoup(r.text, "lxml")
        div_list = soup.find_all('div', class_='hd')
        for each in div_list:
            movie = each.a.span.text.strip()
            movie_list.append(movie)
    return movie_list


result = get_movies()

with open('data/douban_movie_top250.csv', 'w') as f:
    # 实例化csv.writer对象
    writer = csv.writer(f)
    writer.writerows(result)

url = "http://www.baidu.com"  # 目 标 网 址
html = requests.get(url)
print(html)
