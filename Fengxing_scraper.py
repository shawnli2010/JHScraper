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

movie_list_url = "http://www.fun.tv/retrieve/c-e794b5e5bdb1.n-e5bdb1e78987.o-sc.pg-1.uc-23"
chromedriver = webdriver.Chrome()
chromedriver.get(movie_list_url)

root_url = "http://www.fun.tv"

html = chromedriver.page_source
bs = BeautifulSoup(html)

movie_list_div = bs.find("div",{"class":"mod-wrap-in mod-vd-lay-c6 fix"})
first_movie_box = movie_list_div.find("div",{"class":"mod-vd-i first"})
movie_boxes = movie_list_div.findAll("div",{"class":"mod-vd-i  "})
movie_boxes.append(first_movie_box)

for each_div in movie_boxes:
    info_div = each_div.find("div",{"class":"info"})
    movie_name = info_div.find("a").text
    movie_score = info_div.find("b").text

    sub_link_string = info_div.find("a")['href']
    movie_url = root_url + sub_link_string
    chromedriver.set_page_load_timeout(5)
    try:
        chromedriver.get(movie_url)
    except Exception, exception:
        if isinstance(exception, TimeoutError):
            print "aaaaaaaaaa"
        else:
            print "99999"
    # '''Click into each movie to get the views of each movie'''
    # movie_link = chromedriver.find_element_by_link_text(movie_name)
    # movie_link.click()

    # time.sleep(10)

    # print chromedriver.page_source
    
    break
    





