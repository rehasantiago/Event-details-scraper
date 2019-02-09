import sys
#sys.path.append(sys.path[0]+'/tenT_Library/') #Use when library is in sub directory
from scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime
from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import lxml.html
import os
import random
import re
import csv
import itertools

months = ['January','February','March','April','May','June','July','August','September','October','November','December']

bot = Scraper(__file__)

def scrape_page(url,j):
    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = False
    driver = bot.getRequest(url=url,cap=cap,exec_path="geckodriver.exe",flag=1)#path of your driver
    if driver["status"]["code"]:
        driver = driver["data"]
        data_dic = {}
        try:
            name = driver.find_element_by_xpath('//div[@class="inside"]//div[2]//h1').text
        except:
            name = ''

        try:
            date = driver.find_element_by_xpath('//p[@class="catal-ed-main-address"]//span[1]').text
        except:
            date = ''
        if date!='':
            date = date.replace('From','').replace('to','').split('/')
            date[0] = date[0].replace(' ','')
            if len(date)>3:
                date = date[0] + '-' + date[3] + ' ' + months[int(date[1])-1] + ',' + date[-1]
            elif len(date)==3:
                date[0] = date[0].replace('The','')
                date = date[0] + ' ' + months[int(date[1])-1] + ' ' + date[-1]
            else:
                date = months[int(date[0])-1] + ' ' +date[-1]
        try:
            location = driver.find_element_by_xpath('//p[@class="catal-ed-main-address"]//span[2]').text
        except:
            location = ''
        try:
            website_url = driver.find_element_by_xpath('//div[@class="catal-ed-main-infos"]//p[2]//a').get_attribute('href')
        except:
            website_url = ''
        data_dic['record'] = j
        data_dic['event_name'] = name
        data_dic['event_url'] = website_url
        data_dic['event_date'] = date
        data_dic['event_location'] = location
        print(data_dic)
        return data_dic
    else:
        print(['status']['message'])
        return None


############ Create Object ###########

def pageNumbers(link):
    ret = 1
    
############ Sending Request ###########

    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = False
    driver = bot.getRequest(url=link,cap=cap,exec_path="geckodriver.exe",flag=1)#path of driver
    if driver["status"]["code"]:
        driver = driver["data"]
        source_data = driver.page_source
        soup = BeautifulSoup(source_data, "html.parser")
        #soup = BeautifulSoup(page["data"].text, 'html.parser')
        ret_details = soup.find('div',attrs={"class": "pagination__pages"}).findAll('a')
        print(ret_details)
        for retd in ret_details:
            try:
                ret = max (ret, int(retd.text))
            except:
                pass
        return ret
    else:
        print(driver["status"]["message"])
        return None

#################### Logic ####################
def main1 (defaultlink):  
    ret =[]
    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = False
    driver = bot.getRequest(url=defaultlink,cap=cap,exec_path="geckodriver.exe",flag=1)#path of driver
    if driver["status"]["code"]:
        driver = driver["data"]
        driver.maximize_window() 
        j=1
        links = [e.text for e in driver.find_elements_by_xpath('//ul[@class="esf-results-alpha-list"]//li[3]//a')]
        driver.quit()
        for i in links:
            url = "https://www.comexposium.com/Events-Index/Find-an-event/(start_with)/"
            url = url + i
            driver = bot.getRequest(url=url,cap=cap,exec_path="geckodriver.exe",flag=1)
            if driver["status"]["code"]:
                driver = driver["data"]
                try:
                    links_on_each_page = [e.get_attribute('href') for e in driver.find_elements_by_xpath('//h3[@class="catal-ex-item-title"]//a')]
                    for i in links_on_each_page:
                        data_dic = scrape_page(i,j)
                        ret.append(data_dic)
                        j=j+1
                except:
                    pass
                driver.quit()
            else:
                print(driver['status']['message'])
        return ret       
    else:
        print(driver['status']['message'])
        return None
    

    
data = main1("https://www.comexposium.com/Events-Index/Find-an-event")
        
file = bot.saveData(data)
print(file)

    
sys.exit()
