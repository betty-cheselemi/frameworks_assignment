#!/usr/bin/env python3
"""
Download only metadata.csv from CORD-19 dataset on Kaggle

This script downloads the CORD-19 dataset from Kaggle and extracts only the
metadata.csv file to save space (avoiding the full 18GB download).

Requirements:
- Kaggle API credentials (kaggle.json) must be set up
- Install: pip install kaggle

Usage:
    python download_metadata.py
"""

import os
import zipfile
import tempfile
import shutil
from pathlib import Path

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except ImportError:
    print("Error: Kaggle API not installed. Please run: pip install kaggle")
    exit(1)


def download_metadata_only():
    """
    Download only metadata.csv from CORD-19 dataset
    
    This function:
    1. Checks if metadata.csv already exists
    2. Downloads the dataset to a temporary directory
    3. Extracts only metadata.csv
    4. Cleans up temporary files to save space
    """
    
    # Step 1: Check if metadata.csv already exists
    metadata_file = "metadata.csv"
    if os.path.exists(metadata_file):
        print(f"✓ {metadata_file} already exists in current directory")
        print(f"File size: {os.path.getsize(metadata_file) / (1024*1024):.1f} MB")
        return True
    
    print("📥 metadata.csv not found. Starting download from Kaggle...")
    
    # Step 2: Initialize Kaggle API
    try:
        api = KaggleApi()
        api.authenticate()
        print("✓ Kaggle API authenticated successfully")
    except Exception as e:
        print(f"❌ Failed to authenticate with Kaggle API: {e}")
        print("Make sure your kaggle.json credentials are properly configured")
        return False
    
    # Step 3: Create temporary directory for download
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Created temporary directory: {temp_dir}")
        
        try:
            # Step 4: Download dataset to temporary directory
            dataset_name = "allen-institute-for-ai/CORD-19-research-challenge"
            print(f"⬇️  Downloading {dataset_name}...")
            print("   Note: This may take several minutes depending on your connection")
            
            api.dataset_download_files(
                dataset_name, 
                path=temp_dir, 
                unzip=False  # We'll handle extraction manually
            )
            
            # Step 5: Find the downloaded zip file
            zip_files = list(Path(temp_dir).glob("*.zip"))
            if not zip_files:
                print("❌ No zip file found after download")
                return False
            
            zip_path = zip_files[0]
            print(f"✓ Downloaded: {zip_path.name} ({zip_path.stat().st_size / (1024*1024):.1f} MB)")
            
            # Step 6: Extract only metadata.csv from the zip
            print("📂 Extracting metadata.csv from archive...")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # List all files in the zip to find metadata.csv
                file_list = zip_ref.namelist()
                metadata_files = [f for f in file_list if f.endswith('metadata.csv')]
                
                if not metadata_files:
                    print("❌ metadata.csv not found in the downloaded archive")
                    print("Available files:", file_list[:10])  # Show first 10 files
                    return False
                
                # Extract metadata.csv (use the first match if multiple exist)
                metadata_in_zip = metadata_files[0]
                print(f"📄 Found metadata file: {metadata_in_zip}")
                
                # Extract to current directory
                with zip_ref.open(metadata_in_zip) as source:
                    with open(metadata_file, 'wb') as target:
                        shutil.copyfileobj(source, target)
                
                print(f"✓ Extracted {metadata_file} to current directory")
                
            # Step 7: Verify the extracted file
            if os.path.exists(metadata_file):
                file_size_mb = os.path.getsize(metadata_file) / (1024*1024)
                print(f"✅ Success! {metadata_file} downloaded ({file_size_mb:.1f} MB)")
                
                # Show first few lines to verify content
                try:
                    import pandas as pd
                    df = pd.read_csv(metadata_file, nrows=3)
                    print(f"📊 File contains {len(df.columns)} columns")
                    print(f"   Sample columns: {list(df.columns[:5])}")
                except ImportError:
                    print("📊 File appears to be valid CSV format")
                    
                return True
            else:
                print("❌ Failed to extract metadata.csv")
                return False
                
        except Exception as e:
            print(f"❌ Error during download/extraction: {e}")
            return False
    
    # Temporary directory is automatically cleaned up here
    print("🧹 Temporary files cleaned up")


def main():
    """
    Main function to run the metadata download
    """
    print("=" * 60)
    print("CORD-19 Metadata Downloader")
    print("=" * 60)
    print("This script downloads only metadata.csv from the CORD-19 dataset")
    print("to avoid downloading the full 18GB archive.\n")
    
    # Check current directory
    current_dir = os.getcwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Start download process
    success = download_metadata_only()
    
    if success:
        print("\n🎉 Download completed successfully!")
        print("You can now run your analysis scripts.")
    else:
        print("\n💥 Download failed. Please check the error messages above.")
        print("Common issues:")
        print("- Kaggle API credentials not configured")
        print("- Internet connection problems")
        print("- Insufficient disk space")


if __name__ == "__main__":
    main()