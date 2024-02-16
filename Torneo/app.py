from flask import Flask
from flask import render_template,request,redirect,session
from datetime import datetime
from flask import send_from_directory
import os

app=Flask(__name__,template_folder='templates')
app.secret_key="torneo"

@app.route('/')
def inicio():

    return render_template('menu.html')

@app.route('/login_admin')
def login():

    return render_template('login_admin.html')

@app.route('/stats')
def stats():

    return render_template('stats.html')

if __name__=='__main__':

    app.run(debug=True)


