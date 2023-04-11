from flask import Flask, current_app
# from PIL import Image
import requests,os,shutil

class downloader():
    def __init__(self, folder="images"):
        self.app = Flask(__name__)
        # img = Image.open(f'small.png')
        # @app.route('/')
        self.folder = folder
        
        with open("links.txt", "w") as r:
            r.write("")
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def index(path):
            # print(path)
            url = path#.split("?")[0]
            filename = url.split("/")[-1]
            if("?" in filename):
                filename = filename.split("?")[0]
            with open("links.txt", "a") as r:
                r.write(filename+"\n")
            # ftype = filename.split(".")[-1]
            with requests.get(url, allow_redirects=True) as response, open(self.folder+"/" +filename, 'wb') as f:
                #print(response.text)
                data = response.content
                f.write(data)
            return current_app.send_static_file("small.png")
            # return render_template("index.html",name=path)
    def run(self):
        self.app.run(port=6969,debug=False)

if __name__ == '__main__':
    # app.run(port=6969,debug=True)
    a = downloader()
    a.run(port =6969)
