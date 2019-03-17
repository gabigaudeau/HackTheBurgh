import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('roast_me.html')

@app.route('/uploads', methods=['POST'])
def upload_file():
    file = request.files['image']
    poem = "INPUT POEM"
    return render_template('result.html', value=poem)
app.run(debug=True)
