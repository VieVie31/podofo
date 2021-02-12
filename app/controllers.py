import re
import math
import hashlib
import sqlite3
import unicodedata

from pdfminer.high_level import extract_text

from collections import Counter
from io import StringIO
from datetime import datetime
from time import time
from app import app

from .porter_stemmer import PorterStemmer

stemmer = PorterStemmer()

def lemmatize(word):
    return stemmer.stem(word, 0, len(word) - 1)

def conn_to_db(db_name):
    conn = sqlite3.connect(app.config['DB_PATH'] + db_name)
    conn.create_function('LOG', 1, math.log)
    return conn

def pdf_allready_exists(pdf_name):
    # check if a pdf is all ready in the database using the hash
    pdf_hash = hash_file(app.config['PDF_DIR_LOC'] + app.config['PDF_DIR'] + pdf_name)
    conn = conn_to_db('pdf.db')
    cursor = conn.execute("SELECT NAME, HASH, DATE FROM PDF WHERE HASH = '{}'".format(pdf_hash))
    for row in cursor: #just look if it contain one...
        conn.close()
        return True
    conn.close()
    return False

def insert_pdf_to_db(pdf_name):
    # insert a pdf into the database and return his id
    path = app.config['PDF_DIR_LOC'] + app.config['PDF_DIR'] + pdf_name
    conn = conn_to_db('pdf.db')
    cursor = conn.execute("INSERT INTO PDF (NAME, HASH, DATE) VALUES ('{}', '{}', {})".format(
                                            pdf_name, hash_file(path), int(time())))
    conn.commit()
    pdf_id = cursor.lastrowid
    conn.close()
    return pdf_id

def insert_word_to_db(pdf_id, word, freq):
    conn = conn_to_db('pdf.db')
    conn.execute("INSERT INTO FREQ (PDF_ID, WORD, W_FREQ) VALUES ({}, '{}', {})".format(
                                    pdf_id, word, str(freq)))
    conn.commit()
    conn.close()

def count_pdf():
    conn = conn_to_db('pdf.db')
    cursor = conn.execute("SELECT COUNT(*) FROM PDF")

    for row in cursor: #only one results...
        conn.close()
        return int(row[0])

    conn.close() #just in case...
    return 0

def get_results(words, page=0, nb_max_by_pages=8, nb_min_pdfs=8):
    nb_pdf = count_pdf()
    ws = "'" + "','".join(words) + "'"
    conn = conn_to_db('pdf.db')

    start_time = time()
    # a pdf_score is calculated  with sum(tf-idf) of words matched time the number of different words matched on the pdf
    cursor = conn.execute("""
        SELECT PDF_ID, NAME, DATE, WORD, SUM(W_FREQ * (TIDF)) * COUNT(WORD) AS SCORE
        FROM (SELECT PDF_ID, WORD, W_FREQ
              FROM FREQ
              WHERE WORD IN ({}))
          INNER JOIN
             (SELECT PDF_ID AS P2, WORD AS W2, {} / COUNT(PDF_ID) AS TIDF
              FROM FREQ WHERE W2 IN ({})
              GROUP BY W2) ON WORD = W2
          INNER JOIN
             (SELECT ID, NAME, DATE
              FROM PDF) ON ID = PDF_ID
        GROUP BY PDF_ID
        ORDER BY SCORE DESC
        LIMIT {} OFFSET {}
      """.format(ws, str(float(nb_pdf)), ws, nb_max_by_pages, nb_max_by_pages * page))
    conn.commit()
    end_time = time()    

    pdfs = []
    for i, row in enumerate(cursor):
        pdfs.append({"pdf_name" : row[1],
                     "date"     : format(datetime.fromtimestamp(row[2]), '%d/%m/%Y'),
                     "score"    : row[4] * 100})
    conn.close()

    if len(pdfs) == nb_max_by_pages:
        return pdfs, end_time - start_time, True #pdfs list, time took to process and True for telling to display a "next button"

    conn = conn_to_db('pdf.db')
    cursor = conn.execute("SELECT NAME, DATE FROM PDF ORDER BY RANDOM() LIMIT {}".format(str(nb_min_pdfs - len(pdfs))))
    conn.commit()

    for row in cursor:
        pdfs.append({"pdf_name" : row[0], "date" : format(datetime.fromtimestamp(row[1]), '%d/%m/%Y'), "score" : 0})

    conn.close()
    return pdfs, end_time - start_time, False #pdfs list, time took to process and False for telling to not display a "next button"

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

def normalize_txt(text):
    return re.sub('[^0-9a-zA-Z]+', ' ', text)

def convert_pdf_to_txt(pdfname): 
    text = extract_text(pdfname)

    return normalize_txt(text)

def read_as_txt(pdf_path):
    return convert_pdf_to_txt(pdf_path)

def get_word_cout(txt):
    words = map(lemmatize, txt.lower().split())
    word_count = Counter(words)
    return word_count 

