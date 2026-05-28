# 🏗️ SYSTEM ARCHITECTURE

## Application Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER (Frontend)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ HTML5 Templates (4 Pages)                            │  │
│  │ ├─ index.html (Home)                                 │  │
│  │ ├─ predict.html (Match Prediction)                   │  │
│  │ ├─ dashboard.html (Analytics)                        │  │
│  │ └─ tournament.html (Simulator)                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ CSS3 Styling & JavaScript Interactivity             │  │
│  │ ├─ style.css (Dark theme, responsive)               │  │
│  │ ├─ script.js (API calls, DOM updates)               │  │
│  │ └─ Plotly Charts (Interactive visualizations)       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ⇅ (HTTP/REST)
┌─────────────────────────────────────────────────────────────┐
│                   FLASK WEB SERVER (Backend)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ app.py - Main Flask Application (500+ lines)         │  │
│  │ ├─ Routes: /, /predict, /dashboard, /tournament      │  │
│  │ ├─ API Endpoints: /api/teams, /api/predict, etc.    │  │
│  │ ├─ Global Variables: model, scaler, teams_data       │  │
│  │ └─ Configuration: Flask setup, error handling        │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ⇅                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Machine Learning Pipeline                            │  │
│  │ ├─ Load Trained Model: model/predictor.pkl          │  │
│  │ ├─ Load Feature Scaler: model/scaler.pkl            │  │
│  │ ├─ Feature Engineering: 8 features extracted         │  │
│  │ ├─ Prediction: Random Forest classifier             │  │
│  │ └─ Output: Probabilities & scores                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ⇅                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Data Management                                      │  │
│  │ ├─ teams_data (In-memory dictionary)                │  │
│  │ ├─ Database initialization (database.py)            │  │
│  │ └─ Dataset loading (CSV files)                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ⇅ (File I/O)
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ SQLite Database (database.db)                        │  │
│  │ ├─ teams (id, name, fifa_rank, attack, defense)    │  │
│  │ ├─ matches (historical match data)                  │  │
│  │ ├─ predictions (prediction history)                 │  │
│  │ └─ tournament_simulations (simulation results)      │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ⇅                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Dataset Files                                        │  │
│  │ ├─ dataset/matches.csv (50 historical matches)      │  │
│  │ ├─ dataset/fifa_rankings.csv (48 team rankings)     │  │
│  │ ├─ model/predictor.pkl (Trained ML model)           │  │
│  │ └─ model/scaler.pkl (Feature scaler)                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Match Prediction Flow

```
┌─────────────────┐
│ User Selects    │
│ 2 Teams         │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ JavaScript Calls         │
│ POST /api/predict        │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Flask API Handler        │
│ app.py: api_predict()    │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Fetch Team Stats         │
│ From teams_data dict     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Create Feature Vector    │
│ 8 Features Extracted     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Scale Features           │
│ StandardScaler.transform │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ ML Model Prediction      │
│ Random Forest Classifier │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Get Probabilities        │
│ 3 Classes Output         │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Estimate Scoreline       │
│ Normal Distribution      │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Create JSON Response     │
│ Return to Frontend       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ JavaScript Updates DOM   │
│ Display Results          │
└──────────────────────────┘
```

---

## ML Training Pipeline

