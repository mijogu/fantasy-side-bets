import os
from mysql.connector import connect, Error
from dotenv import load_dotenv, find_dotenv

loaded = load_dotenv(find_dotenv())

# Class inspired by:
# https://gist.github.com/xeoncross/494947640a7dcfe8d91496988a5bf325

class Database:
    def __init__(self) -> None:
        self.host = os.getenv('DB_HOST')
        self.database = os.getenv('DB_DATABASE')
        self.user = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')

        self.connection = None
        self.connection = connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database)
        
    def query(self, sql, args):
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        return cursor
    
    def insert(self, sql, args):
        cursor = self.query(sql, args)
        id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return id 

    # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-executemany.html
    def insertmany(self, sql, args):
        cursor = self.connection.cursor()
        cursor.executemany(sql, args)
        rowcount = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return rowcount
    
    def update(self, sql, args):
        cursor = self.query(sql, args)
        rowcount = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return rowcount
    
    def fetch(self, sql, args): 
        rows = []
        cursor = self.query(sql, args)
        if cursor.with_rows:
            rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def fetchone(self, sql, args):
        row = None
        cursor = self.query(sql, args)
        if cursor.with_rows:
            row = cursor.fetchone()
        cursor.close()
        return row
    
    def __del__(self):
        if self.connection != None:
            self.connection.close()



    
    # todo: create database if not exist
    # todo: create tables if not exit
    # todo: setup database migrations 
