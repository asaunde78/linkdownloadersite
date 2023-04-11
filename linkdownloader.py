from flask import Flask, current_app
# from PIL import Image
import requests,re,os,shutil#,unicodedata

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class downloader():
    def __init__(self, folder="images"):
        self.app = Flask(__name__)
        # img = Image.open(f'small.png')
        # @app.route('/')
        self.folder = folder
        self.count = {}
        with open("links.txt", "w") as r:
            r.write("")
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def index(path):
            if(path.startswith("add")):
                vals = path[3:]
                vals = vals.split(",")
                self.count[vals[0]] = int(vals[1]) 
                print(f"[ADD] adding {vals[1]} @ id {vals[0]}")
                return current_app.send_static_file("good.png")
            if(path.startswith("kill")):
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
                # print(path)
                tabid = path[:path.index("http")]
                # print(tabid)
                if tabid in self.count:
                    print(f"[FOUND] id:{tabid}")
                    url = path[len(tabid):]#.split("?")[0]
                    
                    filename = "".join(url.split("/")[-2:])
                    if("?" in filename):
                        filename = filename.split("?")[0]
                    
                    with open("links.txt", "a") as r:
                        r.write(url + ":\t" + filename+"\n")
                    print(filename)
                    with requests.get(url, allow_redirects=True) as response, open(self.folder+"/" +filename, 'wb') as f:
                        #print(response.text)
                        print(response.status_code)
                        data = response.content
                        f.write(data)
                    self.count[tabid] -= 1
                    print(f"[WROTE] {url}, remaining: {self.count[tabid]}")
                    if(self.count[tabid]>1):
                        return current_app.send_static_file("good.png")
                    else:
                        print("sending done code!")
                        return current_app.send_static_file("done.png")
            return current_app.send_static_file("bad.png")
    def run(self):
        self.app.run(port=6969,debug=False)

if __name__ == '__main__':
    # app.run(port=6969,debug=True)
    a = downloader()
    a.run()
