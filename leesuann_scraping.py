import time
import os
import socket
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from selenium.common.exceptions import ElementClickInterceptedException, NoAlertPresentException, ElementNotInteractableException
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import ssl



#ssh 오류 해결 코드
ssl._create_default_https_context = ssl._create_unverified_context


#스크롤 내리는 함수
def scroll_down():
    scroll_count = 1
    print("[scroll_down(): 스크롤 다운 시작]")

    last_height = wd.execute_script("return document.body.scrollHeight")
    after_click = False

    while True:
        print(f"[스크롤 다운: {scroll_count}]")
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_count += 1
        time.sleep(1)

        new_height = wd.execute_script("return document.body.scrollHeight")

        if last_height == new_height:
            if after_click is True:
                break
            else:
                try:
                    more_button = wd.find_element(By.XPATH,'//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
                    if more_button.is_displayed():
                        more_button.click()
                        after_click = True
                except NoSuchElementException as e:
                    print(e)
                    break
        last_height = new_height

#클릭 및 저장하는 함수
def click_and_save(dir_name, index, img, img_list_length):
    global scraped_count

    try:
        #img.click()
        #img.send_keys(Keys.ENTER)
        wd.execute_script("arguments[0].click();", img)
        time.sleep(0.1)
        try:
            src = wd.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]').get_attribute('src')
        except:
            src = wd.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[2]/div/a/img[1]').get_attribute('src')        
        if src.split('.')[-1] == 'png':
            urlretrieve(src, dir_name + '/' + str(scraped_count+1) + ".png")
            print(f"{index+1}/{img_list_length} type 1 PNG 이미지 저장[총 {scraped_count+1}장]")
            scraped_count += 1
        elif src.split('.')[-1] == 'jpg':
            urlretrieve(src, dir_name + '/' + str(scraped_count+1) + ".jpg")
            print(f"{index+1}/{img_list_length} type 1 JPG 이미지 저장[총 {scraped_count+1}장]")
            scraped_count += 1
        elif src.find('png'):
            urlretrieve(src, dir_name + '/' + str(scraped_count+1) + ".png")
            print(f"{index+1}/{img_list_length} type 2 PNG 이미지 저장[총 {scraped_count+1}장]")
            scraped_count += 1        
        elif src.find('jpg'):
            urlretrieve(src, dir_name + '/' + str(scraped_count+1) + ".jpg")
            print(f"{index+1}/{img_list_length} type 2 JPG 이미지 저장[총 {scraped_count+1}장]")
            scraped_count += 1
        else:
            urlretrieve(src, dir_name + '/' + str(scraped_count+1) + ".jpg")
            print(f"{index+1}/{img_list_length} type 3 JPG 이미지 저장[총 {scraped_count+1}장]")
            scraped_count += 1
            
    except NoSuchElementException as e:
        print(f"{index+1}/{img_list_length} click_and_save 함수 예외처리 : ",e)
        pass
    except HTTPError as e:
        print(f"{index+1}/{img_list_length} click_and_save 함수 예외처리 : ",e)
        pass
    except ElementClickInterceptedException as e:
        print(f"{index+1}/{img_list_length} click_and_save 함수 예외처리 : ",e)
        pass

#이미지 스크레핑 함수
def scraping(dir_name, query):
    global scraped_count
    url = f"https://www.google.com/search?q={query}&sca_esv=0f81dff0e80388d2&hl=ko&authuser=0&tbm=isch&source=hp&biw=1920&bih=919&ei=GIa7ZanhCMnCvr0P8O6ImAs&iflsig=ANes7DEAAAAAZbuUKHQ6evRY_EeUzZ-67WcZN0kvwImY&udm=&ved=0ahUKEwipzfeWioqEAxVJoa8BHXA3ArMQ4dUDCA8&uact=5&oq=%E3%85%81%E3%85%81%E3%85%81&gs_lp=EgNpbWciCeOFgeOFgeOFgTIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIzxFQpgJY7Q9wA3gAkAEAmAGRAaAB9gKqAQMwLjO4AQPIAQD4AQGKAgtnd3Mtd2l6LWltZ6gCAMICCBAAGIAEGLED&sclient=img"
    wd.get(url)
    wd.maximize_window()
    time.sleep(2)
    scroll_down()

    div = wd.find_element(By.XPATH,'//*[@id="islrg"]/div[1]')
    img_list = div.find_elements(By.CSS_SELECTOR,'div.fR600b.islir > img')

    for index, img in enumerate(img_list):
        
        try:
            click_and_save(dir_name, index, img, len(img_list))
            
        except ElementClickInterceptedException as e:
            print(f"scraping 함수 예외처리 : ",e)
            wd.execute_script("window.scrollTo(0, window.scrollY + 100)")
            time.sleep(1)
            click_and_save(dir_name, index, img, len(img_list))
        except NoSuchElementException as e:
            print(f"scraping 함수 예외처리 : ",e)
            wd.execute_script("window.scrollTo(0, window.scrollY + 100)")
            time.sleep(1)
            click_and_save(dir_name, index, img, len(img_list))
        except ConnectionResetError as e:
            print(f"scraping 함수 예외처리 : ",e)
            pass
        except URLError as e:
            print(f"scraping 함수 예외처리 : ",e)
            pass
        except socket.timeout as e:
            print(f"scraping 함수 예외처리 : ",e)
            pass
        except socket.gaierror as e:
            print(f"scraping 함수 예외처리 : ",e)
            pass
        except ElementNotInteractableException as e:
            print(f"scraping 함수 예외처리 : ",e)
            break
        time.sleep(0.5)

    try:
        print("[스크래핑 종료 (성공률: %.2f%%)]" %(scraped_count/len(img_list)*100))
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError 예외처리 : ",e)

    wd.quit()

#일정 해상도 이하이거나 손상된 이미지 제거
def filter_and_remove(dir_name,query, filter_size):
    filtered_count = 0

    for index, file_name in enumerate(os.listdir(dir_name)):
        try:
            file_path = os.path.join(dir_name, file_name)
            img = Image.open(file_path)

            if img.width < filter_size and img.height < filter_size:
                img.close()
                os.remove(file_path)
                print(f"{index} 이미지 제거")
                filtered_count += 1
        except OSError as e:
            print(e)
            os.remove(file_path)
            filtered_count += 1

    print(f"[이미지 제거 개수: {filtered_count}/{scraped_count}]")




options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
        
# 크롬 드라이버 최신 버전 설정
#service = ChromeService(executable_path=ChromeDriverManager().install())
        
# chrome driver
#wd = webdriver.Chrome(service=service, options=options) # <- options로 변경
wd = webdriver.Chrome()
socket.setdefaulttimeout(30)

scraped_count =0

path = "./"
query = input("검색어 입력 : ")
dir_name = path + query

try:
    os.makedirs(dir_name)
    print(f"[{dir_name} 디렉토리 생성]")
except:
    print(f"이미 있는 디렉토리입니다")
    pass

scraping(dir_name, query)
filter_and_remove(dir_name,query, 400)





