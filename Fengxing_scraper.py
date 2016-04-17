#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import MySQLdb
import traceback

#***************************************************************************#
#********************* Helper methods **************************************#
#***************************************************************************#

def open_new_page(driver,url,timeout):

    if(driver is None): driver = webdriver.Chrome()
    driver.set_page_load_timeout(timeout)
    
    try:
        driver.get(url)
        new_page_html = driver.page_source
        soup = BeautifulSoup(new_page_html)

        print "Timeout value: " + str(timeout) + " might be larger than needed"        

        return (driver,soup)
    except Exception, exception:
        if isinstance(exception, TimeoutException):
            new_page_html = driver.page_source
            soup = BeautifulSoup(new_page_html)        
        else:
            print ("Some exception other than TimeoutException happened when open" +
                   "the page: " + url )
            print(traceback.format_exc())

        return (driver,soup)  

#***************************************************************************#
#*********************    Setup   ******************************************#
#***************************************************************************#
movie_list_page_timeout = 2
movie_page_timeout = 2

db = MySQLdb.connect("localhost","root","0924xiaopan","JHSDB" )
db_cursor = db.cursor()
db_cursor.execute("SET NAMES UTF8")

root_url = "http://www.fun.tv"
movie_list_url = "http://www.fun.tv/retrieve/c-e794b5e5bdb1.n-e5bdb1e78987.o-sc.pg-1.uc-23"

chromedriver = None
DS_tuple = open_new_page(chromedriver,movie_list_url,movie_list_page_timeout)
time.sleep(movie_list_page_timeout)
chromedriver = DS_tuple[0]
bsoup = DS_tuple[1]

movie_list_div = bsoup.find("div",{"class":"mod-wrap-in mod-vd-lay-c6 fix"})
first_movie_box = movie_list_div.find("div",{"class":"mod-vd-i first  "})
movie_boxes = movie_list_div.findAll("div",{"class":"mod-vd-i  "})
movie_boxes.append(first_movie_box)

count = 0
for each_div in movie_boxes:    
    info_div = each_div.find("div",{"class":"info"})
    movie_name_text = info_div.find("a").text
    movie_score_text = info_div.find("b").text

    sub_link_string = info_div.find("a")['href']
    movie_url = root_url + sub_link_string

    movie_page_timeout_t = movie_page_timeout

    '''(1) Open the individual movie page using the base timeout'''
    DS_tuple = open_new_page(chromedriver,movie_url,movie_page_timeout_t)
    time.sleep(movie_page_timeout_t)
    chromedriver = DS_tuple[0]
    bsoup = DS_tuple[1]

    while(True):

        movie_views_a = bsoup.find("a",{"class":"exp-num"})

        '''(2) If the individual movie page is not loaded completely'''
        if(movie_views_a is None):
            movie_page_timeout_t = movie_page_timeout_t + 1
            print "timeout incremented to " + str(movie_page_timeout_t) + " seconds for " + movie_name_text
            
            '''(3) If the timeout is too long, which means it might be a VIP movie without movie views available'''
            if(movie_page_timeout_t > 6):
                print "timeout too long"
                movie_views_text = "0"
                break

            DS_tuple = open_new_page(chromedriver,movie_url,movie_page_timeout_t)
            time.sleep(movie_page_timeout_t)
            chromedriver = DS_tuple[0]
            bsoup = DS_tuple[1]            
        else:
            movie_views_text = movie_views_a.text
            break
    
    print str(count) + ". " + movie_name_text + movie_views_text

    count = count + 1
    
    

          


    





