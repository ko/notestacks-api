from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, \
        url_for, abort, render_template, flash
from contextlib import closing
from config import app


DATABASE = '/home/yaksok/tmp/notestack.db'
DEBUG = False
SECRET_KEY = 'secret key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.debug = True

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()


#
# Helper functions
#
def fetchall_to_json_list_multiple(rows, list_name, list_entry, count):
    import re
    data_list = []
    for row in rows:
        entry_dict = {}
        for i in range(0,count):
            if row[i] is not None:
                entry_dict[list_entry[i]] = row[i]
        data_list.append(entry_dict)
    data_final = {list_name : data_list}
    return data_final



#
# Internal implementation of views
#
def _notes_list_get(type, to_find = None):
    import json
    if type == 'single':
        cur = g.db.execute('select title, body from note_table order by id asc')
        list_entry = ['title', 'body']
        list_count = 2
    rows = cur.fetchall()
    data_final = fetchall_to_json_list_multiple(rows, 'notes_list', list_entry, list_count);
    json_data = json.dumps(data_final, encoding='utf-8', ensure_ascii=False)
    return json_data

#
# Views
#
@app.route('/')
def notes_index():
    return 'sup'

@app.route('/api/list/')
#@crossdomain(origin='http://yaksok.net')
def notes_list_get():
    return _notes_list_get('single')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://yaksok.net')
    response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    return response

