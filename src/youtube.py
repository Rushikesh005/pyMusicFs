import pafy
url = "https://www.youtube.com/watch?v=DKaBb2hZ06k"
video = pafy.new(url)

#best = video.getbestaudio()
#print(best.url)
#best.download(quiet=False)
audiostreams = video.audiostreams
for k in audiostreams:
    print(k.bitrate)
d = "http://r4---sn-tv0cgv5qc5oq-2o9e.googlevideo.com/videoplayback?clen=13534913"+ "&" + "source=youtube&key=yt5&itag=140&sparams=clen%2Cdur%2Cgir%2Cid%2Cip%2Cipbits%2Citag%2Clmt%2Cpcm2fr%2Csource%2Cupn%2Cexpire&ms=au&gir=yes&upn=D-0bvRcJXAw&ipbits=0&fexp=917000%2C937407%2C943403%2C932273%2C914070%2C916625%2C937417%2C913434%2C934022&expire=1396413637&mws=yes&sver=3&lmt=1386673703641095&signature=6E31D82287BA544D5D85426200CC642B539453C4.71786DB9D752D652806666DC750EB4B20CD70D4A&id=o-AHDMMe5-MKh43rkh8TkAWNoaLMpcIGk-45Mr7404caSq&dur=852.172&mt=1396390781&mv=m&ip=123.201.194.121&pcm2fr=yes&ratebypass=yes"
import subprocess
subprocess.Popen("vlc %s"%d,shell=True)