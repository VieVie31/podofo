import re
import hashlib
import sqlite3

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from collections import Counter
from cStringIO import StringIO
from time import time
from app import app

def conn_to_db(db_name):
    conn = sqlite3.connect(app.config['DB_PATH'] + db_name)
    return conn

def pdf_allready_exists(pdf_name):
    # check if a pdf is all ready in the database using the hash
    pdf_hash = hash_file(app.config['PDF_DIR'] + pdf_name)
    conn = conn_to_db('pdf.db')
    cursor = conn.execute("SELECT NAME, HASH, DATE FROM PDF WHERE HASH = '{}'".format(pdf_hash))
    for row in cursor: #just look if it contain one...
	conn.close()
	return True
    conn.close()
    return False

def insert_pdf_to_db(pdf_name):
    # insert a pdf into the database and return his id
    path = app.config['PDF_DIR'] + pdf_name
    conn = conn_to_db('pdf.db')
    cursor = conn.execute("INSERT INTO PDF (NAME, HASH, DATE) VALUES ('{}', '{}', {})".format(
					    pdf_name, hash_file(path), int(time())))
    conn.commit()
    pdf_id = cursor.lastrowid
    conn.close()
    return pdf_id

def get_total_pdfs_word_count_of(word):
    # TODO : secure the word ??
    conn = conn_to_db('pdf.db')
    cursor = conn.execute("SELECT ID, WORD, TOTAL_COUNT FROM WORD WHERE WORD = '{}'".format(word))
    for row in cursor: #just one row...
	conn.close()
	return row[0], row[2] #id, total_count
    conn.close()
    return -1, 0 #index -1 because not exists, and total count 0

def insert_or_update_word_table(word):
    word_id, total_count = get_total_pdfs_word_count_of(word)
    # TODO : update the changes
    pass

def hash_file(path):
    # return the md5 hash of a file
    BLOCKSIZE = 65536
    hasher = hashlib.md5()

    with open(path, 'rb') as afile:
	buf = afile.read(BLOCKSIZE)
	while len(buf) > 0:
	    hasher.update(buf)
	    buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()

def convert_pdf_to_txt(pdfname): # just stollen here : https://gist.github.com/jmcarp/7105045
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = file(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return re.sub('[^0-9a-zA-Z]+', ' ', text)

def read_as_txt(pdf_path):
    try:
	return convert_pdf_to_txt(pdf_path)
    except:
	return ''

def get_word_cout(txt):
    words = txt.lower().split()
    word_count = Counter(words)
    return word_count 

