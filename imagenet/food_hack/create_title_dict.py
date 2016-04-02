#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3

conn = sqlite3.connect("food.sqlite")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS material_dict (wnid VARCHAR PRIMARY KEY  NOT NULL , title VARCHAR)")

dict = {}
f = open("words.txt")
line = f.readline().strip() # strip()で末尾の改行文字を除く

while line:
    wnid,title = line.split("\t")
    dict[wnid] = title
    line = f.readline()
f.close

data = []
for wnid, title in dict.items():
    data.append((wnid, title))
c.executemany("insert into material_dict(wnid, title) values (?,?)", data)
conn.commit()
conn.close()