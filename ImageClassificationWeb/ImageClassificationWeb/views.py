"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from ImageClassificationWeb import app
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import requests
import json
import io
import os
from PIL import Image
import base64


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
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
            img = Image.open(file)
            output = io.BytesIO()
            img.save(output, 'PNG')
            imgbytes = output.getvalue()
            output.seek(0)
            contents = base64.b64encode(output.read()).decode('ascii')
            output.close()
            headers = {'Content-Type':'application/json'}

            resp = requests.post('http://bb6c6343-69f5-4e8e-a8b0-6b8b22533fdb.eastus.azurecontainer.io/score',data=imgbytes, headers=headers, timeout=300)

            label = json.loads(resp.json())['dog_breed']

            return render_template('uploaded_file.html', filename=file.filename, contents=contents, label=label)

    return '''
    <!doctype html>
    <title>Upload Image</title>
    <h1>Upload an Image to Classify</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
