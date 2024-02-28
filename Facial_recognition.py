import time
import cv2
import numpy as np
import os


#이미지 얼굴 추출 및 저장
def Cutting_face_save(image, name):
    if(image.split('.')[-2] == 'jpg'):
        face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for(x,y,w,h)in faces:
            cv2.rectangle(image,(x,y), (x+w,y+h),(255,0,0),2)
            cropped = image[y: y+h, x:x+w]
            resize = cv2.resize(cropped,(180,180))
            #cv2.imshow("crop&resize",resize)
            cv2.imwrite(f"./resize_picture/{name}.jpg",resize)
        print(f"{good_cnt}/{len(file_list)} 작업완료")
        time.sleep(0.25)
    else:
        bad_cnt += 1
        print(f"png 파일입니다 {bad_cnt}")
        pass
    
    print(f"{good_cnt+bad_cnt}/{len(file_list)} 작업완료 [실패 : {bad_cnt}개]")
    time.sleep(0.25)


path_dir = "./picture"
file_list = os.listdir(path_dir)
file_list = sorted(file_list, key=lambda x: int(x.split('.')[0])) #순서정렬


file_name_list = []

for i in range(len(file_list)):
    file_name_list.append(file_list[i].replace(".jpg",""))

try:
    os.makedirs("./resize_picture")
    print(f"[resize_picture 디렉토리 생성]")
except:
    print(f"이미 있는 디렉토리입니다")
    pass


good_cnt = 1 
bad_cnt = 0

for name in file_name_list:
    img = cv2.imread("./picture/"+name+".jpg",1)
    Cutting_face_save(img,name)
    good_cnt += 1


print(f"성공률 {good_cnt}/{len(file_name_list)} 실패개수 : {bad_cnt}")