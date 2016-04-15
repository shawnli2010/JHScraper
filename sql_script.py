#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb

####### TESTING ############## TESTING ############## TESTING #######
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "http://list.le.com/listn/c1_t-1_a-1_y-1_s1_lg-1_ph-1_md_o3_d1_p.html"
chromedriver = webdriver.Chrome()
chromedriver.get(url)

'''Initial wait to load the initial set of movies before the first scroll'''
time.sleep(2.0)

html_after_scroll = chromedriver.page_source
html_after_scroll = html_after_scroll.decode('utf-8')
bs = BeautifulSoup(html_after_scroll)
outer_list_div = bs.find("div",{"class":"list_cnt"})
movie_columns = outer_list_div.findAll("div",{"class":"layout"})

for column in movie_columns:
    movies = column.findAll("dl",{"class":"dl_list"})
    for movie in movies:        

        the_movie_name = movie.find("dd",{"class":"dd_cnt"}).find("p",{"class":"p_t"}).find("a").text        
        break
    break

chromedriver.close()

# print movie_name            
####### TESTING ############## TESTING ############## TESTING #######

####### CONNECTION #######
db = MySQLdb.connect("localhost","root","0924xiaopan","JHSDB" )
db_cursor = db.cursor()
db_cursor.execute("SET NAMES UTF8")

####### QUERY #######
'''Create the LeTV_Movie table'''
create_letv_movie_table_sql = """CREATE TABLE LETV_MOVIE(
                                        ID INT(11),
                                        MOVIE_NAME CHAR(255), 
                                        MOVIE_SCORE DOUBLE(2,1), 
                                        MOVIE_VIEWS INT(11) )
                                        ENGINE=InnoDB CHARACTER SET=utf8;"""
####### EXECTUION #######
# db_cursor.execute(create_letv_movie_table_sql)

movie_name = "熊出没之夺宝熊兵"

u1 = unicode(movie_name.decode('utf-8'))
# u2 = unicode(the_movie_name.decode('utf-8'))
# d2 = the_movie_name.decode('utf-8')

print u1
print movie_name.decode('utf-8')
# print movie_name

# print u2.encode('utf-8')
# print the_movie_name




# data_movie = (0,movie_name,7.5,200)

# list = []
# list.append(data_movie)
# list.append(data_movie)

# insert_chinese_sql = """INSERT INTO LETV_MOVIE VALUES(%s,%s,%s,%s)"""
db_cursor.execute("INSERT INTO LETV_MOVIE VALUES(%s,%s,%s,%s)",(0,the_movie_name,7.5,200))
# db_cursor.executemany(insert_chinese_sql,list)





# db_cursor.execute("SELECT MOVIE_NAME FROM LETV_MOVIE")
# fetched_data = db_cursor.fetchone()
# print fetched_data
# print movie_name

db.commit()