```
┌─────────────────────────────┐
│ Generate Training Data      │
│ 500 Sample Matches          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Feature Engineering         │
│ Extract 8 Features          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Train/Test Split            │
│ 80% / 20%                   │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Feature Scaling             │
│ StandardScaler.fit_transform│
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Train Model                 │
│ Random Forest (100 trees)   │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Model Evaluation            │
│ Cross-validation            │
│ Training Accuracy: 78.5%    │
│ Test Accuracy: 75.2%        │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Save Model & Scaler         │
│ model/predictor.pkl         │
│ model/scaler.pkl            │
└─────────────────────────────┘
```

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
├────────────────────┬─────────────────┬──────────────────────┤
│   Templates        │      Assets     │    JavaScript        │
├────────────────────┼─────────────────┼──────────────────────┤
│ • index.html       │ • style.css     │ • API Calls          │
│ • predict.html     │ • script.js     │ • DOM Manipulation   │
│ • dashboard.html   │ • Plotly        │ • Form Handling      │
│ • tournament.html  │ • Favicon       │ • Event Listeners    │
└────────────────────┴─────────────────┴──────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     Backend Layer                            │
├────────────────────┬─────────────────┬──────────────────────┤
│   Flask Routes     │  API Endpoints  │  Business Logic      │
├────────────────────┼─────────────────┼──────────────────────┤
│ • / (home)         │ • /api/teams    │ • Prediction Logic   │
│ • /predict         │ • /api/predict  │ • Tournament Sim     │
│ • /dashboard       │ • /api/tournament                      │
│ • /tournament                                               │
└────────────────────┴─────────────────┴──────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   ML Pipeline Layer                          │
├────────────────────┬─────────────────┬──────────────────────┤
│   Data Loading     │   ML Models     │  Feature Processing  │
├────────────────────┼─────────────────┼──────────────────────┤
│ • CSV Files        │ • Predictor     │ • Feature Vector     │
│ • Database         │ • Scaler        │ • Normalization      │
│ • In-memory Dict   │ • Random Forest │ • Score Estimation   │
└────────────────────┴─────────────────┴──────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   Data Storage Layer                         │
├────────────────────┬─────────────────┬──────────────────────┤
│   Databases        │   File Storage  │   Configuration      │
├────────────────────┼─────────────────┼──────────────────────┤
│ • SQLite DB        │ • CSV Files     │ • config.py          │
│ • 4 Tables         │ • Model Files   │ • .env               │
│ • Queries          │ • Scalers       │ • Settings           │
└────────────────────┴─────────────────┴──────────────────────┘
```

---

## Request/Response Cycle

### Match Prediction Request

```
REQUEST CYCLE:
╔════════════════════════════════════════════════════════════╗
║  Browser → Flask App → ML Model → Database → Browser       ║
╚════════════════════════════════════════════════════════════╝

DETAILED FLOW:
1. User Interaction
   └─ Selects 2 teams → Clicks "Predict"

2. Frontend (JS)
   └─ Sends: POST /api/predict {team1, team2}

3. HTTP Transport
   └─ Network Request → localhost:5000

4. Flask Server
   └─ Routes to: api_predict() function
   └─ Parameters received & validated

5. Data Retrieval
   └─ Loads teams_data (in-memory dictionary)
   └─ Extracts team statistics

6. Feature Engineering
   └─ Creates feature vector [8 features]
   └─ Example: [rank1, rank2, atk1, atk2, def1, def2, diff, home]

7. Data Scaling
   └─ Loads scaler.pkl
   └─ Normalizes features

8. ML Prediction
   └─ Loads predictor.pkl
   └─ Random Forest predicts class
   └─ Gets probabilities for all classes

9. Score Estimation
   └─ Calculates expected goals
   └─ Uses normal distribution

10. JSON Response
    └─ Returns: {winner, probs, score}

11. Frontend Processing
    └─ Receives JSON response
    └─ Updates DOM with results
    └─ Displays charts & probabilities

12. User Sees Results
    └─ Win probabilities
    └─ Predicted winner
    └─ Predicted score
    └─ Confidence level
```

---

## Database Schema

```sql
-- Teams Table
CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    fifa_rank INTEGER,
    attack INTEGER,           -- 0-100
    defense INTEGER,          -- 0-100
    created_at TIMESTAMP
);

