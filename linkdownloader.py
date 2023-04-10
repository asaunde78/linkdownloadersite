from flask import Flask, send_file,render_template,current_app
# from PIL import Image


app = Flask(__name__)
# img = Image.open(f'small.png')
# @app.route('/')
with open("links.txt", "w") as r:
    r.write("")
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # print(path)
    url = path#.split("?")[0]
    with open("links.txt", "a") as r:
        r.write(url+"\n")
    return current_app.send_static_file("elaina.png")
    # return render_template("index.html",name=path)
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def get_image(path):
#     # Open the local image using PIL
    
#     # Return the image as a file
#     return send_file(path_or_file="elaina.png",mimetype='image/png')
#     # return render_template("index.html")

if __name__ == '__main__':
    # app.run(port=6969,debug=True)
    app.run(port=6969,debug=False)

#gunicorn -w 4 -b 127.0.0.1:4000 myproject:app
#gunicorn -w 4 -b 127.0.0.1:6969 sitepillow:app
