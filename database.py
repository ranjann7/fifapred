import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'database.db'

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            fifa_rank INTEGER,
            attack INTEGER,
            defense INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1_id INTEGER NOT NULL,
            team2_id INTEGER NOT NULL,
            score1 INTEGER,
            score2 INTEGER,
            winner TEXT,
            tournament TEXT,
            match_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (team1_id) REFERENCES teams(id),
            FOREIGN KEY (team2_id) REFERENCES teams(id)
        )
    ''')
    
    # Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1_id INTEGER NOT NULL,
            team2_id INTEGER NOT NULL,
            predicted_winner TEXT,
            team1_prob FLOAT,
            team2_prob FLOAT,
            draw_prob FLOAT,
            actual_result TEXT,
            accuracy FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (team1_id) REFERENCES teams(id),
            FOREIGN KEY (team2_id) REFERENCES teams(id)
        )
    ''')
    
    # Tournament simulations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournament_simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_name TEXT,
            predicted_champion TEXT,
            confidence FLOAT,
            simulation_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_sample_teams():
    """Add sample team data"""
    teams = [
        ('Argentina', 1, 88, 82),
        ('France', 2, 87, 81),
        ('Brazil', 1, 86, 80),
        ('England', 4, 85, 79),
        ('Spain', 8, 84, 78),
        ('Germany', 15, 82, 76),
        ('Netherlands', 8, 81, 75),
        ('Belgium', 13, 80, 74),
        ('Italy', 17, 79, 77),
        ('Portugal', 20, 78, 73),
    ]
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    for team in teams:
        try:
            cursor.execute(
                'INSERT INTO teams (name, fifa_rank, attack, defense) VALUES (?, ?, ?, ?)',
                team
            )
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    print("Sample teams added!")

def get_team_by_name(team_name):
    """Get team data by name"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM teams WHERE name = ?', (team_name,))
    result = cursor.fetchone()
    
    conn.close()
    return result

def add_prediction(team1_id, team2_id, predicted_winner, probs):
    """Save prediction to database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions 
        (team1_id, team2_id, predicted_winner, team1_prob, team2_prob, draw_prob)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (team1_id, team2_id, predicted_winner, probs[0], probs[1], probs[2]))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
    add_sample_teams()
