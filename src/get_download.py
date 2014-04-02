from urllib2 import urlopen
import sys
from requests import get
from requests import post
import time
from re import findall
from bs4 import BeautifulSoup as Soup
import pafy
class AudioHandler:
    def __init__(self):
        pass
    def download(self,raw_url,name):
        file_name = name
        url = raw_url.replace(' ','%20')
        u = urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)


            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            sys.stdout.write('\r'+status)
        f.close()

    def download_list(self,dwn_list):
        for url in dwn_list:
            self.download(url)

    def search_youtube_link(self,name):
        req = get("http://www.youtube.com/results?", params={"search_query": "%s" % (name)})
        soup = Soup(req.text)
        links = []
        #for body in soup.find_all('ol',{'id':"search-results"}):
        body=soup.find('ol',{'id':"search-results"})
        #for k in body.find_all('a'):
        k=body.a
        links.append(k.get('href'))
        return "https://www.youtube.com" + links[0]

    def getAudioStream(self,name):
        videoLink=self.search_youtube_link(name)
        video = pafy.new(videoLink)
        audiostreams = video.audiostreams
        for k in audiostreams:
            print(k.bitrate)
        return audiostreams[0].url,audiostreams[0].get_filesize()

    def get_download_link(self,name):
        youLink = self.search_youtube_link(name)
        for i in xrange(2):
            statusurl = None
            r = post("http://www.listentoyoutube.com/cc/conversioncloud.php", data={"mediaurl": youLink, "client_urlmap": "none"})
            try:
                statusurl = eval(r.text)['statusurl'].replace('\\/', '/') + "&json"
                break
            except:
                print eval(r.text)['error']
                time.sleep(1)
        while True:
            if not statusurl:
                raise Exception("")
            try:
                resp = eval(get(statusurl).text)
                if 'downloadurl' in resp:
                    downloadurl = resp['downloadurl'].replace('\\/', '/')
                    return downloadurl
                time.sleep(1)
            except Exception:
                pass
        return ""


#d = AudioHandler()
#print d.getAudioStream('Rubberband Man by The Spinners')
