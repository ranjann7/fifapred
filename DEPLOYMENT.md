# 🚀 PROJECT DEPLOYMENT GUIDE

## Pre-Deployment Checklist

### Local Testing ✅
- [ ] Test all 4 pages (Home, Predict, Dashboard, Tournament)
- [ ] Test match predictions with different teams
- [ ] Test tournament simulation
- [ ] Test API endpoints with curl/Postman
- [ ] Check responsive design on mobile
- [ ] Verify dark mode UI looks good
- [ ] Test with 0% CPU usage confirmed

### Configuration ✅
- [ ] Update SECRET_KEY in config.py
- [ ] Set Flask DEBUG = False
- [ ] Update database path if needed
- [ ] Configure logging
- [ ] Set up error tracking
- [ ] Configure email for errors

### Security ✅
- [ ] Change all default passwords
- [ ] Remove debug information
- [ ] Enable HTTPS/SSL
- [ ] Set security headers
- [ ] Implement CORS properly
- [ ] Add rate limiting
- [ ] Validate all inputs

---

## Deployment Options

### Option 1: Render.com (Recommended) ⭐

**Easiest method for beginners**

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/fifa.git
git push -u origin main
```

2. **Connect to Render:**
   - Go to render.com
   - Click "New+" → "Web Service"
   - Connect GitHub (authorize if needed)
   - Select your repository
   - Configure:
     - Name: `fifa-2026-predictor`
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt && python model/train_model.py`
     - Start Command: `gunicorn app:app`
   - Click "Create Web Service"

3. **Set Environment Variables:**
   - Go to Environment in Render dashboard
   - Add: `FLASK_ENV = production`

4. **Deploy:**
   - Automatic on push to main
   - Monitor deployment in Render dashboard
   - Access at: `https://fifa-2026-predictor.onrender.com`

---

### Option 2: Railway.app

**Simple alternative with free tier**

1. **Push to GitHub** (same as above)

2. **Connect to Railway:**
   - Go to railway.app
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Authorize & select repository
   - Click "Deploy"

3. **Configure:**
   - Railway auto-detects Python/Flask
   - Add variables if needed
   - Build & deploy automatic

4. **Custom Domain:**
   - Go to Settings → Domain
   - Add custom domain
   - Update DNS records

---

### Option 3: Heroku (Legacy Alternative)

```bash
# Install Heroku CLI
# (Download from heroku.com)

# Login
heroku login

# Create app
heroku create your-app-name

# Add Procfile (included)
# Git automatically uses it

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

---

### Option 4: Docker + AWS/DigitalOcean

**For advanced deployments**

1. **Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

2. **Build & Push:**
```bash
docker build -t fifa-predictor .
docker tag fifa-predictor your-registry/fifa-predictor:latest
docker push your-registry/fifa-predictor:latest
```

3. **Deploy to Cloud:**
   - AWS ECS
   - DigitalOcean App Platform
   - Google Cloud Run
   - Azure Container Instances

---

## Production Setup

### 1. Install Gunicorn
```bash
pip install gunicorn
```

### 2. Update requirements.txt
Add:
```
gunicorn==21.2.0
```

### 3. Create Production Config
```python
# config.py - Update:
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
```

### 4. Use Environment Variables
```bash
# .env file (don't commit!)
FLASK_ENV=production
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=your-database-url
```

### 5. Run with Gunicorn
```bash
gunicorn app:app --workers 4 --threads 2 --timeout 120
```

---

## Post-Deployment

### Monitoring
1. **Uptime Monitoring:**
   - UptimeRobot
   - Pingdom
   - Freshping

2. **Error Tracking:**
   - Sentry.io
   - Rollbar
   - Bugsnag

3. **Performance Monitoring:**
   - New Relic
   - DataDog
   - Prometheus

### Database
1. **Backup Strategy:**
   - Daily automated backups
   - Keep 30-day history
   - Test restore procedures

2. **Upgrade Path:**
   - SQLite → PostgreSQL for scale
   - Add connection pooling
   - Implement caching (Redis)

### Scaling
1. **Horizontal:**
   - Load balancer (Nginx)
   - Multiple instances
   - Database replication

2. **Vertical:**
   - Upgrade server resources
   - Optimize queries
   - Cache aggressively

---

## SSL/HTTPS Setup

### Automatic (via Render/Railway)
- Both services provide free HTTPS
- Auto-renewable certificates
- Redirect HTTP to HTTPS

### Manual Setup
1. Get certificate (Let's Encrypt)
```bash
certbot certonly --standalone -d yourdomain.com
```

2. Configure Nginx:
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    proxy_pass http://127.0.0.1:5000;
}
```

