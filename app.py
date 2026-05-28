from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fifa2026secret'

# Global variables for models and data
model = None
scaler = None
teams_data = None

def load_model():
    """Load trained ML model"""
    global model, scaler
    model_path = 'model/predictor.pkl'
    scaler_path = 'model/scaler.pkl'
    
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    else:
        # Train if model doesn't exist
        from model.train_model import train_and_save_model
        train_and_save_model()
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

def load_teams_data():
    """Load teams data from CSV files and derive attack/defense ratings."""
    global teams_data

    rankings_path = os.path.join('dataset', 'fifa_rankings.csv')
    kaggle_results = os.path.join('dataset', 'datasetfrom1872to2025', 'results.csv')
    fallback_results = os.path.join('dataset', 'matches.csv')
    results_path = kaggle_results if os.path.exists(kaggle_results) else fallback_results

    ranking_df = pd.read_csv(rankings_path) if os.path.exists(rankings_path) else pd.DataFrame()
    results_df = pd.read_csv(results_path) if os.path.exists(results_path) else pd.DataFrame()

    team_metrics = {}
    if not results_df.empty and {'home_team', 'away_team', 'home_score', 'away_score'}.issubset(results_df.columns):
        home_stats = results_df.groupby('home_team').agg(
            home_games=('home_team', 'count'),
            goals_for_home=('home_score', 'mean'),
            goals_against_home=('away_score', 'mean')
        )
        away_stats = results_df.groupby('away_team').agg(
            away_games=('away_team', 'count'),
            goals_for_away=('away_score', 'mean'),
            goals_against_away=('home_score', 'mean')
        )

        merged = home_stats.join(away_stats, how='outer').fillna(0)
        for team, row in merged.iterrows():
            games = max(1.0, row['home_games'] + row['away_games'])
            gf = (row['goals_for_home'] * row['home_games'] + row['goals_for_away'] * row['away_games']) / games
            ga = (row['goals_against_home'] * row['home_games'] + row['goals_against_away'] * row['away_games']) / games

            attack = float(np.clip(60 + ((gf - 0.2) / 2.8) * 35, 60, 95))
            defense = float(np.clip(90 - ((ga - 0.2) / 2.8) * 30, 60, 90))
            team_metrics[team] = {'attack': round(attack, 1), 'defense': round(defense, 1)}

    teams_data = {}
    if not ranking_df.empty and {'country', 'rank'}.issubset(ranking_df.columns):
        for _, row in ranking_df.iterrows():
            team = str(row['country']).strip()
            rank = int(row['rank']) if pd.notna(row['rank']) else 100
            metric = team_metrics.get(team, {'attack': 72.0, 'defense': 72.0})
            teams_data[team] = {
                'fifa_rank': rank,
                'attack': metric['attack'],
                'defense': metric['defense']
            }

    if not teams_data:
        teams_data = {
            'Argentina': {'fifa_rank': 1, 'attack': 88, 'defense': 82},
            'France': {'fifa_rank': 2, 'attack': 87, 'defense': 81},
            'England': {'fifa_rank': 4, 'attack': 85, 'defense': 79},
            'Spain': {'fifa_rank': 8, 'attack': 84, 'defense': 78},
            'Germany': {'fifa_rank': 15, 'attack': 82, 'defense': 76},
            'Brazil': {'fifa_rank': 1, 'attack': 86, 'defense': 80},
        }

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    """Prediction page"""
    if teams_data:
        teams = sorted(list(teams_data.keys()))
    else:
        teams = []
    return render_template('predict.html', teams=teams)

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    return render_template('dashboard.html')

@app.route('/tournament')
def tournament():
    """Tournament simulator"""
    return render_template('tournament.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for match prediction"""
    try:
        data = request.json
        team1 = data.get('team1')
        team2 = data.get('team2')
        
        if not team1 or not team2:
            return jsonify({'error': 'Teams required'}), 400
        
        if team1 not in teams_data or team2 not in teams_data:
            return jsonify({'error': 'Invalid team'}), 400
        
        # Get team stats
        t1_stats = teams_data[team1]
        t2_stats = teams_data[team2]
        
        # Prepare features
        features = np.array([[
            t1_stats['fifa_rank'],
            t2_stats['fifa_rank'],
            t1_stats['attack'],
            t2_stats['attack'],
            t1_stats['defense'],
            t2_stats['defense'],
            t1_stats['attack'] - t2_stats['defense'],  # Attack vs Defense differential
            0.5  # Home advantage (neutral)
        ]])
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        class_probability = {
            int(cls): float(prob)
            for cls, prob in zip(model.classes_, probability)
        }
        
        # Predict score
        goal_diff = (t1_stats['attack'] - t2_stats['defense']) / 20
        team1_goals = max(0, int(np.random.normal(1.5 + goal_diff * 0.3, 0.8)))
        team2_goals = max(0, int(np.random.normal(1.5 - goal_diff * 0.3, 0.8)))
        
        result = {
            'team1': team1,
            'team2': team2,
            'predicted_winner': team1 if prediction == 1 else (team2 if prediction == 2 else 'Draw'),
            'team1_win_prob': class_probability.get(1, 0.0) * 100,
            'team2_win_prob': class_probability.get(2, 0.0) * 100,
            'draw_prob': class_probability.get(0, 0.0) * 100,
            'predicted_score': f"{team1_goals}-{team2_goals}"
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams')
def get_teams():
    """Get all teams data"""
    return jsonify(teams_data)

@app.route('/api/tournament-simulate', methods=['POST'])
def simulate_tournament():
    """Simulate tournament"""
    try:
        # Simulate 2026 World Cup
        results = {
            'phase': 'Semi-Finals',
            'matches': [
                {'team1': 'Argentina', 'team2': 'France', 'winner': 'Argentina', 'prob': 55},
                {'team1': 'Brazil', 'team2': 'Germany', 'winner': 'Brazil', 'prob': 60}
            ],
            'final': {
                'team1': 'Argentina',
                'team2': 'Brazil',
                'predicted_winner': 'Argentina',
                'confidence': 52
            }
        }
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_teams_data()
    load_model()
    app.run(debug=True, port=5000)
