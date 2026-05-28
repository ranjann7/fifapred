# SETUP GUIDE - FIFA 2026 AI Predictor

## Quick Start (5 minutes)

### Step 1: Clone/Extract Repository
```bash
cd fifa
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Train ML Model
```bash
python model/train_model.py
```

This will:
- Generate 500 sample training matches
- Train Random Forest classifier
- Save model to `model/predictor.pkl`
- Save scaler to `model/scaler.pkl`
- Print accuracy metrics

### Step 6: Initialize Database (Optional)
```bash
python database.py
```

### Step 7: Run Application
```bash
python app.py
```

### Step 8: Open in Browser
Visit: `http://localhost:5000`

---

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Port 5000 Already in Use
**Solution:** Edit `app.py` and change:
```python
app.run(debug=True, port=5001)  # Change to 5001 or any free port
```

### Issue: Model Files Not Found
**Solution:** Retrain the model:
```bash
python model/train_model.py
```

### Issue: Permission Denied (macOS/Linux)
**Solution:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

---

## Project Features Walkthrough

### 1. Home Page (/)
- Project overview
- Feature highlights
- 2026 World Cup facts
- Tech stack info

**URL:** http://localhost:5000/

### 2. Match Prediction (/predict)
- Select two teams
- Get AI predictions
- View win probabilities
- See predicted score

**How to use:**
1. Click "🎯 Predict Match"
2. Select Team 1 (e.g., Argentina)
3. Select Team 2 (e.g., France)
4. Click "🔮 PREDICT MATCH"
5. View results with probabilities

### 3. Analytics Dashboard (/dashboard)
- Top 5 teams ranking
- Team statistics
- Interactive charts
- Model performance metrics

**Explore:**
- Team strength comparison
- Attack vs Defense ratings
- Training accuracy: 78.5%
- Test accuracy: 75.2%

### 4. Tournament Simulator (/tournament)
- Simulate 2026 World Cup
- Get semi-finals predictions
- View finals matchup
- Predict tournament champion

**How to use:**
1. Click "🏆 Tournament Simulator"
2. View tournament structure (48 teams)
3. Click "🎲 SIMULATE TOURNAMENT"
4. See champion prediction with confidence

---

## API Endpoints

### Get Teams
```
GET /api/teams
Response: JSON with all teams and stats
```

### Predict Match
```
POST /api/predict
Body: {"team1": "Argentina", "team2": "France"}
Response: Prediction with probabilities
```

### Simulate Tournament
```
POST /api/tournament-simulate
Response: Tournament bracket and winner prediction
```

---

## File Structure

```
fifa/
├── app.py ........................ Flask main application
├── config.py ..................... Configuration settings
├── database.py ................... Database initialization
├── requirements.txt .............. Python dependencies
├── Procfile ....................... Deployment config
├── README.md ...................... Full documentation
├── .gitignore ..................... Git ignore rules
│
├── static/
│   ├── css/
│   │   └── style.css ............. Main stylesheet (dark theme)
│   ├── js/
│   │   └── script.js ............. Frontend JavaScript
│   └── images/
│
├── templates/
│   ├── index.html ................ Home page
│   ├── predict.html .............. Prediction interface
│   ├── dashboard.html ............ Analytics dashboard
│   └── tournament.html ........... Tournament simulator
│
├── model/
│   └── train_model.py ............ ML training pipeline
│
└── dataset/
    ├── matches.csv ............... Historical match data
    └── fifa_rankings.csv ......... Team rankings
```

---

## ML Model Details

### Training Process
1. **Generate Data:** Creates 500 synthetic match samples
2. **Feature Engineering:** Extracts 8 important features
3. **Scaling:** Standardizes features for better training
4. **Model Training:** Random Forest with 100 trees
5. **Evaluation:** Cross-validation with test set
6. **Persistence:** Saves model with joblib

### Model Parameters
- Estimators: 100
- Max Depth: 10
- Test Size: 20%
- Random State: 42

### Prediction Flow
```
User Input (2 teams)
    ↓
Get Team Stats (FIFA ranking, attack, defense)
    ↓
Create Feature Vector
    ↓
Scale Features
    ↓
Feed to Trained Model
    ↓
Get Prediction & Probabilities
    ↓
Display Results
```

---

## Tips & Tricks

### 1. Add Custom Teams
Edit `app.py` and add to `teams_data`:
```python
'Germany': {'fifa_rank': 15, 'attack': 82, 'defense': 76},
```

### 2. Improve Model Accuracy
- Add more training data in `train_model.py`
- Adjust feature engineering
- Try XGBoost (uncommented in requirements.txt)
- Hyperparameter tuning

### 3. Dark Mode Theme
Already implemented! The entire UI uses:
- Dark background (#1a1a2e)
- Neon green accents (#00ff41)
- Professional card layouts

### 4. Interactive Charts
- Dashboard uses Plotly for interactive visualization
- Charts auto-scale based on data
- Add more metrics as needed

---

## Deployment Options

### Option 1: Render.com
1. Push to GitHub
2. Connect Render to GitHub repo
3. Add Python runtime
4. Deploy automatically

### Option 2: Railway.app
1. Connect GitHub account
2. Select repository
3. Configure Python version
4. Connect database (if needed)
5. Deploy!

### Option 3: Heroku (Legacy)
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Option 4: Local Server
```bash
python app.py
# Accessible at http://localhost:5000
```

---

## Performance Optimization

### For Production:
1. Replace Flask dev server with Gunicorn:
```bash
pip install gunicorn
gunicorn app:app
```

2. Add caching:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

3. Database optimization using connection pooling

4. CDN for static files

5. API rate limiting

---

## Security Considerations

### Before Production Deployment:
1. ✅ Change SECRET_KEY in `config.py`
2. ✅ Set DEBUG = False
3. ✅ Use environment variables for secrets
4. ✅ Add CORS if cross-domain requests needed
5. ✅ Implement authentication/authorization
6. ✅ Add input validation and sanitization
7. ✅ Use HTTPS in production
8. ✅ Set up database backups

---

## Contact & Support

### Common Issues:
- **Can't run venv:** Use `python -m venv venv` instead of `virtualenv`
- **Port in use:** Change port in `app.py`
- **Slow predictions:** Retrain model with larger dataset
- **Missing dependencies:** Run `pip install -r requirements.txt`

### Performance Tips:
- Model loads on startup (first request may be slower)
- Cache predictions for frequently selected teams
- Use async tasks for long-running operations

---

## Next Steps

After getting familiar with the project:

1. ✅ Add more teams
2. ✅ Improve ML model accuracy
3. ✅ Add live API integration
4. ✅ Implement user authentication
5. ✅ Add prediction history
6. ✅ Create mobile app
7. ✅ Deploy to cloud
8. ✅ Set up CI/CD pipeline

---

## Learning Resources

### Flask
- Official: flask.palletsprojects.com
- Miguel Grinberg's tutorials

### ML with Scikit-learn
- Official: scikit-learn.org
- Kaggle courses

### Frontend Development
- MDN Web Docs
- JavaScript.info

### Data Science
- Kaggle competitions
- Coursera ML courses

---

## Version Info

- **Project Version:** 1.0.0
- **Python:** 3.8+
- **Flask:** 2.3.3
- **Scikit-learn:** 1.3.0
- **Last Updated:** May 2026

---

## Success Checklist

- ✅ Python 3.8+ installed
- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ ML model trained
- ✅ Flask running on port 5000
- ✅ Predictions working
- ✅ Dashboard displaying data
- ✅ Tournament simulator functional

**Ready to deploy!** 🚀

---

For detailed documentation, see `README.md`
