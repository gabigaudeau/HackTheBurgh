import os
from faces import roast
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates")

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('roast_me.html')

@app.route('/uploads', methods=['POST'])
def upload_file():
    file = request.files['image']
    file.save(secure_filename(file.filename))
    image_path = os.path.join(app.instance_path[0:-8], file.filename)
    poem = roast(image_path)
    return render_template('result.html', value=poem)
app.run(debug=True)
