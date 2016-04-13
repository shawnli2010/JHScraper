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
