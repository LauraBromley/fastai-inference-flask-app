import os
from pathlib import Path
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename 
from whichpet.model_inference import Result, init_model, do_inference
from whichpet.upload import UploadResult, do_file_upload

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # load the config (testing?)
    app.config.update(
        APP_NAME = 'whichpet',
        IMAGES_FOLDER = 'images',
        UPLOAD_FOLDER = 'test',
        SAMPLE_FOLDER = 'sample',
        MODEL_FOLDER = 'models',
        STATIC_PREFIX_PATH = 'static',
        ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg'],
    )

    # root directory of application
    root_path = Path(__file__).parent

    # initialise the model
    model_path = root_path.joinpath(app.config['STATIC_PREFIX_PATH'], app.config['MODEL_FOLDER'])
    learn = init_model(model_path)

    # initialise upload path
    upload_path = root_path.joinpath(app.config['STATIC_PREFIX_PATH'], app.config['IMAGES_FOLDER'], app.config['UPLOAD_FOLDER'])

    # image src path for template (starting from /static/...)
    test_image_path = os.path.join(app.config['STATIC_PREFIX_PATH'], app.config['IMAGES_FOLDER'], app.config['UPLOAD_FOLDER'])

    # sample image src path for template (starting from /static/...)
    sample_image_path = os.path.join(app.config['STATIC_PREFIX_PATH'], app.config['IMAGES_FOLDER'], app.config['SAMPLE_FOLDER'])

    # Home page and starting point
    @app.route('/')
    def index():
        return render_template('index.html')

    # POST method to upload a file
    @app.route('/upload', methods=['GET','POST'])
    def upload_file():
        if request.method == 'POST':
            upload_result = do_file_upload(request, upload_path, app.config['ALLOWED_IMAGE_FORMATS'])
            if upload_result.success:
                result = do_inference(learn, upload_result.file_path)
                return results(result)
            else:
                flash(upload_result.error_message)
                return redirect(request.url)
        
        return redirect(request.url)

    # Page that displays the results
    @app.route('/results')
    def results(result):
        return render_template('result.html', result=result, test_image_path=test_image_path, sample_image_path=sample_image_path)

    return app
    