from flask import Flask,render_template,request,send_file
from flask_cors import CORS
import base64
import cv2
import  random

app=Flask(__name__)

CORS(app)

@app.route('/')
def homepage():

    return '<h1> Server Started </h1>'




@app.route('/gui')
def gui():
    return render_template('gui.html')




@app.route('/analyse/', methods=['GET', 'POST'])
def analayse():
    if (request.method == 'POST'):
        isthisFile = request.files.get('file')
        print(isthisFile.filename)
        isthisFile.save("./" + isthisFile.filename)
        a, b, c, d, x = getdata(isthisFile.filename)
        return {'a': a, 'b': b, 'c': c, 'd': d, 'x': x}


def getdata(x):

    img = cv2.imread(x)
    img=cv2.resize(img,(400,300))
    k=random.randint(0,100)

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    blur=cv2.GaussianBlur(gray,(11,11),0)
    canny=cv2.Canny(gray,200,200)

    fg=str(k)+'g.jpg'
    fh=str(k)+'h.jpg'
    fb=str(k)+'b.jpg'
    fc=str(k)+'c.jpg'

    cv2.imwrite(fg,gray)
    cv2.imwrite(fh,hsv)
    cv2.imwrite(fb,blur)
    cv2.imwrite(fc,canny)

    with open(fg, "rb") as image_file:
            a = base64.b64encode(image_file.read())

    with open(fh, "rb") as image_file:
        b = base64.b64encode(image_file.read())

    with open(fb, "rb") as image_file:
        c = base64.b64encode(image_file.read())

    with open(fc, "rb") as image_file:
        d = base64.b64encode(image_file.read())

    with open(x, "rb") as image_file:
        w = base64.b64encode(image_file.read())

    return (a.decode('utf-8'),b.decode('utf-8'),c.decode('utf-8'),d.decode('utf-8'),w.decode('utf-8'))


if __name__ == '__main__':
    app.run(debug=True)