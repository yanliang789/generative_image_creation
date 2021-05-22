from flask import Flask, flash, redirect, request, url_for, Response, render_template
# from flask_restful import reqparse, abort, Api, Resource
from werkzeug.utils import secure_filename
import pickle
import werkzeug
import os
import shutil
import time
import numpy as np
import subprocess
import main
# from model import NLPModel

UPLOAD_SAMPLE_FEMALE_FOLDER = 'assets/representative/celeba_hq/ref/female'
UPLOAD_SAMPLE_MALE_FOLDER = 'assets/representative/celeba_hq/ref/male'

UPLOAD_FEMALE_FOLDER = 'assets/representative/celeba_hq/src/female'
UPLOAD_MALE_FOLDER = 'assets/representative/celeba_hq/src/male'

TARGET_FILE = 'expr/results/celeba_hq/reference.jpg'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_SAMPLE_FEMALE_FOLDER'] = UPLOAD_SAMPLE_FEMALE_FOLDER
app.config['UPLOAD_SAMPLE_MALE_FOLDER'] = UPLOAD_SAMPLE_MALE_FOLDER
app.config['UPLOAD_FEMALE_FOLDER'] = UPLOAD_FEMALE_FOLDER
app.config['UPLOAD_MALE_FOLDER'] = UPLOAD_MALE_FOLDER

# api = Api(app)

# class UploadImage(Resource):
#        def post(self):
#            parse = reqparse.RequestParser()
#            parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
#            args = parse.parse_args()
#            image_file = args['file']
#            image_file.save("your_file_name.jpg")

# api.add_resource(HelloWorld, '/')
# api.add_resource(UploadImage, '/upload_sample')

#check if file in allowed list 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def hair_style():
    return render_template("home_page.html")


 # upload sample file          
@app.route('/add_sample', methods=['GET', 'POST'])
def add_sample():
    return upload_file('UPLOAD_SAMPLE_FEMALE_FOLDER', False)

# upload src file          
@app.route('/add_src', methods=['GET', 'POST'])
def add_src():
    return upload_file('UPLOAD_FEMALE_FOLDER', True)
    # run code to get image
    # return result

# process src file          
@app.route('/style', methods=['GET'])
def getStyle():
    # Remove existing result
    print("start get style")
    if(os.path.isfile(TARGET_FILE)):
       os.remove(TARGET_FILE)
       print("clean previous file")

    print("working on style")
    subprocess.Popen('python main.py --mode sample --num_domains 2 --num_workers 0 --resume_iter 100000 --w_hpf 1 \
               --checkpoint_dir expr/checkpoints/celeba_hq \
               --result_dir expr/results/celeba_hq/ \
               --src_dir assets/representative/celeba_hq/src \
               --ref_dir assets/representative/celeba_hq/ref', shell=True)

    while (not os.path.isfile(TARGET_FILE)):
        time.sleep(1)
        print("waiting 1 seconds")
        if(os.path.isfile(TARGET_FILE)):
            shutil.move("expr/results/celeba_hq/reference.jpg", "static/reference.jpg")
            return render_template("style_done.html")

def upload_file(folder, isSrc):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config[folder], filename))
            return render_template("upload_success.html")
    
    if isSrc:
       return render_template("add_src.html")
    else:
       return render_template("add_sample.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)