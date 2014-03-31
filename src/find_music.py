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

    def get_OriginalName(self):
        return self.__fuzzy_match__()

t = find_music(name='breakingBAD',type='tv')
print t.get_OriginalName()
print t.get_seasons()
