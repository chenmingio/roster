import bottle
import sqlite3
import json
import datetime

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
    # c.execute("CREATE TABLE records (date TEXT, name VARCHAR, location VARCHAR)")
    c.execute("CREATE TABLE names (name VARCHAR)")
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


def search_record(day):
    ''' searh sql records whose year and week number meet the requirment'''
    print(day)
    conn = sqlite3.connect('roster.db')
    c = conn.cursor()
    query = f'''
SELECT r.name as Name, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
FROM names n
LEFT JOIN
(SELECT name, group_concat(Sun) as Sunday, group_concat(Mon) as Monday, group_concat(Tue) as Tuesday, group_concat(Wed) as Wednesday, group_concat(Thu) as Thursday, group_concat(Fri) as Friday, group_concat(Sat) as Saturday
FROM
(SELECT name,
CASE date WHEN '{day}' THEN location ELSE NULL END Sun,
CASE date WHEN date('{day}','1 day') THEN location ELSE NULL END Mon,
CASE date WHEN date('{day}','2 day') THEN location ELSE NULL END Tue,
CASE date WHEN date('{day}','3 day') THEN location ELSE NULL END Wed,
CASE date WHEN date('{day}','4 day') THEN location ELSE NULL END Thu,
CASE date WHEN date('{day}','5 day') THEN location ELSE NULL END Fri,
CASE date WHEN date('{day}','6 day') THEN location ELSE NULL END Sat
FROM records
WHERE name IS NOT NULL)
GROUP BY name) r
ON r.name = n.name;
    '''
    c.execute(query)

    result = c.fetchall()
    colume = [key[0] for key in c.description]

    items = [dict(zip(colume, row)) for row in result]
    return json.dumps(items)

    conn.commit()
    conn.close()


@get('/')
def main():
    return "hello world"


@get('/day/<iso_date>')
def week(iso_date):
    ''' ISODate(yyyy-mm-dd) -> list of records
    produce the list of records within the given day + 7day
    example: 2019-01-01 -> List of records between 2019-01-01 and 2019-01-07'''
    results = search_record(iso_date)
    return results


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


if __name__ == '__main__':
    run(host='0.0.0.0', port=8000, debug=True, reloader=True)

# this is the hook for Gunicorn to run Bottle
app = bottle.default_app()
