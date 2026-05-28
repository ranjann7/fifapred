#!/usr/bin/env python
"""
FIFA 2026 AI Predictor - Development Server Launcher
Usage: python run.py
"""

import os
import sys
from app import app, load_teams_data, load_model

if __name__ == '__main__':
    # Check if running in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    # Load data and model
    print("Loading teams data...")
    load_teams_data()
    
    print("Loading ML model...")
    load_model()
    
    print("Starting FIFA 2026 AI Predictor...")
    print("=" * 50)
    print("⚽ FIFA 2026 AI PREDICTOR")
    print("=" * 50)
    print("🌐 Access at: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("🎯 Predict: http://localhost:5000/predict")
    print("🏆 Tournament: http://localhost:5000/tournament")
    print("=" * 50)
    
    if is_production:
        print("⚠️  Running in PRODUCTION mode")
        # In production, use Gunicorn or similar
        # gunicorn app:app
    else:
        print("🔧 Running in DEVELOPMENT mode (debug=True)")
    
    # Run the app
    app.run(debug=not is_production, port=5000, host='0.0.0.0')
