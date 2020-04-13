from es_server import EsServer
import xlrd


def load_xlsx():
    workbook = xlrd.open_workbook("data/豆瓣读书榜单.xls")  # 文件路径
    '''对workbook对象进行操作'''
    # 获取所有sheet的名字
    names = workbook.sheet_names()

    # # 通过sheet名获得sheet对象
    worksheet = workbook.sheet_by_name("豆瓣读书")

    nrows = worksheet.nrows  # 获取该表总行数

    json_list = []
    for i in range(nrows):  # 循环打印每一行
        if i == 0:
            continue
        json = {
            '书名': worksheet.row_values(i)[0],
            '链接': worksheet.row_values(i)[1],
            '作者': worksheet.row_values(i)[2],
            '译者': worksheet.row_values(i)[3],
            '出版社': worksheet.row_values(i)[4],
            '出版日期': worksheet.row_values(i)[5],
            '售价': worksheet.row_values(i)[6],
        }
        json_list.append(json)
    return json_list


index = 'douban_book_top250'
es = EsServer(index)

es.delete_es_server()

properties = {
    "书名": {
        "type": "text"
    },
    "链接": {
        "type": "text",
        "index": False
    },
    "作者": {
        "type": "text"
    },
    "译者": {
        "type": "text"
    },
    "出版社": {
        "type": "text"
    },
    "出版日期": {
        "type": "keyword"
    },
    "售价": {
        "type": "text",
        "index": False
    }
}
es.create_es_server(properties)

es.write_es_server(load_xlsx())

search_keyword = '救赎'
body = {
    'query': {
        'match': {
            "书名": search_keyword
        }
    }
}

es.es_search(body)
