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
import matplotlib.font_manager as fm
import pickle
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba

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
        sleep(1)
        data1 = driver.page_source

        driver.find_element_by_id('songsall').click()
        sleep(1)
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

    def get_most(self, dic, num):
        y = sorted(tuple(dic.items()), key=lambda x:x[1])
        if len(y) > num:
            y = y[:-num:-1]
        print(y)
        return dict(y)

    def save_wordcloud(self, dic, filename):
        plt.clf()
        wc = WordCloud(background_color='white', 
                        font_path="./static/font/simsun.ttf")
        wc.generate_from_frequencies(dic)
        plt.imshow(wc)
        plt.axis("off")
        # plt.show()
        filename = './static/img/' + filename
        plt.savefig(filename)
        plt.close()

    def save_barchart(self, dic, filename):
        plt.clf()
        keys = dic.keys()
        values = dic.values()
        plt.bar(range(len(values)), values, facecolor='yellowgreen', edgecolor='white', tick_label=keys)
        # for x,y in zip(list(range(len(values))), values):
        #     plt.text(x+0.3, y+0.5, y, ha='center', va='bottom')
        filename = './static/img/' + filename
        plt.savefig(filename)
        plt.close()

if __name__ == '__main__':
    spider = Spider()
    username = input('please input your username\n> ')
    spider.crawl(username)
