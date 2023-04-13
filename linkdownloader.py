from flask import Flask, current_app
# from PIL import Image
import requests,re,os,shutil#,unicodedata
from urllib.request import urlretrieve

import concurrent.futures
import threading 

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class downloader():
    lock = threading.Lock()
    def __init__(self, folder="images",fixname=False):
        self.app = Flask(__name__)
        # img = Image.open(f'small.png')
        # @app.route('/')
        self.folder = folder
        self.count = {}
        with open("links.txt", "w") as r:
            r.write("")
        self.setup_routes()
        self.fixname=fixname
        self.links = []
        self.futures =[]

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.total=0

    def download(self,link,tabid):
        if(self.total) <= 0:
            return
        try:
            response = requests.get(link,timeout=1,allow_redirects=True)
            # print(f"CODE: {response.status_code}")
            if(not response.status_code == 200):
                raise Exception("Wrong status code.")
        except Exception as e:
            print(f"[FAILURE] Downloading failed as:",e)
            return
        
        # print(f"Grabbing lock: {self.lock.acquire()}")
        # print(self.lock.locked())
        # with self.lock:
        with self.lock:
            if(self.total) > 0:
                print(f"[DOWNLOADING] {link} NOW")
                filename = f"total{self.total}_" + "".join(link.split("/")[-2:])
                if("?" in filename):
                    filename = filename.split("?")[0]
                if(not "." in filename ):
                    filename += ".jpeg"
                if(filename.count(".")>1):
                    print(f"[WARNING] has too many dots {filename}")
                    filename = filename.replace(".",'')
                    filename += ".jpeg"
                if(self.fixname):
                    ending = filename.split(".")[1]
                    # filename = f"image({self.total}{tabid}{self.count[tabid]}).{ending}"
                    filename = f"image({len(self.links)}).{ending}"
                with open("links.txt", "a") as r:
                    r.write(link + ":\t" + filename+"\n")
                with open(self.folder+"/" +filename, 'wb') as f:
                    #print(response.text)
                    # print(response.status_code)
                    data = response.content
                    # print(data)
                    f.write(data)
                #     
                # urlretrieve(link, self.folder+"/"+filename)
                print(f"[{tabid}-WROTE] {link[:15]}  \n\ttabremaining: {self.count[tabid]} \n\ttotal remaining: {self.total}")
                self.count[tabid] -= 1
                self.total -= 1
                self.links.append(link)
                print(f"[DONE] DOWNLOADING {filename}")
        return
    
    
    def add(self,link,tabid):
        # self.todownload.append(link)
        if(self.total==0):
            return
        # print(f"[DOWNLOAD] adding {link} now")
        # self.futures.append(self.executor.submit(self.download,link, tabid))
        # print(concurrent.futures.as_completed(self.futures))
        self.executor.submit(self.download,link, tabid)
        
        
        
    def setup_routes(self):
        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def index(path):
            if(path.startswith("add")):
                vals = path[3:]
                vals = vals.split(",")
                self.count[vals[0]] = int(vals[1]) 
                
                print(f"[ADD] adding {vals[1]} @ id {vals[0]}")
                if self.total == None:
                    self.total = int(vals[1])
                else:
                    self.total += int(vals[1])
                return current_app.send_static_file("good.png")
            if(path.startswith("kill")):
                self.total= None
                self.links = []
                self.count = {}
                self.futures = []
                self.working = True
                print("clearing!")
                for filename in os.listdir(self.folder):
                    file_path = os.path.join(self.folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                return current_app.send_static_file("good.png")
            if("http" in path):
                if self.total == 0:
                    self.count = {}
                    print(f"unique pictures downloaded: {len(list(set(self.links)))}")
                    self.working = False
                    return current_app.send_static_file("done.png")
                # print(path)
                tabid = path[:path.index("http")]
                url = path[len(tabid):]#.split("?")[0]
                if url in self.links:
                    print("sending continue: link was already grabbed")
                    return current_app.send_static_file("good.png")
                # print(tabid)
                # print(self.count)
                if tabid in self.count:
                    # print(f"[FOUND] id:{tabid}")
                    if(self.count[tabid] > 0):
                        #DOWNLOAD FILE HERE
                        # print(f"[DOWNLOAD] adding {url} now")
                        self.add(url,tabid)
                        pass
                    if self.total < 0:
                        self.total = 0
                    if self.total == 0:
                        self.count = {}
                        # print(f"unique pictures downloaded: {len(list(set(self.links)))}")
                        return current_app.send_static_file("done.png")
                    if(self.count[tabid]>0):
                        # print("sending continue: link was good")
                        return current_app.send_static_file("good.png")
                    else:
                        # print(f"sending done code! removing {tabid}")

                        # self.count[tabid] = -1
                        del self.count[tabid]
                        print(f"Count after deleting the id: {self.count}")
                        return current_app.send_static_file("done.png")
            print("sending bad")
            return current_app.send_static_file("bad.png")
    def run(self):
        self.app.run(port=6969,debug=False)

if __name__ == '__main__':
    # app.run(port=6969,debug=True)
    a = downloader()
    a.run()
#gunicorn downloader:app -w 4 -b 127.0.0.1:8000
