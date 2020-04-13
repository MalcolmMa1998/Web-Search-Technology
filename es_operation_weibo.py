import json
from es_server import EsServer


def load_json():
    with open('data/weibo_search_result.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    return json_data


es = EsServer("weibo")

es.delete_es_server()

properties = {
    "user": {
        "type": "keyword"
    },
    "time": {
        "type": "text",
        "index": False
    },
    "text": {
        "type": "text"
    },
    "attitudes": {
        "type": "integer",
        "index": False
    },
    "comments": {
        "type": "integer",
        "index": False
    },
    "reposts": {
        "type": "integer",
        "index": False
    }
}
es.create_es_server(properties)

weibo_data = load_json()
es.write_es_server(weibo_data)

search_keyword = "美国"
body = {
    'query': {
        'match': {
            "text": search_keyword
        }
    }
}
es.es_search(body)
