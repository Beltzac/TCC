#!flask/bin/python
import os
from oct2py import octave
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

THIS_FOLDER = os.getcwd()
octave.addpath(THIS_FOLDER + '/octave')
UPLOAD_FOLDER = THIS_FOLDER + '/upload'
OUTPUT_FOLDER = THIS_FOLDER + '/output'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload/<path:filename>')
def send_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/output/<path:filename>')
def send_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_path)
            texto , tempo = octave.runOCR(full_path)
            json = jsonify({'text' : texto.tolist(),
                            'time' : tempo})             
            return json #redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload nova imagem</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug = True)
	