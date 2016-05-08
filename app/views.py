from flask import Flask, render_template, request, redirect, url_for, abort, session, send_from_directory, send_file
from werkzeug import secure_filename
from app import app
from time import time
from os import listdir, remove, getcwd
from controllers import *

import io
import random
import unicodedata

@app.route('/', methods=['GET'])
@app.route('/search', methods=['GET'])
def search_page():
    query = request.args.get('s')
    page  = request.args.get('p')

    if not query:
        return render_template('search.html', count_pdf=count_pdf())

    try:
	page = int(page)
    except:
        page = 0

    query = query.lower()
    query = unicodedata.normalize('NFKD', query).encode('ASCII', 'ignore')
    words = query.split()[:5] #max 5 words for querying...
    words = map(secure_filename, words)
    query = " ".join(words)

    if not words:
        return render_template('search.html')

    rows, speed, next_button = get_results(words, page)

    return render_template('results.html', user_request=query, rows=rows, speed=speed) #"Here will be the search results for {}".format(query)

@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def uploaded_page():
    # FIXME : this function is too long (in lines and speed) !! use a thread ?
    try:
	if len(listdir(app.config['PDF_DIR'])) > 200:
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
	    #adding the file name to the text for searching by file name...
	    norm_filnam = normalize_txt(file_name.replace('_', ' ').replace('.', ' ').replace('-', ' '))
            txt = read_as_txt(pdf_path) + " " + norm_filnam

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


@app.route('/pdf/<pdf_name>')
def return_pdf(pdf_name):
    try: # FIXME : when a client load a pdf, the others clients can't acces to the app !! :(
	f = open(app.config['PDF_DIR'] + secure_filename(pdf_name), 'rb')
	pdf_out = io.BytesIO(f.read())
	f.close()
    	return send_file(pdf_out,
			 attachment_filename=pdf_name,
			 mimetype='application/pdf;')
    except:
        abort(404)


