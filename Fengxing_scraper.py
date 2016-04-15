#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import MySQLdb
import traceback

db = MySQLdb.connect("localhost","root","0924xiaopan","JHSDB" )
db_cursor = db.cursor()
db_cursor.execute("SET NAMES UTF8")

url = "http://www.fun.tv/retrieve/c-e794b5e5bdb1.n-e5bdb1e78987.o-sc.pg-1.uc-23"
chromedriver = webdriver.Chrome()
chromedriver.get(url)

html = chromedriver.page_source
bs = BeautifulSoup(html)

movie_list_div = bs.find("div",{"class":"mod-wrap-in mod-vd-lay-c6 fix"})
first_movie_box = movie_list_div.find("div",{"class":"mod-vd-i first"})
movie_boxes = movie_list_div.findAll("div",{"class":"mod-vd-i  "})
movie_boxes.append(first_movie_box)

count = 0
for movie_box in movie_boxes:
    print movie_box
    count = count + 1

print count    





