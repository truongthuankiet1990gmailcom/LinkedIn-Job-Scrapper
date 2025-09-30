from apify_client import ApifyClient
import json
import pandas as pd
from datetime import datetime, timedelta
import os
import hashlib
import sys

# Fix encoding issues on Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_job_signature(row):
    """Create a unique signature for a job based on multiple fields"""
    # Combine key fields that should be unique for a job
    signature_fields = []
    
    # Add company name (cleaned)
    if pd.notna(row.get('company')):
        signature_fields.append(str(row['company']).strip().lower())
    
    # Add job title (cleaned)
    if pd.notna(row.get('title')):
        signature_fields.append(str(row['title']).strip().lower())
    
    # Add location (cleaned)
    if pd.notna(row.get('location')):
        signature_fields.append(str(row['location']).strip().lower())
    
    # Add employment type if available
    if pd.notna(row.get('employmentType')):
        signature_fields.append(str(row['employmentType']).strip().lower())
    
    # Create hash from combined fields
    combined_string = "|".join(signature_fields)
    return hashlib.md5(combined_string.encode()).hexdigest()

def advanced_duplicate_detection(new_df, existing_df):
    """Advanced duplicate detection using multiple criteria"""
    print("\n[DEDUP] Running advanced duplicate detection...")
    
    # Method 1: Check by jobLink (most reliable)
    link_duplicates = 0
    if 'jobLink' in new_df.columns and 'jobLink' in existing_df.columns:
        new_links = set(new_df['jobLink'].dropna())
        existing_links = set(existing_df['jobLink'].dropna())
        link_duplicates = len(new_links.intersection(existing_links))
        print(f"   [LINKS] Found {link_duplicates} jobs with duplicate links")
    
    # Method 2: Check by job signature (company + title + location)
    print("   [SIGNATURES] Creating job signatures...")
    
    # Add signatures to both dataframes
    new_df_copy = new_df.copy()
    existing_df_copy = existing_df.copy()
    
    new_df_copy['job_signature'] = new_df_copy.apply(create_job_signature, axis=1)
    existing_df_copy['job_signature'] = existing_df_copy.apply(create_job_signature, axis=1)
    
    # Find signature duplicates
    new_signatures = set(new_df_copy['job_signature'])
    existing_signatures = set(existing_df_copy['job_signature'])
    signature_duplicates = len(new_signatures.intersection(existing_signatures))
    print(f"   [SIGNATURES] Found {signature_duplicates} jobs with duplicate signatures")
    
    # Method 3: Combine both dataframes and remove duplicates
    combined_df = pd.concat([existing_df_copy, new_df_copy], ignore_index=True)
    
    # Remove duplicates by jobLink first (most reliable)
    before_link_dedup = len(combined_df)
    if 'jobLink' in combined_df.columns:
        combined_df = combined_df.drop_duplicates(subset=['jobLink'], keep='first')
    after_link_dedup = len(combined_df)
    link_removed = before_link_dedup - after_link_dedup
    
    # Then remove duplicates by signature (for jobs without links or same job reposted)
    before_sig_dedup = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=['job_signature'], keep='first')
    after_sig_dedup = len(combined_df)
    signature_removed = before_sig_dedup - after_sig_dedup
    
    # Remove the temporary signature column
    combined_df = combined_df.drop('job_signature', axis=1)
    
    total_removed = link_removed + signature_removed
    print(f"   [RESULT] Removed {link_removed} link duplicates + {signature_removed} signature duplicates = {total_removed} total")
    
    return combined_df, total_removed

def analyze_duplicate_patterns(df):
    """Analyze patterns in duplicate job postings"""
    print(f"\n[ANALYSIS] Duplicate Analysis:")
    
    if 'postDate' in df.columns:
        try:
            df_copy = df.copy()
            df_copy['postDate'] = pd.to_datetime(df_copy['postDate'])
            
            # Group by company and title to find jobs posted multiple times
            duplicates = df_copy.groupby(['company', 'title']).size().reset_index(name='count')
            duplicates = duplicates[duplicates['count'] > 1].sort_values('count', ascending=False)
            
            if len(duplicates) > 0:
                print(f"   [PATTERNS] Found {len(duplicates)} job titles posted multiple times:")
                for _, row in duplicates.head(5).iterrows():
                    print(f"      • {row['company']}: '{row['title']}' ({row['count']} times)")
            else:
                print(f"   [CLEAN] No duplicate job titles found")
            
            # Check for jobs posted in different date ranges
            if len(df_copy) > 1:
                date_range = df_copy['postDate'].max() - df_copy['postDate'].min()
                print(f"   [DATES] Job posting date range: {date_range.days} days")
            
        except Exception as e:
            print(f"   [WARNING] Could not analyze posting dates: {str(e)}")
    
    # Check for similar job titles
    if 'title' in df.columns:
        title_counts = df['title'].value_counts()
        exact_duplicates = title_counts[title_counts > 1]
        if len(exact_duplicates) > 0:
            print(f"   [TITLES] Jobs with identical titles: {len(exact_duplicates)}")
            for title, count in exact_duplicates.head(3).items():
                print(f"      • '{title}' ({count} times)")

# Initialize the ApifyClient with your API token from environment variable
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API token from environment variable
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')

