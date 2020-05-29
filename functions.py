import sqlite3
import random
import string

class DatabaseManager:
    def __init__(self, database: str):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        f = open('config/forbidden_urls.config', 'r')
        self.forbidden_url = f.readlines()
        f.close()

    def shorten(self, url: str):
        cursor = self.connection.cursor()
        exists = True
        new_url = generate_random_url()
        while exists:
            cursor.execute(
                'SELECT id FROM urls WHERE new=?;',
                (new_url, )
            )
            exists = (cursor.rowcount != -1) or (new_url in self.forbidden_url)
            if exists:
                cursor.execute(
                    'SELECT COUNT(*) FROM urls ' +
                    'WHERE LENGTH(new)=?;',
                    (len(new_url),)
                )
                if cursor.rowcount == pow(26, len(new_url)):
                    new_url = generate_random_url(len(new_url) + 1)
                else:
                    new_url = generate_random_url(len(new_url))

        cursor.execute(
            'INSERT INTO urls(original, new) VALUES(' +
            '?, ?);',
            (url, new_url)
        )
        return new_url

    def build(self):
        cursor = self.connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS ' +
            'urls(id INTEGER PRIMARY KEY AUTOINCREMENT, ' +
            'original TEXT NOT NULL, ' +
            'new TEXT NOT NULL);'
        )
        self.connection.commit()

    def clean_database(self):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM urls;')
        self.connection.commit()

    def get_url(self, url: str):
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT original FROM urls ' +
            'WHERE new=?;',
            (url, )
        )
        return cursor.fetchone()[0]


def generate_random_url(length: int = 4):
    return ''.join(random.choices(string.ascii_lowercase, k=length))