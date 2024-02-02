from bs4 import BeautifulSoup
import requests
import os

def download_images(query, num_images):
    base_url = 'https://www.google.co.in'
    url = base_url + "/search?q=" + query + "&source=lnms&tbm=isch"
    headers = {'User-Agent': "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content,'html.parser')

    images = soup.find_all(('img'))

    for i,img in enumerate(images[:num_images+1]):
        img_url = img['src']

        if not img_url.startswith('http'):
            img_url = base_url + img_url

        response = requests.get(img_url)

        if i !=0:
            with open(f'C:\\image\\{query}_{i}.jpg','wb') as file:
                file.write(response.content)

download_images('김채원 고화질',10)