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

db = MySQLdb.connect("localhost","root","0924xiaopan","JHSDB" )
db_cursor = db.cursor()
db_cursor.execute("SET NAMES UTF8")

root_url = "http://www.fun.tv"
movie_list_url = "http://www.fun.tv/retrieve/c-e794b5e5bdb1.n-e5bdb1e78987.o-sc.pg-1.uc-23"

chromedriver = None
DS_tuple = open_new_page(chromedriver,movie_list_url,2)
time.sleep(2)
chromedriver = DS_tuple[0]
bsoup = DS_tuple[1]

movie_list_div = bsoup.find("div",{"class":"mod-wrap-in mod-vd-lay-c6 fix"})
first_movie_box = movie_list_div.find("div",{"class":"mod-vd-i first"})
movie_boxes = movie_list_div.findAll("div",{"class":"mod-vd-i  "})
movie_boxes.append(first_movie_box)

for each_div in movie_boxes:
    info_div = each_div.find("div",{"class":"info"})
    movie_name_text = info_div.find("a").text
    movie_score_text = info_div.find("b").text

    sub_link_string = info_div.find("a")['href']
    movie_url = root_url + sub_link_string

    DS_tuple = open_new_page(chromedriver,movie_url,3)
    time.sleep(3)
    chromedriver = DS_tuple[0]
    bsoup = DS_tuple[1]

    movie_view_text = bsoup.find("a",{"class":"exp-num"}).text
    print movie_view_text


    # try:
    #     chromedriver.get(movie_url)
    # except Exception, exception:
    #     if isinstance(exception, TimeoutException):
    #         each_movie_html = chromedriver.page_source
    #         bs = BeautifulSoup(each_movie_html)
    #         movie_view_text = bs.find("a",{"class":"exp-num"}).text

    #         chromedriver.get(movie_list_url)
    #     else:
    #         print ("Some exception other than TimeoutException happened when open",
    #                "each individual movie's page")
    # '''Click into each movie to get the views of each movie'''
    # movie_link = chromedriver.find_element_by_link_text(movie_name)
    # movie_link.click()

    # time.sleep(10)

    # print chromedriver.page_source
    
    break

          


    





