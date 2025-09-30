# 🚀 Streamlit Cloud Deployment Guide

## Step 1: Prepare Your Code for GitHub

### Create a GitHub Repository
1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name it: `linkedin-job-analyzer`
4. Make it **Public** (required for free tier)
5. Don't initialize with README (we have our own files)

### Upload Your Files
You can either:

**Option A: Use GitHub Web Interface**
1. Click "uploading an existing file"
2. Drag and drop all files from your `d:\LinkedIn Job Scrapper` folder
3. **Important files to upload:**
   - `app.py`
   - `requirements.txt`
   - `dataset_fast-linkedin-jobs-scraper_2025-09-30_04-48-34-346.csv`
   - `.streamlit/config.toml`
   - `README.md`

**Option B: Use Git Commands (if you have Git installed)**
```bash
cd "d:\LinkedIn Job Scrapper"
git init
git add .
git commit -m "Initial commit - LinkedIn Job Analyzer"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/linkedin-job-analyzer.git
git push -u origin main
```

## Step 2: Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub account**
3. **Click "New app"**
4. **Fill in the details:**
   - Repository: `YOUR_USERNAME/linkedin-job-analyzer`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click "Deploy!"**

## Step 3: Your App is Live! 🎉

Your app will be available at:
```
https://YOUR_USERNAME-linkedin-job-analyzer-app-[random].streamlit.app
```

**Features:**
- ✅ FREE hosting
- ✅ Automatic updates when you push to GitHub
- ✅ Custom domain option
- ✅ HTTPS included
- ✅ Built-in analytics

## Troubleshooting

### If deployment fails:
1. **Check requirements.txt** - ensure all packages are listed
2. **File size limits** - CSV should be under 200MB
3. **Memory limits** - Streamlit Cloud has 1GB RAM limit

### If app crashes:
1. Check logs in Streamlit Cloud dashboard
2. Reduce dataset size if needed
3. Add error handling for missing data

## Pro Tips

1. **Custom URL:** You can request a custom subdomain
2. **Private repos:** Upgrade to Streamlit Cloud for Teams
3. **Monitoring:** Use built-in metrics dashboard
4. **Updates:** Just push to GitHub and app auto-updates!