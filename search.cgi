#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from cgi import FieldStorage
from pytube import Search
from json import dumps
#from urllib import parse

print("Content-Type: application/json;charset=utf-8")
print()


form = FieldStorage()
id = form.getvalue('id') 

s = Search(id)

print('{ "items" : [')

for v in s.results:
  vidId = v.watch_url.split("=")[1]  #parse.parse_qs(parse.urlparse(v.watch_url).query)['v'][0]
  title = dumps(v.title)
  print(f' {{ "id" : {{ "videoId" : "{vidId}", "title": {title}, "url": "{v.watch_url}" }} }}, \n')

print(' { "id" : { } } ]}')

