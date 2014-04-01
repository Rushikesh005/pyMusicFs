from  requests import request
from fuzzywuzzy import process
from bs4 import BeautifulSoup as Soup
from re import findall
from re import split as Split
import logging
import requests
class find_music():
    names = []
    site_url = "http://www.tunefind.com"

    original_name = ""
    use_name = ""
    episodes_dict = {}
    def __init__(self,name,type):
        self.url = "http://www.tunefind.com/browse/"
        self.s = requests.session()
        self.p = self.s.get(self.site_url)
        self.tname = name.replace(" ","-")
        self.name=name
        self.type = type
        self.__fuzzy_match__()

    def get_List(self):
        if self.type == "tv":
            url = self.url + self.type
        elif self.type == "movie":
            url = self.url + self.type
        else:
            return []
        req = self.s.get(url)
        soap = Soup(req.text)
        self.names = []
        for body in soap.findAll('div',{"class":"col-md-4"}):
            self.names.append(body.find('a').string.encode('ascii','ignore'))
        return self.names

    def __fuzzy_match__(self):
        temp_names = self.get_List()
        self.original_name =  process.extract(self.name,choices=temp_names,limit=1)[0][0]

    def get_seasons(self):
        self.use_name = self.original_name.replace(' ','-').lower()

        url = "http://www.tunefind.com/show/" + self.use_name
#        url = "http://www.tunefind.com/show/suits"
        req = self.s.get(url)
        seasons=[]
        soap = Soup(req.text)
#        print req.text
        for body in soap.find_all('div',{"class":"panel panel-default tf-panel"}):
            for names in  body.find_all('a'):
                seasons.append(names.string.encode('ascii','ignore'))

        return seasons

    def __get_episodes_dict(self,season_name):
        season_name = season_name.replace(' ','-').lower()
        url = "http://www.tunefind.com/show/"+self.get_OriginalName().lower().replace(" ","-")+"/" + season_name
        req = self.s.get(url)
        episodes = {}

        soap = Soup(req.text)
        for body in soap.find_all('ul',{'class':"list-group"}):
            for episode_body in body.find_all('li',{'class':'list-group-item'}):
                episodes[episode_body.find('a').string.encode('ascii','ignore').replace('\n','').strip(' ')] = episode_body.find('a').get('href')
        self.episodes_dict = episodes
        return episodes

    def get_episodes(self,season_name):
        return self.__get_episodes_dict(season_name).keys()

    def getMusicdict(self,season_name,episode_name):
        url = self.site_url + self.episodes_dict[episode_name]
        req = request('GET',url)
        soap = Soup(req.text)
        episodes = []
        for body in soap.find_all('div',{'class':"media-body"}):
            for k in body.find_all('a',{'class':"tf-popup tf-song-link"}):
                temp  = Split(r'\s{2}',body.getText().encode('ascii','ignore').replace('\n','').lstrip(' '))
                episode_str = ''
                cnt = 0
                for l in temp:
                    if l != '':
                        episode_str = episode_str + " " + l
                        cnt = cnt + 1
                    if cnt > 1:
                        break
                episodes.append(episode_str.lstrip(" "))
        return episodes


    def get_OriginalName(self):
        return self.original_name


'''logging.basicConfig(filename="log1.txt",level=logging.DEBUG,filemode="w")
t = find_music(name='howImetyourmother',type='tv')
print t.get_OriginalName()
print t.get_seasons()
p1 =  t.get_episodes('Season 8')
print p1
print t.getMusicdict(season_name='Season 3',episode_name='1. Farhampton')
'''
