from elasticsearch import Elasticsearch
from tqdm import tqdm


class EsServer(object):
    def __init__(self, index):
        self.es = Elasticsearch(([{'host': '127.0.0.1', 'port': 9200}]))
        self.index = index

    def create_es_server(self, properties):
        body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "date_detection": False,
                "numeric_detection": True,
                "properties": properties
            }
        }
        self.es.indices.create(index=self.index, body=body)

    def es_search(self, query_body):
        search_result = self.es.search(index=self.index, body=query_body)
        print('Searching Response: ', search_result, '\n')
        print('Searching results: ')
        search_list = []
        for item in search_result['hits']['hits']:
            print(item['_source'])
            search_list.append(item['_source'])
        return search_list

    def delete_es_server(self):
        self.es.indices.delete(index=self.index)

    def write_es_server(self, lists):
        print('Writing results in elasticsearch server: ')
        for item in tqdm(lists):
            # print(item)
            self.es.index(index=self.index, body=item)

