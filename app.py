import os
from roaster import roastMe
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import json;

app = Flask(__name__, template_folder="templates",static_url_path='/static')

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/roast_me/')
def roast_me():
    return render_template('roast_me.html')

@app.route('/result/')
def result():
    return render_template('result.html')

@app.route('/hall_of_flame/')
def hall_of_flame():
    return render_template('hall_of_flame.html')




@app.route('/uploads', methods=['POST'])
def upload_file():
    file = request.files['image']
    file.save(secure_filename(file.filename))
    image_path = os.path.join(app.instance_path[0:-8], file.filename)
    roast = roastMe(image_path,'data/database')
    return render_template('result.html', value=roast)
if __name__ =='__main__':
    app.run(threaded=True, port=5000,debug=True)
