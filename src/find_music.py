from  requests import request
from fuzzywuzzy import process
from bs4 import BeautifulSoup as Soup
class find_music():
    names = []
    def __init__(self,name,type):
        self.url = "http://www.tunefind.com/browse/"
        self.name = name
        self.type = type

    def get_List(self):
        if self.type == "tv":
            url = self.url + self.type
        elif self.type == "movie":
            url = self.url + self.type
        else:
            return []
        req = request('GET',url)
        soap = Soup(req.text)
        self.names = []
        for body in soap.findAll('div',{"class":"col-md-4"}):
            self.names.append(body.find('a').string.encode('ascii','ignore'))
        return self.names

    def __fuzzy_match__(self):
        temp_names = self.get_List()
        return process.extract(self.name,choices=temp_names,limit=1)[0][0]

    def get_seasons(self):
        url = "http://www.tunefind.com/show/" + self.__fuzzy_match__()
#        url = "http://www.tunefind.com/show/suits"
        req = request('GET',url)
        seasons=[]
        soap = Soup(req.text)
#        print req.text
        for body in soap.find_all('div',{"class":"panel panel-default tf-panel"}):
            for names in  body.find_all('a'):
                seasons.append(names.string.encode('ascii','ignore'))
        return seasons

    def __get_episodes_dict(self,season_name):
        seasons = self.get_seasons()
        if season_name in seasons:
            season_name = season_name.replace(' ','-')
        else:
            return {}
        url = "http://www.tunefind.com/show/suits/" + season_name
        req = request('GET',url)
        episodes = {}

        soap = Soup(req.text)
        for body in soap.find_all('ul',{'class':"list-group"}):
            for episode_body in body.find_all('li',{'class':'list-group-item'}):
                episodes[episode_body.find('a').string.encode('ascii','ignore').replace('\n','').strip(' ')] = episode_body.find('a').get('href')
        return episodes

    def get_episodes(self,season_name):
        return self.__get_episodes_dict(season_name).keys()

    def get_OriginalName(self):
        return self.__fuzzy_match__()



t = find_music(name='breakingBAD',type='tv')
#print t.get_OriginalName()
#print t.get_seasons()
p1 =  t.get_episodes('Season 2')
print p1
#op =['4. Discovery', '5. Break Point', '13. Zane Vs. Zane', '16. War', '11. Blind-Sided', '9. Asterisk', '15. Normandy', '7. Sucker Punch', '3. Meet the New Boss', '10. High Noon', '2. The Choice', '8. Rewind', "14. He's Back", '12. Blood in the Water', '6. All In', '1. She Knows']
