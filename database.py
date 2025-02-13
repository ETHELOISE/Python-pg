import sqlite3

def connect_db():
    conn = sqlite3.connect('football_matches.db')
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_teams (
            group_id INTEGER,
            team_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups (id),
            FOREIGN KEY (team_id) REFERENCES teams (id),
            PRIMARY KEY (group_id, team_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            team1_id INTEGER,
            team2_id INTEGER,
            score1 INTEGER,
            score2 INTEGER,
            FOREIGN KEY (team1_id) REFERENCES teams (id),
            FOREIGN KEY (team2_id) REFERENCES teams (id)
        )
    ''')
    conn.commit()
