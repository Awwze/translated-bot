import sqlite3


def connect(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor

def create_users_table():
    connection, cursor = connect('translations.db')
    cursor.executescript('''
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            chat_id BIGINT NOT NULL UNIQUE
        );
    ''')
    connection.commit()

# create_users_table()

def create_translations_table():
    connection, cursor = connect('translations.db')
    cursor.executescript('''
    DROP TABLE IF EXISTS translations;
    CREATE TABLE IF NOT EXISTS translations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lang_from TEXT,
        lang_to TEXT,
        original TEXT,
        translated TEXT,
        user_id INTEGER REFERENCES users(id)
        );    
    ''')
    connection.commit()

# create_users_table()
# create_translations_table()

def is_user_exists(chat_id):
    connection, cursor = connect('translations.db')
    cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
    user_id = cursor.fetchone()
    if not user_id:
        return False
    return True

def add_user(first_name, chat_id):
    connection, cursor = connect('translations.db')
    sql = 'INSERT INTO users(first_name, chat_id) VALUES(?,?);'
    if not is_user_exists(chat_id):
        cursor.execute(sql, (first_name, chat_id))
        connection.commit()
        print(f'Добавили пользователя: {first_name}-{chat_id}')

def get_user_id(chat_id):
    connection, cursor = connect('translations.db')
    sql = 'SELECT id FROM users WHERE chat_id = ?;'
    cursor.execute(sql, (chat_id,))
    return cursor.fetchone()[0]

def add_translations(lang_from, lang_to, original, chat_id, translated):
    connection, cursor = connect('translations.db')
    trnsltn = 'INSERT INTO translations(lang_from, lang_to, original, user_id, translated) VALUES (?,?,?,?,?);'
    user_id = get_user_id(chat_id)
    cursor.execute(trnsltn, (lang_from, lang_to, original, user_id, translated))
    connection.commit()
    print('Добавили всю информацию о переводе')

def get_history(user_id):
    connection, cursor = connect('translations.db')
    sql = 'SELECT * FROM translations;'
    cursor.execute(sql)
    return cursor.fetchone()[0]