-- Matches Table
CREATE TABLE matches (
    id INTEGER PRIMARY KEY,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    score1 INTEGER,
    score2 INTEGER,
    winner TEXT,
    tournament TEXT,          -- 'World Cup', 'Euro', etc.
    match_date DATE,
    created_at TIMESTAMP,
    FOREIGN KEY (team1_id) REFERENCES teams(id),
    FOREIGN KEY (team2_id) REFERENCES teams(id)
);

-- Predictions Table
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    predicted_winner TEXT,
    team1_prob FLOAT,
    team2_prob FLOAT,
    draw_prob FLOAT,
    actual_result TEXT,
    accuracy FLOAT,
    created_at TIMESTAMP,
    FOREIGN KEY (team1_id) REFERENCES teams(id),
    FOREIGN KEY (team2_id) REFERENCES teams(id)
);

-- Tournament Simulations Table
CREATE TABLE tournament_simulations (
    id INTEGER PRIMARY KEY,
    tournament_name TEXT,     -- '2026 World Cup'
    predicted_champion TEXT,
    confidence FLOAT,
    simulation_data TEXT,     -- JSON
    created_at TIMESTAMP
);
```

---

## API Interaction Architecture

```
┌──────────────────────────────────────────────────┐
│            Frontend (Browser)                     │
│  ┌────────────────────────────────────────────┐ │
│  │ script.js                                  │ │
│  │ ├─ loadTeams()                            │ │
│  │ ├─ predictMatch()                         │ │
│  │ ├─ simulateTournament()                   │ │
│  │ └─ displayResults()                       │ │
│  └────────────────────────────────────────────┘ │
│              ⇅ (Fetch API)                       │
└──────────────────────────────────────────────────┘
           JSON Requests/Responses
