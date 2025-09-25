from flask import Flask, render_template, request, redirect, url_for, current_app
from db import add_person, get_people, setup

app = Flask(__name__)

usernamess = []

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    setup()
    people = get_people()
    return render_template('hello.html', name=name, people=people)

@app.route('/api/post', methods=['POST'])
def add_guestbook():
    username = request.form.get('username')
    message = request.form.get('message')
    add_person(username, message)
    return redirect(url_for('hello'))