from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PDF_DIR'] = './pdf/'
app.config['DB_PATH'] = './app/sql/'

from app import views

