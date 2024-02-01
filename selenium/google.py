from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import ssl
import requests
from bs4 import BeautifulSoup

import time
import os
import socket
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from selenium.common.exceptions import ElementClickInterceptedException, NoAlertPresentException, ElementNotInteractableException
from PIL import Image

###이안아파트 버전


Chrome_options = webdriver.ChromeOptions()

wd = webdriver.Chrome('chromedriver', options=Chrome_options)
socket.setdefaulttimeout(30)

scraped_count =0

path = "./"

query = input("검색어 입력")

dir_name = path + query
os.makedirs(dir_name)
print(f"[{dir_name} 디렉토리 생성]")








# ssh 신뢰 해주는 부분
ssl._create_default_https_context = ssl._create_unverified_context

#새로운 크롬 창 열기
driver = webdriver.Chrome() 
driver.get("https://www.google.com/imghp?hl=ko&authuser=0&ogbl")    #크롬 창에 띄울 주소

#검색창에 검색하는부분
elem = driver.find_element(By.NAME, "q")
elem.send_keys("김채원")

#엔터
elem.send_keys(Keys.RETURN)


# 검색한 이미지를 클릭해서 큰 이미지로 다운받는 부분
cnt=1
image = driver.find_elements(By.CLASS_NAME,"rg_i.Q4LuWd")
print(len(image))
image2 = driver.find_elements(By.CSS_SELECTOR,".rg_i.Q4LuWd")
print(len(image2))

for image in image2:
    image.click()
    time.sleep(2)

    img_src = driver.find_element(By.CSS_SELECTOR,".sFlh5c.pT0Scc.iPVvYb").get_attribute("src")
    urllib.request.urlretrieve(img_src, str(cnt)+".jpg")
    cnt=cnt+1
    time.sleep(5)

    headers = {'User-Agent': "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content,'html.parser')

time.sleep(10)







# cnt=1
# images = driver.find_elements(By.CSS_SELECTOR,".rg_i.Q4LuWd")

# print(len(images))

# for image in images:
#     image.click()
#     time.sleep(2)
#     img_src = driver.find_element(By.CSS_SELECTOR,".sFlh5c.pT0Scc.iPVvYb").get_attribute("src")
#     urllib.request.urlretrieve(img_src, str(cnt)+".jpg")
#     cnt=cnt+1



# for image in images:
#     image.cilck()
#     time.sleep(2)
#     img_src = driver.find_element(By.CSS_SELECTOR,".sFlh5c.pT0Scc.iPVvYb").get_attribute("src")
#     urllib.request.urlretrieve(img_src, str(cnt)+".jpg")
#     cnt=cnt+1


# time.sleep(10)
# assert "Python" in driver.title
# elem.clear()
# elem.send_keys("pycon")
# assert "No results found." not in driver.page_source
# driver.close()





