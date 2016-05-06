from flask import Flask, render_template, request, redirect, url_for, abort, session
from app import app
 
@app.route('/')
@app.route('/index')
def index():
    return "YO ! :D"

@app.route('/search')
def search_page():
    return render_template('search.html')
