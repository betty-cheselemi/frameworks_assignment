#!/usr/bin/env python3
"""
Test script to download and verify CORD-19 dataset
"""

from utils import download_dataset, load_and_clean_data

def main():
    print("Testing CORD-19 dataset download and loading...")
    
    # Test dataset download
    if download_dataset():
        print("✓ Dataset download successful")
    else:
        print("✗ Dataset download failed")
        return
    
    # Test data loading and cleaning
    df = load_and_clean_data()
    if df is not None:
        print("✓ Data loading and cleaning successful")
        print(f"✓ Dataset shape: {df.shape}")
        print(f"✓ Year range: {df['year'].min()} - {df['year'].max()}")
        print(f"✓ Columns: {list(df.columns[:10])}...")  # Show first 10 columns
    else:
        print("✗ Data loading failed")

if __name__ == "__main__":
    main()