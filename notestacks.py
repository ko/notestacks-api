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
    data_list = []
    for row in rows:
        entry_dict = {}
        for i in range(0,count):
            if row[i] is not None:
                entry_dict[list_entry[i]] = row[i]
        data_list.append(entry_dict)
    data_final = {list_name : data_list}
    return data_final

def fetchall_to_dict(rows, list_entry, count):
    data_list = []
    for row in rows:
        entry_dict = {}
        for i in range(0, count):
            if row[i] is not None:
                entry_dict[list_entry[i]] = row[i]
        data_list.append(entry_dict)
    return data_list

#
# Internal implementation of views
#
def _notes_list_get(type, to_find = None):
    import json
    if type == 'single':
        cur = g.db.execute('select id, title, body from note_table order by id asc')
        list_entry = ['id', 'title', 'body']
        list_count = 3
    rows = cur.fetchall()
    data_final = fetchall_to_json_list_multiple(rows, 'notes_list', list_entry, list_count)
    json_data = json.dumps(data_final, encoding='utf-8', ensure_ascii=False)
    return json_data

def _note_update(sid, nid, title, body):

    query = 'UPDATE note_table '
    query += 'SET stackid=?, title=?, body=? '
    query += 'WHERE id=?;'
    g.db.execute(query, [sid, title, body, nid])
    g.db.commit()
    return 'sup'

#
# Views
#
@app.route('/')
def notes_index():
    return 'sup'

@app.route('/api/list/get/')
#@crossdomain(origin='http://yaksok.net')
def notes_list_get():
    return _notes_list_get('single')

note_update = 1
note_create = 2

@app.route('/api/list/set/', methods = ['POST'])
def notes_list_set():
    type = int(request.form['type'])
    if (type == note_update):
        sid = request.form['stackid']
        nid = request.form['noteid']
        ntitle = request.form['title']
        nbody = request.form['body']
        _note_update(sid, nid, ntitle, nbody)
    elif (type == note_create):
        ntitle = request.form['title']
        nbody = request.form['body']
        stackid = int(request.form['stackid'])
    return notes_list_get()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://yaksok.net')
    response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    return response

