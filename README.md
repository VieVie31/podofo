# podofo
My simple pdf search engine with flask running actually on my raspberry-pi, so I can access and search in my pdfs databe from everywhere !!

This code flask and sqlite3 for the web server and sql queries, for extracting pdfs informations it use pdfminer...

Developped on raspian jessie lite and OS X 10.9 .

# Video Demo
On youtube :

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/iz0-QGdS9Rg/0.jpg)]
(https://www.youtube.com/watch?v=iz0-QGdS9Rg)

or [here](orissermaroix.url.ph/?p=tfidf_pdf_search_engine "tf-idf pdf search engine").


# Azure Install in VM
* Ubuntu 18.04 Server as VM Image. Open ports 22 and 80
* sudo apt update
* sudo apt install rustc libssl-dev python3-pip python3-setuptools sqlite3
* git clone https://github.com/mharrend/podofo.git
* cd podofo
* pip3 install -r requirements.txt
* Change port to 80 in run.py and shebang to python3
* cd app/sql
* ./reset-db.sh
* cd ../../
* ./run.py

