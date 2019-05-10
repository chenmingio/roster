import sqlite3
import os

from bottle import get, post, delete, route, run, debug, request, response

# record the roster situation of a department members under certain week

# data definition
# record is a Record(Date, String, String)
# interp. the date of the record, the Name of the member and the location of him/her.


def connect_db():
    '''connect db=roster.db and build cursor'''
    conn = sqlite3.connect('roster.db')
    c = conn.cursor()


def create_table():
    ''' create table for data record'''
    conn = sqlite3.connect('roster.db')
    c = conn.cursor()
    c.execute("CREATE TABLE records (date TEXT, name VARCHAR, location VARCHAR)")
    conn.commit()
    conn.close()


def insert_record(record):
    ''' insert a record according to given compound data '''
    conn = sqlite3.connect('roster.db')
    c = conn.cursor()
    c.execute("INSERT INTO records (date, name, location) VALUES (?,?,?)", record)
    conn.commit()
    conn.close()


def delete_record(record):
    ''' delete the record in DB'''
    conn = sqlite3.connect('roster.db')
    c = conn.cursor()
    c.execute("DELETE FROM records WHERE date=? AND name=?", record)
    conn.commit()
    conn.close()


@get('/')
def main():
    return "hello world"


@get('/week/<wk>')
def week():
    ''' URL(week/String) -> list of records
    produce the list of records within the given weeks
    example: 08 -> List of records which is in week08 of year 2019'''
    pass


@post('/people/<name>')
def upsert(name):
    ''' add a record into DB according to request, by trying to delete it if already exists'''
    delete_record((request.forms.date, request.forms.name))
    record_data = (request.forms.date, request.forms.name,
                   request.forms.location)
    insert_record(record_data)


@delete('/people/<name>')
def delete(name):
    ''' delete a record'''
    to_delete = (request.forms.date, request.forms.name)
    delete_record(to_delete)


# create_table()


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True, reloader=True)