---

## CI/CD Pipeline

### GitHub Actions (Automated Testing)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python model/train_model.py
      - run: pytest  # Add tests

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: curl ${{ secrets.RENDER_DEPLOY_HOOK }}
```

---

## Testing Before Production

### 1. Functionality Tests
```bash
# Test all pages load
curl http://localhost:5000/
curl http://localhost:5000/predict
curl http://localhost:5000/dashboard
curl http://localhost:5000/tournament

# Test API endpoints
curl http://localhost:5000/api/teams
curl -X POST http://localhost:5000/api/predict \
  -d '{"team1":"Argentina","team2":"France"}' \
  -H "Content-Type: application/json"
```

### 2. Load Testing
```bash
pip install locust

# Create locustfile.py with test scenarios
locust -f locustfile.py --host=http://localhost:5000
```

### 3. Security Testing
```bash
# OWASP ZAP scanning
# SQL injection tests
# XSS vulnerability tests
# CSRF protection verification
```

---

## Domain Setup

### 1. Register Domain
- Namecheap
- GoDaddy
- Google Domains
- Route53 (AWS)

### 2. Configure DNS
For Render:
```
CNAME: www.yourdomain.com → your-app.onrender.com
CNAME: yourdomain.com → your-app.onrender.com
```

For Railway:
```
CNAME: yourdomain.com → railway domain
```

### 3. Email (Optional)
- Mailgun (transactional)
- SendGrid (email marketing)
- Postmark (API emails)

---

## Maintenance

### Regular Tasks
- **Daily:** Check error logs
- **Weekly:** Monitor performance
- **Monthly:** Update dependencies
- **Quarterly:** Security audit

### Updates
```bash
# Check outdated packages
pip list --outdated

# Update safely
pip install --upgrade flask pandas scikit-learn

# Test after updates
python app.py
```

---

## Rollback Plan

### If Deployment Fails
1. **Render/Railway:**
   - Dashboard shows deployment history
   - One-click rollback to previous version

2. **Manual:**
   - Revert last commit
   - Deploy previous version
   - Check logs for errors

### Backup Strategy
- Keep last 5 deployments
- Daily database backups
- Code backups via GitHub

---

## Performance Optimization

### Frontend
- Minify CSS/JS
- Enable GZIP compression
- Use CDN for static files
- Optimize images

### Backend
- Database query optimization
- Cache frequently accessed data
- Use connection pooling
- Implement pagination

### Monitoring
```python
# Add timing logs
import time

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_time(response):
    elapsed = time.time() - g.start_time
    print(f"Request took {elapsed:.2f}s")
    return response
```

---

## Common Issues

### Issue: Model Training Takes Too Long
**Solution:** Reduce sample size or run async task

### Issue: Database Locked
**Solution:** Upgrade to PostgreSQL or implement WAL mode

### Issue: 502 Bad Gateway
**Solution:** Check server logs, increase timeout, more workers

### Issue: Memory Usage High
**Solution:** Implement caching, reduce model size, use Redis

---

## Support & Resources

### Documentation
- Flask: flask.palletsprojects.com
- Render: render.com/docs
- Railway: railway.app/docs

### Community
- Stack Overflow
- GitHub Discussions
- Flask Slack

### Monitoring
- Check deployment logs daily
- Set up alerts for errors
- Monitor response times

---

## Success Checklist

After deployment:
- [ ] Site loads without errors
- [ ] Predictions working
- [ ] Dashboard functional
- [ ] Tournament simulator works
- [ ] Mobile responsive
- [ ] Fast response times
- [ ] HTTPS working
- [ ] Error tracking enabled
- [ ] Backups configured
- [ ] Monitoring active

---

## Performance Targets

- **Page Load:** <2 seconds
- **Prediction API:** <500ms
- **Tournament Sim:** <3 seconds
- **Dashboard:** <1 second
- **Uptime:** >99.5%

---

## Next Steps

1. ✅ Test locally thoroughly
2. ✅ Push to GitHub
3. ✅ Deploy to Render/Railway
4. ✅ Configure domain
5. ✅ Set up monitoring
6. ✅ Monitor for 1 week
7. ✅ Launch officially
8. ✅ Gather feedback

---

**Last Updated:** May 2026  
**Version:** 1.0.0  
**Status:** Ready for Production  

🚀 **Deployment Ready!**
