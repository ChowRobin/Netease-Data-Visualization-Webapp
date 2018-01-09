import requests
from bs4 import BeautifulSoup
from urllib import parse
from time import sleep
import os
from selenium import webdriver
import re
from urllib import parse
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pandas import DataFrame
import pandas as pd
import pickle
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
font = fm.FontProperties(fname="./static/font/simsun.ttf", size=14)


class Spider:

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def crawl(self, username):
        driver = self.driver
        username = parse.quote(username)
        userurl = 'https://music.163.com/#/search/m/?s=' + username + '&type=1002'
        driver.get(userurl)
        sleep(2)
        driver.switch_to_frame('contentFrame')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        userlist = soup.find('table', class_='m-table m-table-2 m-table-2-cover').find_all('tr')
        usertxt = userlist[0].find('td').find('div').find('a').get('href')
        for user_tr in userlist:
            _name = user_tr.find('td').find('div').find('a').find('span').get('title')
            if _name == username:
                usertxt = user_tr.find('td').find('div').find('a').get('href')
                break
        userid = re.findall(r'\d+', usertxt)[0]
        print('userid is ', userid)
        url = 'https://music.163.com/#/user/songs/rank?id=' + userid
        
        driver.get(url)
        sleep(1.5)
        driver.switch_to_frame('contentFrame')
        sleep(0.8)
        data1 = driver.page_source

        driver.find_element_by_id('songsall').click()
        sleep(2)
        data2 = driver.page_source

        driver.close()
        self.parse(data1, 'week')
        self.parse(data2, 'all')

    def parse(self, data, pre):
        print('==>', pre)
        soup = BeautifulSoup(data, 'html.parser')
        
        lis = soup.find('div', class_='m-record').find_all('li')

        songs = []

        rank = 0

        for li in lis:
            rank += 1
            song = {}
            topsdiv = li.find('div', class_='tops')
            hddiv = li.find('div', class_='hd ')
            songdiv = li.find('div', class_='song')
            song['rank'] = rank
            song['name'] = songdiv.find('div', class_='tt').find('span', class_='txt').find('a').text
            tmp = songdiv.find('div', class_='tt').find('span', class_='txt').find('span').find('span').get('title').split('/')
            # song['singer'] = [t.replace(' ', '-') for t in tmp]
            song['singer'] = tmp
            width = topsdiv.find('span').get('style')
            song['width'] = int(re.findall(r'\d+', width)[0])
            # print(song)
            songs.append(song)

        singers = {}
        _songs = {}
        singerslist = []

        for song in songs:
            _name = song.get('name')
            _songs[_name] = song.get('width')
            names = song.get('singer')
            for name in names:
                try:
                    count = singers.get(name)
                    singers[name] = count+1
                except:
                    singers[name] = 1

        filename = pre + '_singers_wordcloud.png'
        self.save_wordcloud(singers, filename)

        filename = pre + '_singers.png'
        self.save_barchart(self.get_most(singers, 10), filename)

        filename = pre + '_songs.png'
        self.save_barchart(self.get_most(_songs, 10), filename)

        filename = pre + '_singers_pie.png'
        self.save_pie(self.get_most(singers,10), filename)

    def get_most(self, dic, num):
        y = sorted(tuple(dic.items()), key=lambda x:x[1])
        if len(y) > num:
            y = y[:-num:-1]
        # print(y)
        return dict(y)

    def save_wordcloud(self, dic, filename):
        plt.clf()
        wc = WordCloud(background_color='white', 
                        font_path="./static/font/simsun.ttf")
        wc.generate_from_frequencies(dic)
        plt.imshow(wc)
        plt.axis("off")
        filename = './static/img/' + filename
        plt.savefig(filename)

    def save_barchart(self, dic, filename):
        plt.clf()
        # print(dic)
        keys = list(dic.keys())
        values = list(dic.values())
        
        df = DataFrame({"score":values}, index=keys)
        ax = df.plot(kind = 'bar', rot = 30, figsize=(14,9)) 
        ax.set_xticklabels(df.index.values, fontproperties=font)
        filename = './static/img/' + filename
        plt.savefig(filename)
        
    def save_pie(self, dic, filename):
        plt.clf()
        plt.figure(figsize=(9,9))
        total = 0
        labels = dic.keys()
        sizes = dic.values()

        patches,l_text,p_text = plt.pie(sizes,labels=labels,labeldistance = 1.1,autopct = '%3.1f%%',shadow = False, startangle = 90, pctdistance = 0.6)
        for t in l_text:
            t.set_size=(30)
            t.set_fontproperties(font)
        for t in p_text:
            t.set_size=(20)
            t.set_fontproperties(font)
        plt.axis('equal')
        plt.legend(prop=font)
        filename = './static/img/' + filename
        plt.savefig(filename)
        
if __name__ == '__main__':
    spider = Spider()
    username = input('please input your username\n> ')
    spider.crawl(username)
