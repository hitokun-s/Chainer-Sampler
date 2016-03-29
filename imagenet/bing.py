#! /usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import urllib
import requests
import json
# from urllib.parse import quote_plus

NUM = 100
keyBing = 'jsEog+xgBLvNEjTOaiU5mTQTT3KLcPKQjpMbLkNxYmI' #api keyを入れる

class BingAPI(object):
    API_URL_BASE = 'https://api.datamarket.azure.com/Bing/Search/v1/'
    def __init__(self, key):
        self._key = key

    def search(self, query, source='Web', top=50, skip=0):
        params = {
            'Query': urllib.quote("'%s'" % query),
            'Market': urllib.quote("'ja-JP'"),
            '$top': top,
            '$skip': skip,
            '$format': 'json'
        }
        url = self.API_URL_BASE + source + '?' + \
              '&'.join([key + '=' + str(params[key]) for key in params.keys()])
        auth = (self._key, self._key)
        res = requests.get(url, auth=auth)
        print res
        # return res.json()

def main():
    key = 'Primary Account Key'
    api = BingAPI(keyBing)
    json = api.search('たけのこの里')
    # for result in json['d']['results']:
    #     print('{Title}\t{Url}'.format(**result))

if __name__ == '__main__':
    main()