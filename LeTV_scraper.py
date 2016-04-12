import urllib2
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import MySQLdb
import traceback

url = "http://list.le.com/listn/c1_t-1_a-1_y-1_s1_lg-1_ph-1_md_o3_d1_p.html"
chromedriver = webdriver.Chrome()
chromedriver.get(url)

'''Initial wait to load the initial set of movies before the first scroll'''
time.sleep(2.0)
while(True):    
    '''Scroll to the bottom of the page
       to load more movies'''
    chromedriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    '''Wait until the new set of movies are loaded, then load the new page_source'''
    # time.sleep(2.0)
    html_after_scroll = chromedriver.page_source

    bs = BeautifulSoup(html_after_scroll)
    '''If there is no "Now Loading" on the page, then stop scrolling'''
    stop_scrolling = ( bs.find("div",{"class":"feed-loading","style":"display: block;"}) is None )
    if stop_scrolling: break     

 

#***************************************************************************#
#********************* After loading all the movies ************************#
#***************************************************************************#    

html_after_scroll = chromedriver.page_source

bs = BeautifulSoup(html_after_scroll)
outer_list_div = bs.find("div",{"class":"list_cnt"})
movie_columns = outer_list_div.findAll("div",{"class":"layout"})
count = 0
for column in movie_columns:
    movies = column.findAll("dl",{"class":"dl_list"})
    for movie in movies:
        movie_name = movie.find("dd",{"class":"dd_cnt"}).find("p",{"class":"p_t"}).find("a").text
        print movie_name
        count = count + 1
print "Total: " + str(count)        
        






