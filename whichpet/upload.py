import os
import glob
from pathlib import Path
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename 

# Class to hold the result of the image file upload
class UploadResult:
  def __init__(self, file_path, success, error_message):
    self.file_path = file_path
    self.success = success
    self.error_message = error_message

# Check file extensions
def allowed_file(allowed_extensions, filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Clear down folder
def clear_images_folder(folder_path):
    test_path = folder_path.joinpath("*")
    files = glob.glob(str(test_path))
    for f in files:
        os.remove(f)

# File upload checks
def do_file_upload(request, upload_location, allowed_extensions):
    # First clear the images folder
    clear_images_folder(upload_location)
    # check if the post request has the file part
    if 'file' not in request.files:
        return UploadResult("", False, 'No file part')
    file = request.files['file']
    # check file has a filename
    if file.filename == '':
        return UploadResult("", False, 'No selected file')
    if file and allowed_file(allowed_extensions, file.filename):
        filename = secure_filename(file.filename)
        file_path = str(upload_location.joinpath(filename))
        file.save(file_path)
        return UploadResult(file_path, True, "")


        