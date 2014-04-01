#!/usr/bin/env python

#
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os, stat, errno, find_music
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG,filemode='w')
# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse
import seekDonwload
import urllib2
import io
hdr = {'User-Agent':'Mozilla/5.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
req=urllib2.Request("http://www.textfiles.com/100/ad.txt",headers=hdr)
u=urllib2.urlopen(req)

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)
import seekDonwload
hello_path = '/home/shreyas/prodrive_feb2/local/mta'
config = ["suits/all","breakingbad/Season 2","breakingbad/Season 3"]
table={}
for everyItem in config:
    series,season=everyItem.split("/")
    x=find_music.find_music(name=series,type='tv')
    series=x.get_OriginalName()
    if series not in table:
        table[series]=[season]
    else:
        table[series].append(season)

#dictionary=os.listdir(hello_path)
class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class HelloFS(Fuse):
    def getattr(self, path):
        print "path=",path
        st = MyStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        elif path.count("/")<=3:
           st.st_mode=stat.S_IFREG | 0755
           st.st_nlink = 2
           st.st_size=14227762
        elif path.count("/")==4:
            '''st.st_mode=stat.S_IFREG | 0755
            st.st_nlink = 2
            st.st_size=36845'''
            st=os.stat("/home/shreyas/Pictures/all-help.tec.txt")
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        if path=="/":
            self.dictionary=[i for i in table.keys()]
        elif path.count("/")==1:
            nameOfSeries=path.split("/")[-1]
            seriesObject=find_music.find_music(nameOfSeries,"tv")
            if table[nameOfSeries]==["all"]:
                self.dictionary=seriesObject.get_seasons()
            else:
                self.dictionary=[]
                validList=seriesObject.get_seasons()
                for currentSeason in table[nameOfSeries]:
                    if currentSeason in validList:
                        self.dictionary.append(currentSeason)
        elif path.count("/")==2:
            empty,nameOfSeries,currentSeason=path.split("/")
            seriesObject=find_music.find_music(nameOfSeries,"tv")
            self.dictionary=seriesObject.get_episodes(currentSeason)
        elif path.count("/")==3:
            empty,nameOfSeries,currentSeason,currentEpisode=path.split("/")
            seriesObject=find_music.find_music(nameOfSeries,"tv")
            self.dictionary=seriesObject.getMusicdict(currentSeason,currentEpisode)
        for r in ['.','..']+self.dictionary:
                yield fuse.Direntry(r)

    def open(self, path, flags):
        logging.info("open called")
        self.h = seekDonwload.HttpFile("http://srv60.listentoyoutube.com/download/4pSZb3BlnGRkr6yq3JmTtGpjoWhnaWxwmZXfhKKj3Jeih6iR1djXrZuV/")
        logging.info("open completed")

    def read(self, path, size, offset):
        logging.info("read called size,offset "+str(size)+" "+str(offset))
        self.h.seek(offset,whence=0)
        return self.h.read(size)
        #logging.info("read completed")

    def truncate(self,path,size):
        return 0

    def release(self,path,flags):
        x=""
        self.h=""
        return 0
def main():
    usage="""
Userspace hello example
""" + Fuse.fusage
    server = HelloFS(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')
    print table
    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
