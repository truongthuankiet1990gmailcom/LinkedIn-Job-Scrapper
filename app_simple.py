import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# Configure page
st.set_page_config(
    page_title="LinkedIn Job Analyzer",
    page_icon="💼",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0077B5;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load data with file upload option"""
    uploaded_file = st.file_uploader("Upload your LinkedIn job data CSV", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ File uploaded successfully! {len(df)} jobs loaded.")
            return df
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None
    
    # Try to load default dataset
    try:
        df = pd.read_csv('dataset_fast-linkedin-jobs-scraper_2025-09-30_04-48-34-346.csv')
        st.info(f"📊 Using default dataset: {len(df)} jobs")
        return df
    except:
        st.warning("📁 No default dataset found. Please upload a CSV file above.")
        return None

def extract_basic_skills(description):
    """Simple skill extraction"""
    if pd.isna(description):
        return []
    
    desc_lower = str(description).lower()
    skills = ['python', 'sql', 'r', 'excel', 'tableau', 'power bi', 'java', 'javascript', 
              'machine learning', 'data science', 'analytics', 'statistics']
    
    found_skills = [skill for skill in skills if skill in desc_lower]
    return found_skills

def main():
    # Header
    st.markdown('<h1 class="main-header">💼 LinkedIn Job Market Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Simplified Version - Optimized for Streamlit Cloud")
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Basic info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Jobs", len(df))
    with col2:
        st.metric("Companies", df['company'].nunique() if 'company' in df.columns else 'N/A')
    with col3:
        st.metric("Locations", df['location'].nunique() if 'location' in df.columns else 'N/A')
    with col4:
        st.metric("Columns", len(df.columns))
    
    # Show dataset preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head())
    
    # Column analysis
    st.subheader("📊 Column Information")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes,
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum()
    })
    st.dataframe(col_info)
    
    # Basic visualizations if we have the right columns
    if 'company' in df.columns:
        st.subheader("🏢 Top Companies")
        top_companies = df['company'].value_counts().head(10)
        fig = px.bar(x=top_companies.values, y=top_companies.index, orientation='h')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    if 'location' in df.columns:
        st.subheader("📍 Top Locations")
        top_locations = df['location'].value_counts().head(10)
        fig = px.pie(values=top_locations.values, names=top_locations.index)
        st.plotly_chart(fig, use_container_width=True)
    
    if 'title' in df.columns:
        st.subheader("💼 Job Titles")
        top_titles = df['title'].value_counts().head(15)
        fig = px.bar(x=top_titles.values, y=top_titles.index, orientation='h')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Skills analysis if description column exists
    if 'description' in df.columns:
        st.subheader("🛠️ Skills Analysis")
        
        with st.spinner("Analyzing skills..."):
            all_skills = []
            for desc in df['description'].dropna():
                all_skills.extend(extract_basic_skills(desc))
            
            if all_skills:
                skill_counts = Counter(all_skills)
                top_skills = skill_counts.most_common(10)
                
                if top_skills:
                    skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
                    fig = px.bar(skills_df, x='Count', y='Skill', orientation='h')
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show percentages
                    st.write("**Skill Demand Percentages:**")
                    for skill, count in top_skills:
                        percentage = (count / len(df)) * 100
                        st.write(f"• {skill}: {count} jobs ({percentage:.1f}%)")
                else:
                    st.info("No common skills found in the dataset.")
            else:
                st.info("No skills extracted from job descriptions.")
    
    # Data download
    st.subheader("📥 Download Analysis")
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download dataset as CSV",
        data=csv,
        file_name="job_analysis.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("**LinkedIn Job Market Analyzer - Simplified Version**")
    st.markdown("*Built with Streamlit, Pandas, and Plotly*")

if __name__ == "__main__":
    main()