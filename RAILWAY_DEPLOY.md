# 🚂 Railway Deployment Guide

Railway is another excellent option for deploying your app with a generous free tier.

## Step 1: Prepare Your Repository
1. Upload your code to GitHub (same as Streamlit Cloud process)

## Step 2: Deploy on Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your `linkedin-job-analyzer` repository**

## Step 3: Configure Deployment

Railway will auto-detect it's a Python app. You just need to:

1. **Set the start command:**
   ```
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

2. **Add environment variables (if needed):**
   - No special env vars needed for basic setup

## Step 4: Your App is Live!

Your app will be available at:
```
https://your-app-name.up.railway.app
```

**Railway Benefits:**
- ✅ FREE $5/month credits
- ✅ Automatic HTTPS
- ✅ Custom domains
- ✅ Database support
- ✅ Easy scaling

## Advanced Railway Setup

Create `railway.toml` for custom configuration:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"
```