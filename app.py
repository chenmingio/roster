import sqlite3
from bottle import get, put, route, run, debug, request, response

# record the roster situation of a department members under certain week

# data definition
# record is a Record(Date, String, String)
# interp. the date of the record, the Name of the member and the location of him/her.


def create_table():
    cursor.


@get('week/<wk>')
def week():
    # URL(week/String) -> list of records
    # produce the list of records within the given weeks
    # 08 -> List of records which is in week08 of year 2019
