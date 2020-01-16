import os
import uuid
import requests
import style_transfer
from flask import Flask, Response, flash, request, redirect, url_for, jsonify, abort
from werkzeug.utils import secure_filename

CONFIGS = {
    'IMAGE_FOLDER': './images',
    'MODEL_FOLDER': './style_models',
    'RESULT_FOLDER': './results',
}

app = Flask(__name__)
    
for var, path in CONFIGS.items():
    if not os.path.exists(path):
        os.mkdir(path)
    app.config[var] = path

def get_available_gpu():
    url = 'http://127.0.0.1:2048/allocate_gpu'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return int(r.content)
        else:
            return None
    except:
        return None

def perform_transfer(image_path, model_path, result_path, gpu_id):
    config = style_transfer.Config()
    config.content_image = image_path
    config.model = model_path
    config.output_image = result_path
    config.device_id = gpu_id
    style_transfer.stylize(config)
    return open(result_path, 'rb')


@app.route('/submit', methods=['POST'])
def submit_task():
    if request.method == 'POST':
        image = request.files['image']
        model = request.files['model']
        image_mime = 'image/' + image.filename.rsplit('.', 1)[-1]
        image_path = os.path.join(app.config['IMAGE_FOLDER'], image.filename)
        model_path = os.path.join(app.config['MODEL_FOLDER'], model.filename)
        result_path = os.path.join(app.config['RESULT_FOLDER'], image.filename)
        image.save(image_path)
        model.save(model_path)
        gpu_id = get_available_gpu()
        if gpu_id is None:
            abort(408)
            
        try:
            result = perform_transfer(image_path, model_path, result_path, gpu_id)
        except:
            abort(413)

    return Response(result, mimetype=image_mime)


def perform_training(image_path, model_path, gpu_id):
    config = style_transfer.Config()
    config.style_image = image_path
    config.save_model_path = model_path
    config.device_id = gpu_id
    style_transfer.train(config)
    return open(model_path, 'rb')


@app.route('/custom', methods=['POST'])
def custom_task():
    if request.method == 'POST':
        image = request.files['image']
        
        image_path = os.path.join(app.config['IMAGE_FOLDER'], image.filename)
        model_path = os.path.join(app.config['MODEL_FOLDER'], image.filename)
        image.save(image_path)

        return model_path, 200
    
        gpu_id = get_available_gpu()
        if gpu_id is None:
            abort(408)
            
        try:
            result = perform_training(image_path, model_path, gpu_id)
        except:
            abort(413)

    return Response(result)


@app.route('/')
def hellow():
    return "hellow"
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666, threaded=True)
