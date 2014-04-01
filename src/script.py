import os,sys
import subprocess
import get_download
x=get_download.get_download()
link,size=x.donwload_by_name(sys.argv[1].split("/")[-1])
subprocess.call(["vlc",str(link)])
