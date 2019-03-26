import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import seg as s
import time

UPLOAD_FOLDER = './user inputs'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            destination = os.path.join(app.config['UPLOAD_FOLDER'],"1.jpg")
            file.save(destination)
    return render_template('hello.html')
    
@app.route('/my-link/')
def my_link():
    (wid,hei) = s.seg()
    time.sleep(5)

    return render_template('hello1.html', wid=wid, hei=hei)



if __name__ == '__main__':
   app.run(debug=True)
