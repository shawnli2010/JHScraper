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

url = "http://list.le.com/listn/c1_t-1_a-1_y-1_s1_lg-1_ph-1_md_o3_d1_p.html"
chromedriver = webdriver.Chrome()
chromedriver.get(url)


#***************************************************************************#
#****** Keep scrolling the page to the bottom to load more movies **********#
#***************************************************************************#

'''Initial wait to load the initial set of movies before the first scroll'''
time.sleep(2.0)
while(True):    
    '''Scroll to the bottom of the page
       to load more movies'''
    chromedriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    html_after_scroll = chromedriver.page_source

    bs = BeautifulSoup(html_after_scroll)
    '''If there is no "Now Loading" on the page, then stop scrolling'''
    stop_scrolling = ( bs.find("div",{"class":"feed-loading","style":"display: block;"}) is None )
    if stop_scrolling: break     
    
    '''Scroll only one time for debug '''
    break


#***************************************************************************#
#********************* After loading all the movies ************************#
#***************************************************************************#    

html_after_scroll = chromedriver.page_source

bs = BeautifulSoup(html_after_scroll)
outer_list_div = bs.find("div",{"class":"list_cnt"})
movie_columns = outer_list_div.findAll("div",{"class":"layout"})

movie_tuple_list = []
count = 0
for column in movie_columns:
    movies = column.findAll("dl",{"class":"dl_list"})
    for movie in movies:        

        movie_name = movie.find("dd",{"class":"dd_cnt"}).find("p",{"class":"p_t"}).find("a").text        

        movie_data = movie.find("dd",{"class":"dd_cnt"}).find("p",{"class":["p_c ico_num"]})

        movie_score_em = movie_data.find("em",{"class":"blu"})
        movie_views_span = movie_data.find("span",{"class":"ico_play_num"})
        
        if(movie_score_em is not None):
            movie_score = movie_score_em.text
        else:
            movie_score = "0.0"
        
        if(movie_views_span is not None):
            movie_views = movie_views_span.text
        else:
            movie_views = "0"    
        
        '''PRINT-OUT'''
        print str(count) + ". " + movie_name + " Score: " + movie_score + " View: " + movie_views        

        '''Put the data into a list of tuples for inserting into MYSQL database'''
        movie_views = movie_views.replace(",","")
        movie_tuple = (count,movie_name,float(movie_score),int(movie_views))
        movie_tuple_list.append(movie_tuple)

        '''Increment count at the very last of loop'''
        count = count + 1

'''PRINT-OUT'''        
print "Total: " + str(count)

chromedriver.close() 


#***************************************************************************#
#********************* Insert into database ********************************#
#***************************************************************************#        

# try:
#     '''Insert all the data into database'''
#     insert_sql = """INSERT INTO LETV_MOVIE VALUES(%s,%s,%s,%s)"""    
#     db_cursor.executemany(insert_sql,movie_tuple_list)  
#     db.commit()
# except Exception ,err:
#     db.rollback()
#     print "Database has been rolled back because of an Exception !!!"
#     print(traceback.format_exc())
        






