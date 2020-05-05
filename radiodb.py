#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
import json
import logging


class RadioDB:

    """description"""
    def __init__(self, filename):
        self._dbfilename = filename
        self.create_db()
        self.load_from_json()

    def create_db(self):
        try:
            db = sqlite3.connect(self._dbfilename)
            c = db.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS stations ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                      "name TEXT NOT NULL UNIQUE,"
                      "url TEXT NOT NULL,"
                      "position INTEGER"
                      ")")
            c = db.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS settings ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                      "param TEXT NOT NULL UNIQUE,"
                      "value TEXT NOT NULL"
                      ")")
            db.commit()
            c.close()
        except Error as e:
            print(e)

    def read_table_radio(self):
        db = sqlite3.connect(self._dbfilename)
        db.row_factory = sqlite3.Row
        c = db.cursor()
        c.execute('SELECT * from stations')
        records = c.fetchall()
        c.close()
        return records

    def get_settings(self):
        db = sqlite3.connect(self._dbfilename)
        db.row_factory = sqlite3.Row
        c = db.cursor()
        c.execute('SELECT * from settings')
        records = c.fetchall()
        c.close()
        return records

    def store_setting(self, key, value):
        db = sqlite3.connect(self._dbfilename)
        c = db.cursor()
        try:
            c.execute("INSERT INTO settings (param,value) "
                      "VALUES ('{}', '{}')"
                      "ON CONFLICT(param)"
                      "DO UPDATE SET value={}".format(key, value, value))

        except Error as e:
            logging.info(e)
            pass
        db.commit()
        db.close()

    def load_from_json(self):
        db = sqlite3.connect(self._dbfilename)
        c = db.cursor()

        try:
            rows = json.load(open('radio.json'))
            query = "insert into stations (name, url, position) values (?,?,?)"
            position = 1
            for station in rows:
                c.execute(query, (station['name'], station['url'], position))
                position += 1
        except Exception as e:
            logging.error(e)
            pass
        db.commit()
        db.close()
