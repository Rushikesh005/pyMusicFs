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

    def fuzzy_match(self):
        temp_names = self.get_List()
        return process.extract(self.name,choices=temp_names,limit=1)
t = find_music(name='suits',type='tv')
print t.fuzzy_match()
