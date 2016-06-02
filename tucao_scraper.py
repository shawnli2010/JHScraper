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

db = MySQLdb.connect(host = "localhost",user = "root",passwd = "0924xiaopan",db = "JHSDB",charset = "utf8mb4", use_unicode = True )
db_cursor = db.cursor()
db_cursor.execute("SET NAMES utf8mb4")

url = "http://weibo.com/p/1005053177527181/home?profile_ftype=1&is_all=1#_0"
chromedriver = webdriver.Chrome()
chromedriver.get(url)

#***************************************************************************#
#****** Keep scrolling the page to the bottom to load more weibo  **********#
#***************************************************************************#

'''Initial wait to load the initial set of movies before the first scroll'''
next_page_link = None

time.sleep(2.0)
while(True):    
    '''Scroll to the bottom of the page
       to load more weibos'''
    chromedriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    html_after_scroll = chromedriver.page_source

    bs = BeautifulSoup(html_after_scroll)
    '''If there is no "Now Loading" on the page, then stop scrolling'''
    next_page_link = bs.find("a", {"class":"page next S_txt1 S_line1"}) 
    if next_page_link: 
        print "stop scolling"
        break     

page_number_link = bs.find("a", {"class":"page S_txt1"})
print page_number_link.text;

s_next_page_link =  chromedriver.find_element_by_link_text("下一页")   
s_next_page_link.click()