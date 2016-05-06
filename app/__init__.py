from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PDF_DIR'] = './pdf/'

from app import views

