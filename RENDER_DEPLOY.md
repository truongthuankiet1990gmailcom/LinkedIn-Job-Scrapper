# 🎨 Render Deployment Guide

Render offers a reliable free tier for web applications.

## Step 1: Upload to GitHub
Same process as other platforms - get your code on GitHub first.

## Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New Web Service"**
4. **Connect your GitHub repository**

## Step 3: Configure Service

**Settings to configure:**
- **Name:** `linkedin-job-analyzer`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

## Step 4: Advanced Configuration

Create `render.yaml` for infrastructure as code:
```yaml
services:
  - type: web
    name: linkedin-job-analyzer
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true"
    plan: free
```

**Render Benefits:**
- ✅ 750 hours/month free
- ✅ Automatic deploys
- ✅ Custom domains
- ✅ SSL certificates
- ✅ Database integration