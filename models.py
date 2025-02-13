from database import connect_db

class Team:
    def __init__(self, name):
        self.name = name

    def save(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO teams (name) VALUES (?)', (self.name,))
        conn.commit()
        conn.close()

class Match:
    def __init__(self, team1_id, team2_id):
        self.team1_id = team1_id
        self.team2_id = team2_id

    def save(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO matches (team1_id, team2_id) VALUES (?, ?)', (self.team1_id, self.team2_id))
        conn.commit()
        conn.close()

    def update_score(self, score1, score2):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE matches SET score1 = ?, score2 = ? WHERE team1_id = ? AND team2_id = ?', (score1, score2, self.team1_id, self.team2_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_match(match_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT team1_id, team2_id FROM matches WHERE id = ?', (match_id,))
        match = cursor.fetchone()
        conn.close()
        if match:
            return Match(match[0], match[1])
        return None

class Group:
    def __init__(self, name):
        self.name = name

    def save(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO groups (name) VALUES (?)', (self.name,))
        conn.commit()
        conn.close()

    @staticmethod
    def add_team(group_id, team_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO group_teams (group_id, team_id) VALUES (?, ?)', (group_id, team_id))
        conn.commit()
        conn.close()

    def get_teams(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT team_id FROM group_teams WHERE group_id = ?', (self.id,))
        teams = cursor.fetchall()
        conn.close()
        return teams

class Tournament:
    def __init__(self, groups):
        self.groups = groups
        self.is_started = False

    def start(self):
        if all(len(teams) > 0 for teams in self.groups.values()):
            self.is_started = True
            print("Tournament has started!")
        else:
            print("Cannot start tournament. Ensure all teams are assigned to groups.")
