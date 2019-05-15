import os
from pathlib import Path
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename 
from whichpet.model_inference import Result, init_model, do_inference
from whichpet.upload import UploadResult, do_file_upload
from whichpet.page_info import PageInfo

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # root directory of application
    root_path = Path(__file__).parent

    # set config from file
    app.config.from_pyfile('config_penguin.py')

    # initialise the model
    model_path = root_path.joinpath(app.config['STATIC_PREFIX_PATH'], app.config['MODEL_FOLDER'])
    learn = init_model(model_path)

    # initialise upload path
    upload_path = root_path.joinpath(app.config['STATIC_PREFIX_PATH'], app.config['IMAGES_FOLDER'], app.config['UPLOAD_FOLDER'])

    # image src path for template (starting from /static/...)
    test_image_path = os.path.join(app.config['STATIC_PREFIX_PATH'], app.config['IMAGES_FOLDER'], app.config['UPLOAD_FOLDER'])

    # sample image src path for template (starting from /static/...)
    sample_image_path = os.path.join(app.config['STATIC_PREFIX_PATH'], app.config['IMAGES_FOLDER'], app.config['SAMPLE_FOLDER'])

    page_info = PageInfo(app.config['TITLE'], app.config['HEADING'], app.config['INTRODUCTION'], 
        app.config['UPLOAD_INSTRUCTION'], test_image_path, sample_image_path)

    # Home page and starting point
    @app.route('/')
    def index():
        return render_template('index.html', page_info=page_info)

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
        return render_template('result.html', result=result, page_info=page_info)

    return app
    