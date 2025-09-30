import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from collections import Counter
from datetime import datetime, timedelta
import io
import subprocess
import sys
import os

# Configure page
st.set_page_config(
    page_title="LinkedIn Job Market Analyzer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #0077B5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E86AB;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #0077B5;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0077B5;
        margin: 1rem 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #0077B5;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class JobAnalyzer:
    def __init__(self, df):
        self.df = df
        self.extracted_data = None
        self.skill_counts = None
        self.benefit_counts = None
        self.process_data()
    
    def extract_skills_and_requirements(self, description):
        """Extract skills, requirements, and benefits from job description"""
        if pd.isna(description) or not description:
            return {"skills": [], "experience": [], "degree": [], "benefits": []}
        
        desc_lower = description.lower()
        
        # Programming languages and technical skills
        programming_skills = [
            'python', 'java', 'javascript', 'sql', 'r', 'scala', 'c++', 'c#', 
            'go', 'kotlin', 'swift', 'php', 'ruby', 'matlab', 'sas', 'stata'
        ]
        
        # Data science and analytics tools
        data_tools = [
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
            'tableau', 'power bi', 'powerbi', 'looker', 'qlik', 'spotfire',
            'excel', 'spark', 'hadoop', 'kafka', 'airflow', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'google cloud', 'bigquery', 'snowflake', 'redshift'
        ]
        
        # Machine learning concepts
        ml_concepts = [
            'machine learning', 'deep learning', 'neural networks', 'nlp', 
            'computer vision', 'time series', 'forecasting', 'optimization',
            'statistics', 'statistical modeling', 'data mining', 'analytics'
        ]
        
        # Experience patterns
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\s*to\s*(\d+)\s*years?\s*experience',
            r'minimum\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?'
        ]
        
        # Degree patterns
        degree_patterns = [
            r"bachelor'?s?\s*(?:degree)?",
            r"master'?s?\s*(?:degree)?",
            r"phd", r"doctorate",
            r"undergraduate", r"graduate"
        ]
        
        # Benefits keywords
        benefit_keywords = [
            'salary', 'bonus', 'insurance', 'health', 'dental', 'vision',
            'retirement', '401k', 'vacation', 'pto', 'remote', 'flexible',
            'training', 'development', 'career growth', 'promotion'
        ]
        
        # Extract skills
        found_skills = []
        for skill in programming_skills + data_tools + ml_concepts:
            if skill in desc_lower:
                found_skills.append(skill)
        
        # Extract experience
        experience_reqs = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, desc_lower)
            for match in matches:
                if isinstance(match, tuple):
                    experience_reqs.append(f"{match[0]}-{match[1]} years")
                else:
                    experience_reqs.append(f"{match}+ years")
        
        # Extract degrees
        degree_reqs = []
        for pattern in degree_patterns:
            if re.search(pattern, desc_lower):
                degree_reqs.append(re.search(pattern, desc_lower).group())
        
        # Extract benefits
        found_benefits = []
        for benefit in benefit_keywords:
            if benefit in desc_lower:
                found_benefits.append(benefit)
        
        return {
            "skills": found_skills,
            "experience": experience_reqs,
            "degree": degree_reqs,
            "benefits": found_benefits
        }
    
    def categorize_job_role(self, title):
        """Categorize job titles into broader role types"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['data scientist', 'scientist']):
            return 'Data Scientist'
        elif any(word in title_lower for word in ['data engineer', 'engineer']):
            return 'Data Engineer'
        elif any(word in title_lower for word in ['analyst', 'analytics']):
            return 'Data Analyst'
        elif any(word in title_lower for word in ['manager', 'lead', 'head']):
            return 'Management/Leadership'
        elif any(word in title_lower for word in ['intern', 'internship']):
            return 'Internship'
        elif any(word in title_lower for word in ['research', 'researcher']):
            return 'Research'
        else:
            return 'Other'
    
    def process_data(self):
        """Process the dataframe and extract insights"""
        # Convert date column
        self.df['postDate'] = pd.to_datetime(self.df['postDate'])
        
        # Extract structured information
        self.extracted_data = self.df['description'].apply(self.extract_skills_and_requirements)
        
        # Categorize jobs
        self.df['job_category'] = self.df['title'].apply(self.categorize_job_role)
        
        # Extract skills and benefits
        all_skills = []
        all_benefits = []
        
        for data in self.extracted_data:
            all_skills.extend(data['skills'])
            all_benefits.extend(data['benefits'])
        
        self.skill_counts = Counter(all_skills)
        self.benefit_counts = Counter(all_benefits)

@st.cache_data
def load_data():
    """Load and cache the dataset"""
    try:
        # Try multiple possible file names
        possible_files = [
            'dataset.csv',
        ]
        
        for filename in possible_files:
            try:
                df = pd.read_csv(filename)
                st.success(f"✅ Dataset loaded successfully: {filename}")
                return df
            except FileNotFoundError:
                continue
        
        # If no file found, show file upload option
        st.error("📁 Dataset file not found. Please upload your job data CSV file:")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
            return df
        
        return None
        
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        return None

def refresh_data():
    """Refresh the dataset by running the scraper"""
    try:
        with st.spinner("🔄 Scraping new LinkedIn job data... This may take a few minutes."):
            # Run the refresh_data.py script
            result = subprocess.run([sys.executable, "refresh_data.py"], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                st.success("✅ Data refresh completed successfully!")
                st.info("📊 New jobs have been added to your dataset. Please refresh the page to see the updated data.")
                # Clear cache to reload data
                st.cache_data.clear()
                return True
            else:
                st.error(f"❌ Error during data refresh: {result.stderr}")
                return False
                
    except Exception as e:
        st.error(f"❌ Error running data refresh: {str(e)}")
        return False

def main():
    # Header
    st.markdown('<h1 class="main-header">💼 LinkedIn Job Market Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Data-Driven Insights for Job Seekers and Employers")
    
    # Sidebar for data management
    with st.sidebar:
        st.header("🔄 Data Management")
        
        # Data refresh section
        st.subheader("Refresh Dataset")
        st.write("Click below to scrape new LinkedIn job data and append it to your existing dataset.")
        
        if st.button("🔄 Refresh Data", type="primary", help="Scrape new jobs from LinkedIn and add to dataset"):
            refresh_data()
        
        st.markdown("---")
        
        # Dataset info in sidebar
        if os.path.exists("dataset.csv"):
            try:
                df_info = pd.read_csv("dataset.csv")
                st.metric("📊 Current Jobs", len(df_info))
                
                if 'postDate' in df_info.columns:
                    try:
                        df_info['postDate'] = pd.to_datetime(df_info['postDate'])
                        latest_date = df_info['postDate'].max().strftime('%Y-%m-%d')
                        st.metric("📅 Latest Job", latest_date)
                    except:
                        pass
            except:
                pass
    
    # Add deployment info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🌐 **Live Demo**: This app analyzes real LinkedIn job data")
    with col2:
        st.info("📊 **Interactive**: Use filters to explore different market segments")
    with col3:
        st.info("🔄 **Real-time**: All charts update automatically based on your selections")
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Display dataset info
    with st.expander("📈 Dataset Information"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Jobs", len(df))
        with col2:
            st.metric("Companies", df['company'].nunique())
        with col3:
            st.metric("Locations", df['location'].nunique())
        with col4:
            if 'postDate' in df.columns:
                try:
                    df['postDate'] = pd.to_datetime(df['postDate'])
                    date_range = (df['postDate'].max() - df['postDate'].min()).days
                    st.metric("Date Range", f"{date_range} days")
                except:
                    st.metric("Date Range", "N/A")
            else:
                st.metric("Columns", len(df.columns))
    
    analyzer = JobAnalyzer(df)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Company filter
    companies = ['All'] + sorted(df['company'].unique().tolist())
    selected_company = st.sidebar.selectbox("Select Company", companies)
    
    # Location filter
    locations = ['All'] + sorted(df['location'].unique().tolist())
    selected_location = st.sidebar.selectbox("Select Location", locations)
    
    # Experience level filter
    exp_levels = ['All'] + sorted(df['experienceLevel'].unique().tolist())
    selected_exp = st.sidebar.selectbox("Select Experience Level", exp_levels)
    
    # Job category filter
    job_categories = ['All'] + sorted(df['job_category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Select Job Category", job_categories)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_company != 'All':
        filtered_df = filtered_df[filtered_df['company'] == selected_company]
    if selected_location != 'All':
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
    if selected_exp != 'All':
        filtered_df = filtered_df[filtered_df['experienceLevel'] == selected_exp]
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['job_category'] == selected_category]
    
    # Overview metrics
    st.markdown('<div class="section-header">📊 Market Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Jobs", len(filtered_df))
    with col2:
        st.metric("Companies", filtered_df['company'].nunique())
    with col3:
        st.metric("Locations", filtered_df['location'].nunique())
    with col4:
        st.metric("Avg Jobs/Day", f"{len(filtered_df) / 30:.1f}")
    
    # Main dashboard
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Market Trends", "🛠️ Skills Analysis", "🏢 Companies & Locations", "💼 Job Categories", "📋 Recommendations"])
    
    with tab1:
        st.markdown('<div class="section-header">📈 Job Market Trends</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Employment type distribution
            emp_dist = filtered_df['employmentType'].value_counts()
            fig_emp = px.pie(values=emp_dist.values, names=emp_dist.index, 
                           title="Employment Type Distribution")
            st.plotly_chart(fig_emp, use_container_width=True)
        
        with col2:
            # Experience level distribution
            exp_dist = filtered_df['experienceLevel'].value_counts()
            fig_exp = px.bar(x=exp_dist.index, y=exp_dist.values, 
                           title="Experience Level Distribution")
            st.plotly_chart(fig_exp, use_container_width=True)
        
        # Posting timeline
        posting_timeline = filtered_df.groupby(filtered_df['postDate'].dt.date).size()
        fig_timeline = px.line(x=posting_timeline.index, y=posting_timeline.values,
                             title="Job Posting Timeline", markers=True)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="section-header">🛠️ Skills Analysis</div>', unsafe_allow_html=True)
        
        # Recalculate skills for filtered data
        filtered_skills = []
        for idx in filtered_df.index:
            if idx < len(analyzer.extracted_data):
                filtered_skills.extend(analyzer.extracted_data.iloc[idx]['skills'])
        
        if filtered_skills:
            skill_counts_filtered = Counter(filtered_skills)
            top_skills = skill_counts_filtered.most_common(15)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top skills bar chart
                skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
                fig_skills = px.bar(skills_df, x='Count', y='Skill', orientation='h',
                                  title="Top 15 Most Demanded Skills",
                                  color='Count', color_continuous_scale='viridis')
                fig_skills.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_skills, use_container_width=True)
            
            with col2:
                # Skills by category
                programming_langs = ['python', 'sql', 'r', 'java', 'javascript', 'scala', 'go']
                viz_tools = ['tableau', 'power bi', 'excel']
                ml_tools = ['tensorflow', 'pytorch', 'scikit-learn', 'machine learning', 'deep learning']
                cloud_tools = ['aws', 'azure', 'gcp', 'google cloud']
                
                skill_categories = {
                    'Programming': sum([skill_counts_filtered.get(skill, 0) for skill in programming_langs]),
                    'Visualization': sum([skill_counts_filtered.get(skill, 0) for skill in viz_tools]),
                    'ML/AI': sum([skill_counts_filtered.get(skill, 0) for skill in ml_tools]),
                    'Cloud': sum([skill_counts_filtered.get(skill, 0) for skill in cloud_tools]),
                    'Analytics': skill_counts_filtered.get('analytics', 0) + skill_counts_filtered.get('statistics', 0)
                }
                
                fig_cat = px.bar(x=list(skill_categories.keys()), y=list(skill_categories.values()),
                               title="Skills by Category")
                st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No skills data available for the selected filters.")
    
    with tab3:
        st.markdown('<div class="section-header">🏢 Companies & Locations</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top companies
            top_companies = filtered_df['company'].value_counts().head(10)
            fig_companies = px.bar(x=top_companies.values, y=top_companies.index, orientation='h',
                                 title="Top 10 Companies by Job Postings")
            fig_companies.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_companies, use_container_width=True)
        
        with col2:
            # Top locations
            top_locations = filtered_df['location'].value_counts().head(10)
            fig_locations = px.bar(x=top_locations.values, y=top_locations.index, orientation='h',
                                 title="Top 10 Locations by Job Postings")
            fig_locations.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_locations, use_container_width=True)
    
    with tab4:
        st.markdown('<div class="section-header">💼 Job Categories Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Job category distribution
            job_dist = filtered_df['job_category'].value_counts()
            fig_jobs = px.pie(values=job_dist.values, names=job_dist.index,
                            title="Job Category Distribution")
            st.plotly_chart(fig_jobs, use_container_width=True)
        
        with col2:
            # Job titles
            top_titles = filtered_df['title'].value_counts().head(10)
            fig_titles = px.bar(x=top_titles.values, y=top_titles.index, orientation='h',
                              title="Top 10 Job Titles")
            fig_titles.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_titles, use_container_width=True)
        
        # Skills by job category
        st.subheader("Skills by Job Category")
        for category in job_dist.index:
            category_jobs = filtered_df[filtered_df['job_category'] == category]
            category_skills = []
            
            for idx in category_jobs.index:
                if idx < len(analyzer.extracted_data):
                    category_skills.extend(analyzer.extracted_data.iloc[idx]['skills'])
            
            if category_skills:
                category_skill_counts = Counter(category_skills)
                top_category_skills = category_skill_counts.most_common(5)
                
                with st.expander(f"{category} ({len(category_jobs)} jobs)"):
                    skills_text = ", ".join([f"{skill} ({count})" for skill, count in top_category_skills])
                    st.write(f"**Top Skills:** {skills_text}")
    
    with tab5:
        st.markdown('<div class="section-header">📋 Insights & Recommendations</div>', unsafe_allow_html=True)
        
        # Key insights
        total_jobs = len(filtered_df)
        
        st.markdown(f"""
        <div class="insight-box">
        <h4>🎯 Key Market Insights</h4>
        <ul>
        <li><strong>Market Size:</strong> {total_jobs} data-related job opportunities analyzed</li>
        <li><strong>Top Location:</strong> {filtered_df['location'].mode().iloc[0] if not filtered_df.empty else 'N/A'}</li>
        <li><strong>Most Hiring Company:</strong> {filtered_df['company'].mode().iloc[0] if not filtered_df.empty else 'N/A'}</li>
        <li><strong>Dominant Role:</strong> {filtered_df['job_category'].mode().iloc[0] if not filtered_df.empty else 'N/A'}</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
            <h4>📚 For Job Seekers</h4>
            <ul>
            <li><strong>Essential Skills:</strong> Focus on R, Python, SQL, and Excel</li>
            <li><strong>High Demand Roles:</strong> Data Analyst positions are most abundant</li>
            <li><strong>Experience Strategy:</strong> 2-5 years experience is most sought after</li>
            <li><strong>Location Focus:</strong> Ho Chi Minh City offers the most opportunities</li>
            <li><strong>Continuous Learning:</strong> Emphasize development and training</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <h4>🏢 For Employers</h4>
            <ul>
            <li><strong>Skill Gaps:</strong> Cloud platforms and advanced ML skills are underrepresented</li>
            <li><strong>Competitive Edge:</strong> Offer development opportunities and flexible work</li>
            <li><strong>Talent Pool:</strong> Focus on HCMC and Hanoi for recruitment</li>
            <li><strong>Benefits Package:</strong> Highlight training, health benefits, and growth opportunities</li>
            <li><strong>Remote Work:</strong> Consider hybrid/remote options to attract talent</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**LinkedIn Job Market Analyzer** | Built with ❤️ using Streamlit")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

if __name__ == "__main__":
    main()