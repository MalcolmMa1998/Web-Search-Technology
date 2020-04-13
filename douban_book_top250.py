import requests
from bs4 import BeautifulSoup
import xlwt


def get_books(link, row_num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) '
                      'Chrome/17.0.963.56 Safari/535.11',
        'Host': 'book.douban.com'
    }
    resp = requests.get(link, headers=headers, timeout=10)
    home_page_html = resp.text
    soup = BeautifulSoup(home_page_html, "html.parser")

    j = row_num
    k = row_num

    items_title = soup.find_all("div", class_="pl2")
    for i in items_title:
        tag = i.find("a")
        # Remove Space and \n
        name = ''.join(tag.text.split())
        sheet.write(j, 0, name)
        link = tag["href"]
        title_results = "[{}]({})".format(name, link)
        print(title_results)
        sheet.write(j, 1, link)
        j += 1

    items_author = soup.find_all("p", class_="pl")
    for i in items_author:
        author_results = i.text
        print(author_results)
        author_results = author_results.split(" / ")
        if (len(author_results) == 4):
            author_results.insert(1, "-")
        for r in range(len(author_results)):
            sheet.write(k, 2 + r, author_results[r])
        k += 1


workbook = xlwt.Workbook()
sheet = workbook.add_sheet('豆瓣读书')
head = ['书名', '链接', '作者', '译者', '出版社', '出版日期', '售价']
for h in range(len(head)):
    sheet.write(0, h, head[h])

for i in range(0, 10):
    link = 'https://book.douban.com/top250?start=' + str(i * 25)
    row_num = i * 25 + 1
    get_books(link, row_num)

workbook.save('../data/豆瓣读书榜单.xls')
