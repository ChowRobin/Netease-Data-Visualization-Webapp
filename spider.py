import requests
from bs4 import BeautifulSoup
from urllib import parse
from time import sleep
import json
from selenium import webdriver
import re
from urllib import parse
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import pickle
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba

class Spider:

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def crawl(self, username):
        username = parse.quote(username)
        userurl = 'https://music.163.com/#/search/m/?s=' + username + '&type=1002'
        self.driver.get(userurl)
        sleep(2)
        self.driver.switch_to_frame('contentFrame')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        usertxt = soup.find('table', class_='m-table m-table-2 m-table-2-cover').find('tr').find('td').find('div').find('a').get('href')
        userid = re.findall(r'\d+', usertxt)[0]
        print('userid is ', userid)
        url = 'https://music.163.com/#/user/songs/rank?id=' + userid
        
        driver.get(url)
        sleep(2)
        driver.switch_to_frame('contentFrame')
        # sleep(3)
        data1 = driver.page_source

        driver.get(url)
        sleep(2)
        driver.find_element_by_id('songsall').click()
        driver.switch_to_frame('contentFrame')
        data2 = driver.page_source

        driver.close()
        self.parse(data1, 'week')
        self.parse(data2, 'all')

    def parse(self, data, pre)
        soup = BeautifulSoup( 'html.parser')
        
        lis = soup.find('div', class_='m-record').find_all('li')

        songs = []

        rank = 0

        for li in lis:
            rank += 1
            song = {}
            hddiv = li.find('div', class_='hd ')
            songdiv = li.find('div', class_='song')
            topsdiv = li.find('div', class_='tops')
            song['rank'] = rank
            song['name'] = songdiv.find('div', class_='tt').find('span', class_='txt').find('a').text
            tmp = songdiv.find('div', class_='tt').find('span', class_='txt').find('span').find('span').get('title').split('/')
            # song['singer'] = [t.replace(' ', '-') for t in tmp]
            song['singer'] = tmp
            width = topsdiv.find('span').get('style')
            song['width'] = re.findall(r'\d+', width)[0]
            # print(song)
            songs.append(song)

        singers = {}
        singerslist = []

        for song in songs:
            names = song.get('singer')
            for name in names:
                try:
                    count = singers.get(name)
                    singers[name] = count+1
                except:
                    singers[name] = 1

    def save_wordcloud(self, dic, filename):
        wc = WordCloud(background_color='white', 
                        font_path="./static/font/simsun.ttf")
        wc.generate_from_frequencies(dic)
        plt.imshow(wc)
        plt.axis("off")
        # plt.show()
        filename = './static/img/' + filename
        Plt.savefig(filename)