if not APIFY_API_TOKEN:
    print("[ERROR] APIFY_API_TOKEN environment variable not found!")
    print("[INFO] Please set your Apify API token:")
    print("   1. Create a .env file in your project directory")
    print("   2. Add: APIFY_API_TOKEN=your_actual_api_token_here")
    print("   3. Or set environment variable: set APIFY_API_TOKEN=your_token")
    sys.exit(1)

client = ApifyClient(APIFY_API_TOKEN)

# Define the run input based on LinkedIn Jobs Scraper parameters
run_input = {
    "jobTitle": "Data",
    "location": "VietNam",
    "publishDuration": "r2592000",  # Last month (30 days in seconds)
    "workplaceType": "all",
    "requirePublisherEmail": True,
    "includeCompanyDetails": True,
}

print("[STARTING] LinkedIn job scraping...")
print("Parameters:")
print(f"   Job Title: {run_input['jobTitle']}")
print(f"   Location: {run_input['location']}")
print(f"   Publish Duration: {run_input['publishDuration']}")
print(f"   Workplace Type: {run_input['workplaceType']}")
print(f"   Require Publisher Email: {run_input['requirePublisherEmail']}")
print(f"   Include Company Details: {run_input['includeCompanyDetails']}")

try:
    # Run the Actor with the specified input
    print("\n[RUNNING] LinkedIn scraper...")
    run = client.actor("hjnF35SpLkssCAven").call(run_input=run_input)
    
    print(f"[SUCCESS] Scraping completed! Run ID: {run['id']}")
    print(f"[STATUS] Status: {run['status']}")
    
    # Fetch results from the dataset
    print("\n[DOWNLOADING] Fetching results...")
    items = []
    item_count = 0
    
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        items.append(item)
        item_count += 1
        if item_count % 10 == 0:
            print(f"   Downloaded {item_count} jobs...")
    
    print(f"\n[COMPLETE] Successfully scraped {len(items)} job postings!")
    
    if items:
        # Convert new data to DataFrame
        new_df = pd.DataFrame(items)
        print(f"[DATA] New data collected: {len(new_df)} jobs")
        
        # Define the main dataset filename
        main_dataset = "dataset.csv"
        
        # Check if main dataset exists
        if os.path.exists(main_dataset):
            print(f"[LOADING] Loading existing dataset: {main_dataset}")
            existing_df = pd.read_csv(main_dataset, encoding='utf-8')
            print(f"[DATA] Existing data: {len(existing_df)} jobs")
            
            # Use advanced duplicate detection
            final_df, duplicates_removed = advanced_duplicate_detection(new_df, existing_df)
            
        else:
            print(f"[NEW] No existing dataset found. Creating new {main_dataset}")
            final_df = new_df
            duplicates_removed = 0
        
        # Save the updated dataset
        final_df.to_csv(main_dataset, index=False, encoding='utf-8')
        print(f"[SAVED] Dataset updated: {main_dataset}")
        
        # Create backup with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"dataset_backup_{timestamp}.csv"
        final_df.to_csv(backup_filename, index=False, encoding='utf-8')
        print(f"[BACKUP] Backup created: {backup_filename}")
        
        # Display statistics
        print(f"\n[SUMMARY] Updated Dataset Summary:")
        print(f"   Total Jobs: {len(final_df)}")
        print(f"   New Jobs Scraped: {len(new_df)}")
        print(f"   Duplicates Removed: {duplicates_removed}")
        print(f"   Net New Jobs Added: {len(new_df) - duplicates_removed}")
        print(f"   Columns: {len(final_df.columns)}")
        print(f"   Date Range: {final_df['postDate'].min() if 'postDate' in final_df.columns else 'N/A'} to {final_df['postDate'].max() if 'postDate' in final_df.columns else 'N/A'}")
        
        if 'company' in final_df.columns:
            print(f"   Unique Companies: {final_df['company'].nunique()}")
            print(f"   Top Companies: {', '.join(final_df['company'].value_counts().head(3).index.tolist())}")
        
        if 'location' in final_df.columns:
            print(f"   Unique Locations: {final_df['location'].nunique()}")
        
        # Save a sample of the new data as JSON for inspection
        sample_filename = f"new_jobs_sample_{timestamp}.json"
        with open(sample_filename, 'w', encoding='utf-8') as f:
            json.dump(items[:5], f, indent=2, ensure_ascii=False)
        print(f"[SAMPLE] New data sample saved to: {sample_filename}")
        
        # Print column names for reference
        print(f"\n[COLUMNS] Available Columns:")
        for i, col in enumerate(final_df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        # Analyze duplicate patterns
        analyze_duplicate_patterns(final_df)
        
        print(f"\n[SUCCESS] Dataset updated! Your Streamlit app will automatically use the updated {main_dataset}.")
        
    else:
        print("[WARNING] No data was scraped. Check your search parameters.")
        
except Exception as e:
    print(f"[ERROR] Error occurred: {str(e)}")
    print("[TIPS] Troubleshooting tips:")
    print("   1. Check your API token is valid")
    print("   2. Verify you have sufficient Apify credits")
    print("   3. Try reducing the scope (e.g., specific city instead of country)")
    print("   4. Check if LinkedIn has rate limits")

print("\n[FINISHED] Script completed!")