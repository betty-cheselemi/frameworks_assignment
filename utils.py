"""
Utility functions for CORD-19 dataset analysis
"""
import pandas as pd
import os
import subprocess
import sys

def download_dataset():
    """
    Download CORD-19 metadata.csv if it doesn't exist
    """
    if not os.path.exists('metadata.csv'):
        print("Downloading CORD-19 metadata... This may take a few minutes.")
        try:
            # Run the download script
            result = subprocess.run([sys.executable, 'download_metadata.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("Dataset downloaded successfully")
                return True
            else:
                print(f"Download failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error running download script: {e}")
            return False
    else:
        print("metadata.csv already exists, skipping download")
        return True

def load_and_clean_data():
    """
    Load and clean the CORD-19 metadata
    """
    # Ensure dataset is downloaded
    if not download_dataset():
        return None
    
    # Load the data
    df = pd.read_csv('metadata.csv', low_memory=False)
    
    # Drop rows with missing title or publish_time
    original_size = len(df)
    df = df.dropna(subset=['title', 'publish_time'])
    print(f"Dropped {original_size - len(df)} rows with missing title or publish_time")
    
    # Convert publish_time to datetime
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df = df.dropna(subset=['publish_time'])
    
    # Extract year
    df['year'] = df['publish_time'].dt.year
    
    # Add abstract word count
    df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))
    
    print(f"Final dataset shape: {df.shape}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    
    return df