import os
from collections import defaultdict

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def _pick_results_path():
    kaggle_path = os.path.join("dataset", "datasetfrom1872to2025", "results.csv")
    fallback_path = os.path.join("dataset", "matches.csv")
    if os.path.exists(kaggle_path):
        return kaggle_path
    if os.path.exists(fallback_path):
        return fallback_path
    raise FileNotFoundError("No results dataset found in dataset/ folder")


def _load_rankings_map():
    path = os.path.join("dataset", "fifa_rankings.csv")
    if not os.path.exists(path):
        return {}

    df = pd.read_csv(path)
    if "country" not in df.columns:
        return {}

    rank_col = "rank" if "rank" in df.columns else None
    if rank_col is None:
        return {}

    return {
        str(row["country"]).strip(): int(row[rank_col])
        for _, row in df.iterrows()
        if pd.notna(row["country"]) and pd.notna(row[rank_col])
    }


def _attack_from_avg_goals(avg_goals):
    clipped = float(np.clip(avg_goals, 0.2, 3.0))
    return 60 + ((clipped - 0.2) / 2.8) * 35


def _defense_from_avg_conceded(avg_conceded):
    clipped = float(np.clip(avg_conceded, 0.2, 3.0))
    return 90 - ((clipped - 0.2) / 2.8) * 30


def _team_stats(stats, team_name):
    s = stats[team_name]
    if s["games"] == 0:
        return {
            "attack": 72.0,
            "defense": 72.0,
            "form": 0.5,
            "goals_for_avg": 1.2,
            "goals_against_avg": 1.2,
            "win_rate": 0.33,
        }

    goals_for_avg = s["goals_for"] / s["games"]
    goals_against_avg = s["goals_against"] / s["games"]
    form = s["points"] / (s["games"] * 3)
    win_rate = s["wins"] / s["games"]

    return {
        "attack": _attack_from_avg_goals(goals_for_avg),
        "defense": _defense_from_avg_conceded(goals_against_avg),
        "form": float(np.clip(form, 0.0, 1.0)),
        "goals_for_avg": goals_for_avg,
        "goals_against_avg": goals_against_avg,
        "win_rate": win_rate,
    }


def build_training_data():
    path = _pick_results_path()
    rankings = _load_rankings_map()

    df = pd.read_csv(path)
    required_cols = {"home_team", "away_team", "home_score", "away_score", "date"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Dataset missing required columns: {required_cols - set(df.columns)}")

    df = df.dropna(subset=["home_team", "away_team", "home_score", "away_score", "date"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    stats = defaultdict(
        lambda: {
            "games": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "points": 0,
        }
    )

    X = []
    y = []

    for _, row in df.iterrows():
        home_team = str(row["home_team"]).strip()
        away_team = str(row["away_team"]).strip()
        home_score = int(row["home_score"])
        away_score = int(row["away_score"])

        neutral_raw = row["neutral"] if "neutral" in row else False
        neutral = str(neutral_raw).strip().lower() == "true"

        h = _team_stats(stats, home_team)
        a = _team_stats(stats, away_team)

        home_rank = rankings.get(home_team, 100)
        away_rank = rankings.get(away_team, 100)

        features = [
            home_rank,
            away_rank,
            h["attack"],
            a["attack"],
            h["defense"],
            a["defense"],
            h["attack"] - a["defense"],
            0.0 if neutral else 1.0,
        ]
        X.append(features)

        if home_score > away_score:
            label = 1
        elif home_score < away_score:
            label = 2
        else:
            label = 0
        y.append(label)

        # Update stats after using pre-match features.
        stats[home_team]["games"] += 1
        stats[away_team]["games"] += 1
        stats[home_team]["goals_for"] += home_score
        stats[home_team]["goals_against"] += away_score
        stats[away_team]["goals_for"] += away_score
        stats[away_team]["goals_against"] += home_score

        if home_score > away_score:
            stats[home_team]["wins"] += 1
            stats[away_team]["losses"] += 1
            stats[home_team]["points"] += 3
        elif home_score < away_score:
            stats[away_team]["wins"] += 1
            stats[home_team]["losses"] += 1
            stats[away_team]["points"] += 3
        else:
            stats[home_team]["draws"] += 1
            stats[away_team]["draws"] += 1
            stats[home_team]["points"] += 1
            stats[away_team]["points"] += 1

    return np.array(X), np.array(y), path


def train_and_save_model():
    """Train model using historical match data and save artifacts."""
    X, y, source_path = build_training_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        max_depth=16,
        min_samples_leaf=2,
        class_weight="balanced",
    )
    model.fit(X_train_scaled, y_train)

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, os.path.join("model", "predictor.pkl"))
    joblib.dump(scaler, os.path.join("model", "scaler.pkl"))

    accuracy = model.score(X_test_scaled, y_test)
    print(f"Training source: {source_path}")
    print(f"Samples used: {len(X)}")
    print(f"Model trained with {accuracy * 100:.2f}% accuracy")

if __name__ == '__main__':
    train_and_save_model()
