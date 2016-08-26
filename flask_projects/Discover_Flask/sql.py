import sqlite3

with sqlite3.connect('sample.db') as connection:
    _cursor = connection.cursor()
    _cursor.execute("DROP TABLE posts")
    _cursor.execute("CREATE TABLE posts(title TEXT, description TEXT)")
    _cursor.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    _cursor.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')