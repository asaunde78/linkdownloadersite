from flask import Flask, current_app
# from PIL import Image


class downloader():
    def __init__(self):
        self.app = Flask(__name__)
        # img = Image.open(f'small.png')
        # @app.route('/')
        with open("links.txt", "w") as r:
            r.write("")
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def index(path):
            # print(path)
            url = path#.split("?")[0]
            with open("links.txt", "a") as r:
                r.write(url+"\n")
            return current_app.send_static_file("small.png")
            # return render_template("index.html",name=path)
    def run(self):
        self.app.run(port=6969,debug=False)

if __name__ == '__main__':
    # app.run(port=6969,debug=True)
    a = downloader()
    a.run(port =6969)
