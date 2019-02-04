from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)

from .db import get_db
import requests
import json


bp = Blueprint('auth', __name__, url_prefix='/auth')

USER_ADDR = 'http://users:5000'


@bp.route('/login', methods=['POST'])
def login():
    print("Syslog: login")
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        database = get_db()
        resp = None

        data = {
                'email': email,
                'id': -1
                }

        row = database.execute(
            'SELECT id FROM user WHERE email = ? and password = ?', (email, password,)
            ).fetchone()

        if row:
            print("Successful login")
            data['msg'] = "Login successful"
            data['id'] = row['id']
            resp = jsonify(data)
            resp.status_code = 200
            return resp

        print("Unsuccessful login")
        data['msg'] = 'Incorrect login or password'
        resp = jsonify(data)
        resp.status_code = 400
        return resp

    abort(404)


@bp.route('/register', methods=['POST'])
def register():
    print("Syslog: register")
    if request.method == 'POST':
        login = request.json['login']
        email = request.json['email']
        password = request.json['password']
        try:
            database = get_db()
        except:
            import traceback
            traceback.print_exc()

        data = {
                'id': -1,
                }

        row = database.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
            ).fetchone()

        if row:
            print("User already exists")
            resp = jsonify(data)
            resp.status_code = 400
            return resp

        print('Sending to:')
        print(USER_ADDR + '/api/users/')
        r = requests.post('{}/api/users/'.format(USER_ADDR),
                          data=json.dumps({'email': email, 'login': login}),
                          headers={'content-type': 'application/json'})
        print("Status code = {}".format(r.status_code))

        print(r)

        if r.status_code == 201:
            database.execute(
                'INSERT INTO user (id, email, password) VALUES (?, ?, ?)',
                (r.json()['id'], email, password)
            )
            database.commit()
            data['id'] = r.json()['id']
            resp = jsonify(data)
            resp.status_code = 202
            return resp

        resp = jsonify(data)
        resp.status_code = 400
        return resp

    abort(404)


@bp.route('/')
def home():
    return '''
        <form method="post" action="login">
            <p>Email:<input type=text name=email>
            <p>Password:<input type=text name=password>
            <p>Login<input type=text name=login>
            <p><input type=submit value=Login>
        </form>
        <br>
        <form method="post" action="register">
            <p>Email:<input type=text name=email>
            <p>Login:<input type=text name=login>
            <p>Password:<input type=text name=password>
            <p><input type=submit value=Register>
        </form>
    '''
