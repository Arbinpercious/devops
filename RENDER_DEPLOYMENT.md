# Render Deployment Guide

## Steps to Deploy on Render

### 1. Push to GitHub
First, make sure your code is pushed to a GitHub repository:
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### 3. Deploy to Render
1. Click **"New+"** button in Render dashboard
2. Select **"Web Service"**
3. Choose your GitHub repository containing this code
4. Fill in the service details:
   - **Name**: `bus-booking-system` (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Plan**: Free (or Starter for better performance)

### 4. Environment Variables (Optional)
Add any environment variables needed in Render dashboard:
- `PYTHON_VERSION`: 3.11

### 5. Deploy
Click **"Create Web Service"** and Render will:
- Clone your repository
- Install dependencies from `requirements.txt`
- Start the application with gunicorn

### 6. Access Your Application
After deployment completes, you'll get a URL like:
```
https://bus-booking-system.onrender.com
```

### 7. API Endpoints
- **GET** `/` - API information
- **GET** `/api/buses` - List all buses
- **POST** `/api/book` - Book a seat
- **GET** `/health` - Health check

## Example API Usage

```bash
# Get available buses
curl https://your-app.onrender.com/api/buses

# Book a seat
curl -X POST https://your-app.onrender.com/api/book \
  -H "Content-Type: application/json" \
  -d '{
    "bus_id": "B001",
    "seat": 1,
    "passenger_name": "John Doe"
  }'
```

## Configuration Files Added

- **Procfile** - Defines how to run the application
- **render.yaml** - Render infrastructure configuration
- **wsgi.py** - Flask web application entry point
- **requirements.txt** - Updated with Flask and gunicorn

## Notes

- The application runs on port 10000
- Free tier includes: 750 hours/month of compute
- Auto-deploy from GitHub: any push to main branch triggers redeploy
- Render will keep the app running 24/7 (within free tier limits)
