import hashlib
import sqlite3

from collections import Counter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from time import time
from app import app

def conn_to_db(db_name):
    conn = sqlite3.connect(app.config['DB_PATH'] + db_name)
    return conn

def pdf_allready_exists(pdf_name):
    # TODO : check if a pdf is all ready in the database using the hash
    return False

def insert_pdf_to_db(pdf_name):
    path = app.config['PDF_DIR'] + pdf_name
    conn = conn_to_db('pdf.db')
    conn.execute("INSERT INTO PDF (NAME, HASH, DATE) VALUES ('{}', '{}', {})".format(
				   pdf_name, hash_file(path), int(time())))
    conn.commit()
    conn.close()

def hash_file(path):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()

    with open(path, 'rb') as afile:
	buf = afile.read(BLOCKSIZE)
	while len(buf) > 0:
	    hasher.update(buf)
	    buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()

def convert_pdf_to_txt(path):
    #from : http://stackoverflow.com/questions/5725278/how-do-i-use-pdfminer-as-a-library
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')

    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    parser.set_document(doc)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(
      fp, pagenos, maxpages=maxpages,
      password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

def read_as_txt(pdf_path):
    try:
	return convert_pdf_to_txt(pdf_path)
    except:
	return ''

def get_word_cout(txt):
    words = txt.lower().split()
    word_count = Counter(words)
    return word_count 

