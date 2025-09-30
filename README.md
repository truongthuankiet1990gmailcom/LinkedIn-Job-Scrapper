# 💼 LinkedIn Job Market Analyzer

> **A comprehensive end-to-end data analytics platform for LinkedIn job market insights with automated data collection, advanced duplicate detection, and interactive visualizations.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## 🚀 Live Demo

**[Deploy Your Own Instance](https://streamlit.io/cloud)** - Follow our deployment guide below

---

## ✨ Features

### 📊 **Interactive Analytics Dashboard**
- **Multi-tab Interface**: Overview, Skills Analysis, Company Insights, Job Trends, and Geographic Analysis
- **Real-time Filtering**: Dynamic filters by company, location, experience level, and employment type
- **Mobile Responsive**: Optimized for desktop, tablet, and mobile viewing
- **Data Export**: Download filtered results and visualizations

### � **Automated Data Collection**
- **One-Click Refresh**: Built-in LinkedIn job scraper with refresh button
- **Smart Duplicate Detection**: Advanced deduplication using job links and content signatures
- **Incremental Updates**: Append new jobs while preserving existing data
- **Backup System**: Automatic timestamped backups before each update

### 🧠 **Advanced NLP Processing**
- **Skill Extraction**: Automated identification of technical skills from job descriptions
- **Job Categorization**: Smart classification of roles (Analyst, Engineer, Scientist, etc.)
- **Requirements Analysis**: Extract education, experience, and certification requirements
- **Benefits Parsing**: Identify and categorize job benefits and perks

### 📈 **Comprehensive Visualizations**
- **Interactive Charts**: Plotly-powered visualizations with hover details and zoom
- **Geographic Maps**: Job distribution across cities and regions
- **Time Series**: Posting trends and seasonal patterns
- **Correlation Analysis**: Skill combinations and salary relationships

---

## 🚦 Quick Start

### Option 1: Run Locally (5 minutes)

```bash
# Clone the repository
git clone https://github.com/your-username/LinkedIn-Job-Scrapper.git
cd LinkedIn-Job-Scrapper

# Install dependencies
pip install -r requirements.txt

# Configure API token (for data refresh feature)
cp .env.example .env
# Edit .env file and add your Apify API token

# Run the application
streamlit run app.py

# Open browser to http://localhost:8501
```

### Option 2: Deploy on Streamlit Cloud (FREE)

1. **Fork this repository** to your GitHub account
2. **Visit [Streamlit Cloud](https://share.streamlit.io)**
3. **Connect your GitHub** and select this repository
4. **Configure secrets** in Streamlit Cloud settings:
   ```toml
   APIFY_API_TOKEN = "your_actual_api_token_here"
   ```
5. **Deploy with one click** - automatic dependency installation
6. **Share your live URL** with anyone!

📖 **Detailed setup guide**: See `SECURITY_SETUP.md` for API token configuration

---

## 🏗️ Project Architecture

```
LinkedIn-Job-Scrapper/
├── 📱 Frontend & Analytics
│   ├── app.py                    # Main Streamlit dashboard
│   ├── .streamlit/config.toml   # App configuration
│   └── requirements.txt         # Python dependencies
├── 🔄 Data Pipeline
│   ├── refresh_data.py          # LinkedIn scraper with deduplication
│   ├── dataset.csv             # Main job dataset
│   └── dataset_backup_*.csv    # Automatic backups
├── � Security & Configuration
│   ├── .env.example            # Environment variables template
│   ├── .env                    # Local environment variables (not in git)
│   ├── .gitignore              # Git ignore patterns
│   └── SECURITY_SETUP.md       # Security configuration guide
├── �🚀 Deployment
│   ├── Dockerfile              # Container configuration
│   ├── Procfile               # Process configuration
│   ├── runtime.txt            # Python version
│   └── packages.txt           # System dependencies
├── 📊 Analysis
│   └── test.ipynb             # Jupyter notebook for EDA
└── 📚 Documentation
    ├── README.md               # Main documentation
    └── STREAMLIT_CLOUD_DEPLOY.md
```

---

## 🎯 Key Analytics & Insights

### 💡 **Skills Intelligence**
- **Most In-Demand**: Python (46.7%), SQL (46.7%), R (98.3%)
- **Emerging Technologies**: Machine Learning, TensorFlow, AI/ChatGPT
- **Visualization Tools**: Power BI, Tableau, Excel mastery
- **Cloud Platforms**: AWS, Azure, Google Cloud expertise

### 🌍 **Market Trends**
- **Geographic Hotspots**: Ho Chi Minh City (70%), Hanoi, Da Nang
- **Role Distribution**: Data Analyst (28%), Data Engineer (12%), Data Scientist (12%)
- **Experience Demand**: 5+ years most sought after
- **Employment Types**: Full-time (85%), Contract (10%), Remote (5%)

### 🏢 **Company Insights**
- **Top Employers**: Google, Microsoft, Procter & Gamble, HEINEKEN
- **Hiring Patterns**: Tech companies hiring 40% more data roles
- **Benefits Trends**: Professional development (61.7%), Training programs (31.7%)
- **Growth Sectors**: E-commerce, Fintech, Healthcare Analytics

---

## 🔧 Advanced Features

### 🤖 **Smart Data Collection**
```python
# Automated LinkedIn scraping with configurable parameters
run_input = {
    "jobTitle": "Data",
    "location": "VietNam",
    "publishDuration": "r2592000",  # Last month
    "workplaceType": "all",
    "requirePublisherEmail": True,
    "includeCompanyDetails": True
}
```

### 🔍 **Duplicate Detection System**
- **Multi-level Detection**: Job links + content signatures
- **Smart Matching**: Company + Title + Location + Employment Type
- **Pattern Analysis**: Identifies companies posting duplicate jobs
- **Preservation**: Keeps oldest posting, removes recent duplicates

### 📊 **Performance Optimization**
- **Data Caching**: Streamlit caching for sub-second load times
- **Efficient Processing**: Pandas optimizations for large datasets
- **Memory Management**: Handles 10k+ job records efficiently
- **Progressive Loading**: Lazy loading for better UX

---

## 🎯 Use Cases

### 👩‍💻 **For Job Seekers**
- **Skill Gap Analysis**: Identify missing skills for target roles
- **Salary Benchmarking**: Understand compensation ranges
- **Geographic Strategy**: Find best locations for opportunities
- **Career Progression**: Map skill evolution paths
- **Company Research**: Deep dive into potential employers

### 🏢 **For Employers & Recruiters**
- **Market Intelligence**: Understand competitor hiring patterns
- **Talent Scarcity**: Identify hard-to-fill skill areas
- **Compensation Analysis**: Benchmark salary offerings
- **Job Posting Optimization**: Improve posting effectiveness
- **Talent Pipeline**: Plan future hiring strategies

### 🎓 **For Researchers & Analysts**
- **Labor Market Research**: Analyze employment trends
- **Skills Evolution**: Track technology adoption rates
- **Economic Indicators**: Job market health metrics
- **Policy Impact**: Measure workforce development effects
- **Academic Studies**: Support research with real job data

---

## 🛠️ Customization Guide

### Adding New Skills to Track
```python
# In app.py, modify the skills extraction
technical_skills = [
    'python', 'sql', 'r', 'java', 'scala',
    'tensorflow', 'pytorch', 'scikit-learn',
    'your-custom-skill'  # Add here
]
```

### Custom Job Categories
```python
def categorize_job_role(title):
    title_lower = title.lower()
    if any(word in title_lower for word in ['analyst', 'analysis']):
        return 'Data Analyst'
    elif 'your-keyword' in title_lower:
        return 'Your Custom Category'
```

### Styling Customization
```css
/* Modify the CSS in app.py */
.main-header {
    color: #your-brand-color;
    font-family: 'Your-Font';
}
```

---

## 📋 Data Requirements

### Required CSV Columns
| Column | Description | Example |
|--------|-------------|---------|
| `company` | Company name | "Google", "Microsoft" |
| `title` | Job title | "Data Analyst", "Senior Data Engineer" |
| `location` | Job location | "Ho Chi Minh City", "Remote" |
| `description` | Full job description | Text with requirements & benefits |
| `employmentType` | Employment type | "Full-time", "Part-time", "Contract" |
| `experienceLevel` | Experience required | "Entry level", "Mid-Senior level" |
| `postDate` | Posting date | "2025-09-30" |
| `jobLink` | LinkedIn job URL | Full LinkedIn job posting URL |

### Optional Columns
- `salary` - Compensation information
- `workplaceType` - Remote/Hybrid/On-site
- `industry` - Company industry
- `companyDetails` - Additional company info

---

## 🚀 Deployment Options

| Platform | Cost | Setup Time | Performance | Best For |
|----------|------|------------|-------------|----------|
| **Streamlit Cloud** | FREE | 5 min | Good | Demos, MVPs |
| **Railway** | FREE tier | 10 min | Excellent | Production apps |
| **Render** | FREE tier | 10 min | Very Good | Reliable hosting |
| **Heroku** | $7/month | 15 min | Good | Enterprise |
| **Docker + VPS** | $5+/month | 30 min | Excellent | Custom setups |

### 🐳 Docker Deployment
```bash
# Build and run with Docker
docker build -t linkedin-analyzer .
docker run -p 8501:8501 linkedin-analyzer
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

**🐛 App Won't Start**
```bash
# Update dependencies
pip install --upgrade streamlit pandas plotly numpy

# Check Python version (3.8+ required)
python --version

# Run with verbose output
streamlit run app.py --logger.level debug
```

**📊 Data Not Loading**
- ✅ Use the built-in file upload feature
- ✅ Check CSV format and required columns
- ✅ Ensure file size < 200MB
- ✅ Verify UTF-8 encoding

**🔄 Refresh Button Not Working**
- ✅ Check Apify API token configuration (see SECURITY_SETUP.md)
- ✅ Ensure APIFY_API_TOKEN environment variable is set
- ✅ Verify internet connection
- ✅ Check Apify account credits
- ✅ Review console output for errors

**🐌 Performance Issues**
```python
# Optimize for large datasets
@st.cache_data
def load_large_dataset(file_path):
    return pd.read_csv(file_path, nrows=5000)  # Limit rows
```

**🎨 Unicode/Encoding Errors**
- Fixed in refresh_data.py with Windows encoding handling
- All emoji characters replaced with text tags
- UTF-8 encoding enforced

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/LinkedIn-Job-Scrapper.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and test
streamlit run app.py

# Submit a pull request
```

### Contribution Areas
- 🔍 **New Analytics**: Additional visualizations and insights
- 🛠️ **Data Sources**: Integration with other job platforms
- 🎨 **UI/UX**: Interface improvements and mobile optimization
- 🔧 **Performance**: Speed and memory optimizations
- 📚 **Documentation**: Tutorials and guides
- 🧪 **Testing**: Unit tests and integration tests

---

## 📄 License

```
MIT License

Copyright (c) 2025 LinkedIn Job Market Analyzer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

---

## 🙏 Acknowledgments

- **Streamlit Team** - Amazing framework for data apps
- **Plotly** - Interactive visualization library
- **Apify** - LinkedIn scraping infrastructure
- **Pandas Team** - Data manipulation excellence
- **Open Source Community** - Inspiration and best practices

---

## 📞 Support & Contact

- 📖 **Documentation**: Check troubleshooting section above
- 🐛 **Bug Reports**: [Open a GitHub Issue](https://github.com/your-username/LinkedIn-Job-Scrapper/issues)
- � **Feature Requests**: [GitHub Discussions](https://github.com/your-username/LinkedIn-Job-Scrapper/discussions)
- ⭐ **Show Support**: Star this repository if you find it helpful!

---

<div align="center">

**🚀 Built with ❤️ using Streamlit, Plotly, and Modern Data Science Stack**

*Transform your job market data into actionable insights with just one click!*

[![GitHub stars](https://img.shields.io/github/stars/your-username/LinkedIn-Job-Scrapper.svg?style=social&label=Star)](https://github.com/your-username/LinkedIn-Job-Scrapper)
[![GitHub forks](https://img.shields.io/github/forks/your-username/LinkedIn-Job-Scrapper.svg?style=social&label=Fork)](https://github.com/your-username/LinkedIn-Job-Scrapper/fork)

</div>