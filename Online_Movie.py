import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from matplotlib import pyplot as plt

def Online_Movie_URL(result):
    Movie_URL = 'http://www.kobis.or.kr/kobis/business/stat/online/onlineFormerBoxRank.do?CSRFToken=q3HoRwzTjEZKPa1M_42ClV4KGamLtUf1uCSxS6tIuAI&loadEnd=0&searchType=search'    
    wd = webdriver.Chrome('C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python37_64/WebDriver/chromedriver.exe')
    wd.get(Movie_URL)
    time.sleep(1)

    rcv_data = wd.page_source
    soupData = BeautifulSoup(rcv_data, 'html.parser')    

    datalist = soupData.findAll('table', attrs = {'class': 'tbl_comm'})

    for tr in datalist:
        tr_tag = tr.findAll('tr')

        for td in tr_tag:
            if td is None:
                continue
            td_tag = td.findAll('td')
            
            a = list(td_tag)
            temp=[]
            for i,impo in enumerate(a):
                if i==2:                              #제목
                    impo_title=[]
                    atitle = str(impo).split('>')
                    btitle = str(atitle[3]).split('<')
                    impo_title.append(btitle[0])
                    print(impo_title,'\n')
                elif i==3:                            #개봉일
                    impo_release = list(impo)
                    print(impo_release,"\n")
                elif i==5:                            #장르
                    impo_genre = list(impo)
                    print(impo_genre,"\n")
                elif i==9:                            #누적관객수
                    #impo_audience = list(impo)
                    audience = str(impo).split('"')
                    impo_audience = audience[3]
                    impo_audience = str(impo_audience).replace(',','')
                    print(impo_audience,"\n")
                    
                    result.append(impo_title + impo_release + impo_genre + [impo_audience])
                    #print(result)
            
    return
    

def Online_Movie():

    result = []

    print('ONLINE MOVIE LANKING START')
    Online_Movie_URL(result)
    movie_table = pd.DataFrame(result, columns=('영화제목', '개봉일', '장르', '누적관객수'))
    movie_table.to_csv("./Online_Movie.csv", encoding="cp949", mode='w', index=True)

    print('FINISHED')


def Analysis():  #분석
    genre = ['애니메이션', '범죄', '판타지', '코미디', '액션', '미스터리', 
             '사극', '드라마', '스릴러', '멜로/로맨스', '어드벤처', 'SF', '공포(호러)', '다큐멘터리']

    sub_genre = ['Animation', 'Crime', 'Fantasy', 'Comedy', 'Action', 'Mystery',
                 'Historical', 'Drama', 'Thriller', 'Romance', 'Adventure', 'SF', 'Horror', 'Documentary']

    counting = []
    genre_counting = []
    
    for i in range(14):
        counting.append(0)
    print(counting)
    f = open('D:/데이터 크롤링/정인엽 크롤링/기말프로젝트/Online_Movie.csv', 'r', encoding = 'cp949')
    line = f.readline() #csv파일 맨 위 카태고리 줄 생략
    for j in range(300):
        line = f.readline().split(',')
        for i in range(len(genre)):
            if line[3]==genre[i]:
                #print(line[4])
                #print(type(line[4]))
                counting[i]=counting[i]+int(line[4])
    f.close()


    
    f = open('D:/데이터 크롤링/정인엽 크롤링/기말프로젝트/result_data.csv','w',encoding='cp949')
    for i in range(len(genre)):
        f.write(genre[i]+','+ str(counting[i])+'\n')
    f.close()
    plt.ylim(1000000,420000000)
    plt.bar(sub_genre,counting,color='blue')
    plt.show()

if __name__ == '__main__':
     Online_Movie()
     Analysis()