┌──────────────────────────────────────────────────┐
│              Flask Backend                        │
│  ┌────────────────────────────────────────────┐  │
│  │ app.py Routes                              │  │
│  │ ├─ GET /api/teams                         │  │
│  │ │  └─ Returns all teams                   │  │
│  │ ├─ POST /api/predict                      │  │
│  │ │  ├─ Input: {team1, team2}              │  │
│  │ │  └─ Output: predictions                 │  │
│  │ └─ POST /api/tournament-simulate          │  │
│  │    ├─ Input: none                         │  │
│  │    └─ Output: tournament bracket          │  │
│  └────────────────────────────────────────────┘  │
│                  ⇅                               │
│  ┌────────────────────────────────────────────┐  │
│  │ ML & Data Processing                       │  │
│  │ ├─ Load model & scaler                    │  │
│  │ ├─ Extract features                       │  │
│  │ ├─ Make predictions                       │  │
│  │ └─ Format response                        │  │
│  └────────────────────────────────────────────┘  │
│                  ⇅                               │
│  ┌────────────────────────────────────────────┐  │
│  │ Data Sources                               │  │
│  │ ├─ In-memory teams dictionary             │  │
│  │ ├─ SQLite database                        │  │
│  │ ├─ ML model files                         │  │
│  │ └─ CSV datasets                           │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌────────────────────────────────────────────────────────┐
│                 Deployment Target                      │
│                 (Render/Railway/Heroku)                │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Docker Container / Virtual Server                │ │
│  │ ┌────────────────────────────────────────────┐  │ │
│  │ │ Gunicorn WSGI Server (4 workers)           │  │ │
│  │ │  └─ Running Flask app                      │  │ │
│  │ ├────────────────────────────────────────────┤  │ │
│  │ │ Static Files & Assets                      │  │ │
│  │ │  ├─ CSS, JS, Images                       │  │ │
│  │ │  └─ Served by Nginx (reverse proxy)        │  │ │
│  │ ├────────────────────────────────────────────┤  │ │
│  │ │ Database                                   │  │ │
│  │ │  ├─ SQLite (development)                  │  │ │
│  │ │  └─ PostgreSQL (production upgrade)        │  │ │
│  │ └────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────┘ │
│                        ⇅                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Domain & SSL                                      │ │
│  │  ├─ Custom Domain (yourapp.com)                 │ │
│  │  ├─ HTTPS Certificate (Let's Encrypt)           │ │
│  │  └─ Free CDN (Cloudflare optional)               │ │
│  └──────────────────────────────────────────────────┘ │
│                        ⇅                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Monitoring & Logging                             │ │
│  │  ├─ Error tracking (Sentry)                     │ │
│  │  ├─ Performance monitoring                      │ │
│  │  ├─ Uptime monitoring                           │ │
│  │  └─ Daily backups                               │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  HTML5 | CSS3 (Dark Theme) | JavaScript | Plotly            │
│  Mobile Responsive | 4 Pages | Interactive Charts           │
└─────────────────────────────────────────────────────────────┘
                               ⇅
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  Flask Framework | Python 3.8+ | REST API | 3 Endpoints    │
│  Request Handling | Response Processing | Business Logic    │
└─────────────────────────────────────────────────────────────┘
                               ⇅
┌─────────────────────────────────────────────────────────────┐
│                   MACHINE LEARNING LAYER                     │
│  Scikit-learn | XGBoost | Pandas | NumPy                    │
│  Random Forest | Feature Scaling | Model Prediction         │
└─────────────────────────────────────────────────────────────┘
                               ⇅
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  SQLite Database | CSV Files | Models (.pkl) | Scalers      │
│  Persistent Storage | Configuration | Caching               │
└─────────────────────────────────────────────────────────────┘
```

---

## Scalability Path

```
Current (Single Instance)
├─ Flask dev server
├─ SQLite database
├─ Single machine
└─ 1-10 concurrent users

Phase 1 (Horizontal)
├─ Load balancer (LB)
├─ 2-4 Flask instances
├─ SQLite → PostgreSQL
└─ 10-100 concurrent users

Phase 2 (Advanced)
├─ Redis caching layer
├─ Database connection pooling
├─ Static file CDN
├─ Monitoring & logging
└─ 100-1000+ concurrent users

Phase 3 (Enterprise)
├─ Kubernetes orchestration
├─ Microservices architecture
├─ Advanced ML pipeline
├─ Real-time data feeds
└─ 10,000+ concurrent users
```

---

## Security Architecture

```
┌────────────────────────────────────┐
│      User / Public Internet        │
└────────────────┬───────────────────┘
                 │
        ┌────────▼────────┐
        │  HTTPS/SSL      │
        │  Encryption     │
        └────────┬────────┘
                 │
    ┌────────────▼──────────────┐
    │  Reverse Proxy (Nginx)    │
    │  Rate Limiting            │
    │  Request Filtering        │
    └────────────┬──────────────┘
                 │
   ┌─────────────▼──────────────┐
   │  Flask Application Layer   │
   │  Input Validation          │
   │  CSRF Protection          │
   │  Authentication (Optional)│
   └─────────────┬──────────────┘
                 │
    ┌────────────▼────────────┐
    │  Database Layer         │
    │  SQL Injection Prevention
    │  Parameterized Queries  │
    └─────────────────────────┘
```

---

## Performance Optimization

```
Optimization Layer Strategy
│
├─ Frontend Optimization
│  ├─ CSS Minification
│  ├─ JS Minification
│  ├─ Image Optimization
│  ├─ Lazy Loading
│  └─ Browser Caching
│
├─ Application Optimization
│  ├─ Response Caching
│  ├─ Connection Pooling
│  ├─ Query Optimization
│  └─ Async Processing
│
├─ Infrastructure Optimization
│  ├─ CDN for static files
│  ├─ Database indexing
│  ├─ Load balancing
│  └─ Server compression
│
└─ Monitoring & Tuning
   ├─ Performance metrics
   ├─ Bottleneck identification
   ├─ Continuous optimization
   └─ A/B testing
```

---

**Architecture Version:** 1.0.0  
**Last Updated:** May 2026  
**Status:** Production-Ready
