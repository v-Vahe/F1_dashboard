from urllib import response
import requests
import pandas as pd
import time 

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
_BASE_URL = 'http://ergast.com/api/f1'


class F1Requests():
    def __init__(self, headers = None, user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"):
        self.user_agent = user_agent
        self.headers = {"User-Agent": user_agent} 
        self.tables_list = self._list_tables()
        # self.current_seasons = []
        # self.table_counts = self.num_rows()

    def request_seasons(self, url = '/seasons', limit = 30, ofset = 0):
        url = self._url_parse(url)
        return self.request_json(url)['MRData']['SeasonTable']['Seasons']
        

    def request_json(self, url,headers = None, params = None, limit = 30, offset = 0):
        assert limit <= 30; 'limit needs to be set 0 for antiblocking policy'
        url = self._url_parse(url)
        if headers != None:
            headers = self.headers
        if params == None:
            params = {'limit':limit, 'offset':offset}
        print(limit)
        response = requests.get(url, params = params, headers=headers, stream = True, timeout=10)
        response.raise_for_status()
        time.sleep(2)
        return response.json()

    def num_rows(self, url):
        url = self._url_parse(url)
        response = self.request_json(url, limit = 0)
        return response['MRData']['total']

    def _list_tables(self, filepath = 'f1_pipeline/f1_sql_server/ordered_tables_list.txt'):
        with open(filepath) as file:
            tables = file.read().splitlines()
        return tables

    def _url_parse(self, url):
        if _BASE_URL not in url:
            url = _BASE_URL + url
        if url[-5:] != '.json':
            url = url + '.json'
        return url

if __name__ == '__main__':
    f1_request = F1Requests()
    seasons = pd.json_normalize(f1_request.request_seasons(url = '/2021/seasons'))
    print(seasons)