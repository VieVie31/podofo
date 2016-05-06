from flask import Flask, render_template, request, redirect, url_for, abort, session
from werkzeug import secure_filename
from app import app
from time import time
from os import listdir, remove
from controllers import *

@app.route('/')
@app.route('/index')
def index_page():
    return "YO ! :D"

@app.route('/search', methods=['GET'])
def search_page():
    query = request.args.get('s')
    if not query:
        return render_template('search.html')
    return "Here will be the search results for {}".format(query)

@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def uploaded_page():
    try:
	if len(listdir(app.config['PDF_DIR'])) > 50:
	    return "Too many pdf all ready uploaded..."
	uploaded_file = request.files['file']
	file_name = uploaded_file.filename
	if file_name: #TODO : add more contidions (size, type, allready upld, etc)
            file_name = str(int(time())) + "_" + secure_filename(file_name)
	    uploaded_file.save(app.config['PDF_DIR'] + file_name) #temporary save
	    # TODO : processing on the file ...
	    if pdf_allready_exists(file_name):
		#remove the pdf from the directory
		remove(app.config['PDF_DIR'] + file_name)
		return "This pdf allready exist in the database..."
	    insert_pdf_to_db(file_name) #add the pdf to the database
	    # TODO : update all the words frequencies ...
	    return "File {} successfully uploaded... <a href='/search'>search</a>.".format(uploaded_file.filename)
    except:
	return "Fail to upload"

