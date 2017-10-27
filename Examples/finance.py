#!/usr/bin/env python3

from robobrowser import RoboBrowser
import json
from watson_developer_cloud import ToneAnalyzerV3
import os
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def stock_Search(company):
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    driver.set_window_size(1024, 768)
    driver.get("https://finance.google.com")
    #assert "Python" in driver.title
    search_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME,"q"))#Wait until element is loaded before interaction
        )

    search_box.clear
    search_box.send_keys(company, Keys.RETURN)
    assert "No results found." not in driver.page_source
    return driver
def stock_PriceFind(soup):
    stock_Data = soup.findAll("div", {"class" : "g-unit"})#Load banner block of stock data
    for x in stock_Data[1]:#For second item in data lest
        price = x.find("div", {"class" : "id-price-panel goog-inline-block"}).get_text()
        print(price)
    address = soup.findAll("div", {"class" : "sfe-section"})
    print(address[2].get_text())
company = input("Enter stock symbol: ")
driver = stock_Search(company)
sleep(4)
soup = BeautifulSoup(str(driver.page_source), "lxml")
stock_PriceFind(soup)