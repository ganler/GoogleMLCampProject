import os
import uuid
import requests
from PIL import Image
from flask_cors import CORS
from flask import Flask, Response, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

CONFIGS = {
    'IMAGE_FOLDER': './images',
    'MODEL_FOLDER': './style_models',
    'SAMPLE_FOLDER': './style_samples',
    'RESULT_FOLDER': './results',
}

app = Flask(__name__)
app.config['RESEND_TIMES'] = 3
app.config['GPU_SERVERS'] = (
    #('xxx.xxx.xxx.xxx:6666', 3), Please fill in your GPU servers address here
)
for var, path in CONFIGS.items():
    if not os.path.exists(path):
        os.mkdir(path)
    app.config[var] = path

##########################################
def listdir(rootdir):
    all_file = os.listdir(rootdir)
    files_path = []
    for i in range(0,len(all_file)):
        files_path.append(os.path.join(rootdir, all_file[i]))
    return files_path

@app.route('/style_list', methods=['GET'])
def style_list():
    samples_path = listdir(app.config['SAMPLE_FOLDER'])
    models_path  = listdir(app.config['MODEL_FOLDER'])
    all_samples = set([os.path.split(file)[-1].split('.')[0] for file in samples_path])
    all_models = set([os.path.split(file)[-1].split('.')[0] for file in models_path])
    available_styles = all_samples.intersection(all_models)

    style_list = {}
    for sample_path in samples_path:
        img = Image.open(sample_path) 
        sample_name = os.path.split(sample_path)[-1].split('.')[0]
        if sample_name in available_styles:
            style_list[sample_name] = (sample_path[1:], img.size)

    return jsonify(style_list)
##########################################


##########################################
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/custom', methods=['POST'])
def custom():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        image = request.files['file']
        image_name = image.filename
        
        if image_name == '':
            flash('No selected file')
            return redirect(request.url)
        if image and allowed_file(image_name):
            image_name = secure_filename(image_name)
            prefix, suffix = image_name.rsplit('.', 1)
            image_name = prefix + '_' + str(uuid.uuid4()) + '.' + suffix
            image.save(os.path.join(app.config['IMAGE_FOLDER'], image_name))
            status_code = post_custom(image_name)
            return os.path.join(app.config['RESULT_FOLDER'][1:], image_name), status_code
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/submit', methods=['POST'])
def listen():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        image = request.files['file']
        image_name = image.filename
        style_name = request.form['name'] + '.pth'
        
        if image_name == '':
            flash('No selected file')
            return redirect(request.url)
        if image and allowed_file(image_name):
            image_name = secure_filename(image_name)
            prefix, suffix = image_name.rsplit('.', 1)
            image_name = prefix + '_' + str(uuid.uuid4()) + '.' + suffix
            image.save(os.path.join(app.config['IMAGE_FOLDER'], image_name))
            status_code = post_task(image_name, style_name)
            return os.path.join(app.config['RESULT_FOLDER'][1:], image_name), status_code
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/results/<filename>')
def post_result(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename=filename)

@app.route('/style_samples/<filename>')
def post_sample(filename):
    return send_from_directory(app.config['SAMPLE_FOLDER'], filename=filename)

def post_custom(image_name):
    import random
    
    for i in range(app.config['RESEND_TIMES']):
        addr = random.choice(sum([[addr] * cnt for addr, cnt in app.config['GPU_SERVERS']], []))
        url = 'http://' + addr + '/custom'
        files = {
            'image': open(os.path.join(app.config['IMAGE_FOLDER'], image_name), 'rb'),
        }

        try:
            r = requests.post(url, files=files)

            if r.status_code != 408:
                return r.status_code
        except:
            continue
        
    return 408 


def post_task(image_name, style_name):
    import random
    
    for i in range(app.config['RESEND_TIMES']):
        addr = random.choice(sum([[addr] * cnt for addr, cnt in app.config['GPU_SERVERS']], []))
        url = 'http://' + addr + '/submit'
        files = {
            'image': open(os.path.join(app.config['IMAGE_FOLDER'], image_name), 'rb'),
            'model': open(os.path.join(app.config['MODEL_FOLDER'], style_name), 'rb'),
        }

        try:
            r = requests.post(url, files=files)

            if r.status_code == 200:
                result_path = os.path.join(app.config['RESULT_FOLDER'], image_name)
                with open(result_path, 'wb') as f:
                    f.write(r.content)

            if r.status_code != 408:
                return r.status_code
        except:
            continue
        
    return 408 
##########################################

@app.route('/')
def main():
    return "Welcome, this is Magic Filters!"

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(host='0.0.0.0', port=2333, threaded=True)
