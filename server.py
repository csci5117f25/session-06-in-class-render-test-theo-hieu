from flask import Flask, render_template, request, redirect, url_for, current_app, session
from db import add_person, get_people, setup
import os

import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET']

oauth = OAuth(app)

oauth.register(
    'auth0',
    client_id=os.environ['AUTH0_ID'],
    client_secret=os.environ['AUTH0__SECRET'],
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{os.environ["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
)

usernames = []

@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('callback', _external=True)
    )

@app.route('/callback', methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    user = token.get('userinfo')
    session['user'] = user
    return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        'https://' + os.environ.get('AUTH0_DOMAIN') +
        '/v2/logout?' + urlencode({
            'returnTo': url_for('main', _external=True),
            'client_id': os.environ.get('AUTH0_ID'),
        }, quote_via=quote_plus)
    )

@app.route('/')
def main():
    setup()
    return render_template('purecsstest.html')

# @app.route('/welcome/<name>')
# def hello(name=None, people=None):
#     people = get_people()
#     if name:
#         session['name'] = name
#     return render_template('hello.html', name=session.get("name"), people=people)

@app.route('/api/post', methods=['POST'])
def add_guestbook():
    username = request.form.get('username')
    message = request.form.get('message')
    add_person(username, message)
    return redirect(url_for('main'))