from flask import Flask, render_template, request, redirect, url_for, abort, session
from app import app
 
@app.route('/')
@app.route('/index')
def index_page():
    return "YO ! :D"

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/upload')
def upload_page():
    return "Here will be the upload form..."
