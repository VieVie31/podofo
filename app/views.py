from flask import Flask, render_template, request, redirect, url_for, abort, session
from werkzeug import secure_filename
from app import app
from time import time
from os import listdir, remove
from controllers import *

@app.route('/', methods=['GET'])
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
    # FIXME : this function is too long (in lines and speed) !! use a thread ?
    try:
	if len(listdir(app.config['PDF_DIR'])) > 50:
	    return "Too many pdf all ready uploaded..."

	uploaded_file = request.files['file']
	file_name = uploaded_file.filename

	if not file_name:
	    return "No file ?"

        file_name = str(int(time())) + "_" + secure_filename(file_name)
	pdf_path = app.config['PDF_DIR'] + file_name
	uploaded_file.save(pdf_path) #temporary save

	# check if the hash all ready exists in the db
        if pdf_allready_exists(file_name):
            #remove the pdf from the directory
            remove(pdf_path)
            return "This pdf allready exist in the database... <a href='/search'>search</a>."	

	# "File temporary uploaded... processing it before adding it to database...</br>"

	counter = None
	try:
            txt = read_as_txt(pdf_path)

    	    if not txt:
		remove(pdf_path)
		return "We cann't extract nothing from this pdf... <a href='/search'>search</a>."

	    counter = get_word_cout(txt)
	except:
	    remove(pdf_path)
	    return "This is not a pdf... <a href='/search'>search</a>." 

	pdf_id = insert_pdf_to_db(file_name) #add the pdf to the database 
        total_words = sum(counter.values())
	for word in counter: #update the words in database
	    insert_word_to_db(pdf_id, word, counter[word] / float(total_words))
	return "File {} successfully uploaded as  {}... <a href='/search'>search</a>.".format(uploaded_file.filename, str(pdf_id))
    except:
	return "Fail to upload"

