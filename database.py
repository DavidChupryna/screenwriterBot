import logging
import sqlite3
from config import config


def create_stories_table():
    try:
        con = sqlite3.connect('stories.db')
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS stories(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            sessions INTEGER,
            tokens INTEGER,
            character TEXT,
            world TEXT,
            genre TEXT,
            additional TEXT,
            task TEXT,
            answer TEXT,
            time TEXT);
        ''')
        logging.info('table was created')
    except sqlite3.Error as error:
        logging.error(f'Error database:', error)
    finally:
        con.close()


def limit_users():
    count = 0
    try:
        con = sqlite3.connect('stories.db')
        cur = con.cursor()
        result = cur.execute('SELECT DISTINCT user_id FROM stories')
        for i in result:
            count += 1
    except Exception as error:
        logging.error("Database error", error)
    finally:
        con.close()
        return count >= int(config['LIMITS']['MAX_USERS'])


def insert_data(user_id=None, name=None, sessions=0, tokens=None, character=None, world=None, genre=None, additional=None, task=None, answer=None, time=None):
    try:
        con = sqlite3.connect('stories.db')
        cur = con.cursor()
        cur.execute(f'INSERT INTO stories(user_id, name, sessions, tokens, character, world, genre, additional, task, answer, time)'
                    f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                    (user_id, name, sessions, tokens, character, world, genre, additional, task, answer,  time,))
        logging.info('data is written to the database')
        con.commit()
    except sqlite3.Error as error:
        logging.error(f'Error database:', error)
    finally:
        con.close()


def check_user_in_db(user_id):
    try:
        con = sqlite3.connect('stories.db')
        cur = con.cursor()
        query = cur.execute('''
                    SELECT user_id
                    FROM stories
                    WHERE user_id = ?
                    LIMIT 1
                ''', (user_id,))
        result = query.fetchall()
        logging.info('get data from database')
        return bool(result)
    except sqlite3.Error as error:
        logging.error('Error database', error)
    finally:
        con.close()


def get_last_session(user_id):
    try:
        con = sqlite3.connect('stories.db')
        cur = con.cursor()
        query = cur.execute('''
            SELECT sessions
            FROM stories
            WHERE user_id = ?
            ORDER BY sessions desc 
            LIMIT 1;
        ''', (user_id,))
        result = query.fetchall()
        return result[0][0]
    except sqlite3.Error as error:
        logging.error('Error database', error)
    finally:
        con.cursor()


def update_data(user_id, column, value):
    try:
        con = sqlite3.connect('stories.db')
        cur = con.cursor()
        cur.execute(f'UPDATE stories '
                    f'SET {column} = ? '
                    f'WHERE user_id = ?;', (value, user_id))
        con.commit()
        logging.info('data has been updated')
    except sqlite3.Error as error:
        logging.error('Error database:', error)
    finally:
        con.close()