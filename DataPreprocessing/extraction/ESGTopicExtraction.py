"""
Phase 1: DAX ESG Media Dataset Exploration & Topic Extraction
Dataset: https://www.kaggle.com/datasets/equintel/dax-esg-media-dataset

This script helps you:
1. Load and explore the dataset structure
2. Understand what data you actually have
3. Extract and analyze ESG topics
4. Prepare for ontology design based on REAL data patterns
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re


def load_dax_dataset(file_path):
    """
    Load the DAX ESG dataset and handle different formats
    """
    print("="*80)
    print("STEP 1: LOADING DAX ESG DATASET")
    print("="*80)
    
    # Try different delimiters (CSV might be comma or pipe-separated)
    try:
        df = pd.read_csv(file_path, delimiter='|', low_memory=False)
        print(f"Loaded with '|' delimiter")
    except:
        try:
            df = pd.read_csv(file_path, delimiter=',', low_memory=False)
            print(f"Loaded with ',' delimiter")
        except Exception as e:
            print(f"Error loading file: {e}")
            return None

    print(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    excel_file = file_path.rsplit(".", 1)[0] + ".xlsx"
    try:
        df.to_excel(excel_file, index=False)
        print(f"Saved Excel file for easier reading: {excel_file}")
    except Exception as e:
        print(f"Could not save Excel file: {e}")
    
    
    return df


def explore_dataset_structure(df):
    """
    Understand the dataset structure
    """
    print("\n" + "="*80)
    print("STEP 2: DATASET STRUCTURE ANALYSIS")
    print("="*80)
    
    print("\nColumn Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col} ({df[col].dtype})")
    
    print("\nBasic Statistics:")
    print(f"  Total Records: {len(df):,}")
    print(f"  Date Range: {df['date'].min()} to {df['date'].max()}" if 'date' in df.columns else "  Date column not found")
    
    # Missing values
    print("\nMissing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    for col in df.columns:
        if missing[col] > 0:
            print(f"  {col}: {missing[col]:,} ({missing_pct[col]}%)")
    
    # Sample data
    print("\nFirst Record Sample:")
    print("-"*80)
    first_record = df.iloc[0]
    for col in df.columns:
        value = str(first_record[col])
        if len(value) > 100:
            value = value[:100] + "..."
        print(f"{col}: {value}")
    
    return df


def analyze_companies(df):
    """
    Analyze company distribution
    """
    print("\n" + "="*80)
    print("STEP 3: COMPANY ANALYSIS")
    print("="*80)
    
    if 'company' not in df.columns:
        print("'company' column not found")
        return
    
    companies = df['company'].value_counts()
    
    print(f"\nTotal Unique Companies: {len(companies)}")
    print(f"Reports per Company (avg): {companies.mean():.1f}")
    print(f"Reports per Company (median): {companies.median():.1f}")
    
    print("\nTop 10 Companies by Report Count:")
    for i, (company, count) in enumerate(companies.head(10).items(), 1):
        print(f"  {i:2d}. {company:30s} - {count:4d} reports")
    
    print("\nBottom 10 Companies by Report Count:")
    for i, (company, count) in enumerate(companies.tail(10).items(), 1):
        print(f"  {i:2d}. {company:30s} - {count:4d} reports")
    
    # Visualization
    plt.figure(figsize=(12, 6))
    companies.head(20).plot(kind='bar')
    plt.title('Top 20 Companies by Report Count')
    plt.xlabel('Company')
    plt.ylabel('Number of Reports')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('company_distribution.png', dpi=300, bbox_inches='tight')
    print("\nSaved: company_distribution.png")
    
    return companies


def extract_esg_topics(df):

    all_topics = []

    for idx, row in df.iterrows():
        if pd.notna(row['esg_topics']):
            try:
                topics = eval(row['esg_topics']) if isinstance(row['esg_topics'], str) else row['esg_topics']
                all_topics.extend(topics)
            except Exception as e:
                if idx < 5:
                    print(f"  Warning: Could not parse topics at row {idx}: {e}")
                continue

    topic_counts = Counter(all_topics)
    unique_topics = list(topic_counts.keys())

    # Save unique topics to file
    with open("../categorization/reference/extracted-esg-topics.txt", "w", encoding="utf-8") as f:
        for topic in unique_topics:
            f.write(f"{topic}\n")
    print(f"Saved {len(unique_topics)} unique ESG topics to 'extracted-esg-topics.txt'")

    # Save dataset statistics to separate file
    with open("DAX-dataset-stats.txt", "w", encoding="utf-8") as f:
        f.write("ESG TOPIC STATISTICS:\n")
        f.write(f"Total topic mentions: {len(all_topics):,}\n")
        f.write(f"Unique topics: {len(topic_counts)}\n")
        f.write(f"Most common topics (>100 mentions): {len([t for t, c in topic_counts.items() if c > 100])}\n")
        f.write(f"Rare topics (<10 mentions): {len([t for t, c in topic_counts.items() if c < 10])}\n")
    print("Saved ESG topic statistics to 'DAX-dataset-stats.txt'")


    # Topic co-occurrence
    cooccurrence = analyze_topic_cooccurrence(df)

    return {
        'topic_counts': topic_counts,
        'all_topics': unique_topics,
        'cooccurrence': cooccurrence
    }




def analyze_topic_cooccurrence(df):
    """
    Find which topics appear together in reports
    """
    print("\n  Analyzing which topics appear together...")
    
    cooccurrence = defaultdict(lambda: defaultdict(int))
    
    for idx, row in df.iterrows():
        if pd.notna(row.get('esg_topics')):
            try:
                topics = eval(row['esg_topics']) if isinstance(row['esg_topics'], str) else row['esg_topics']
                
                # Count co-occurrences
                for i, topic1 in enumerate(topics):
                    for topic2 in topics[i+1:]:
                        cooccurrence[topic1][topic2] += 1
                        cooccurrence[topic2][topic1] += 1
                        
            except:
                continue
    
    # Find top co-occurrences
    top_pairs = []
    for topic1, partners in cooccurrence.items():
        for topic2, count in partners.items():
            if topic1 < topic2:  # Avoid duplicates
                top_pairs.append((topic1, topic2, count))
    
    top_pairs.sort(key=lambda x: x[2], reverse=True)
    
    print("\n  Top 10 Topic Pairs (frequently appear together):")
    for i, (topic1, topic2, count) in enumerate(top_pairs[:10], 1):
        print(f"    {i:2d}. {topic1} + {topic2}: {count} times")
    
    return dict(cooccurrence)





# ==============================
# MAIN EXECUTION
# ==============================
def main(file_path):
    df = load_dax_dataset(file_path)
    if df is None:
        return

    df = explore_dataset_structure(df)
    companies = analyze_companies(df)
    topic_analysis = extract_esg_topics(df)

    return df, companies, topic_analysis


if __name__ == "__main__":
    FILE_PATH = "../Dataset/raw/esg_documents_for_dax_companies.csv"
    df, companies, topic_analysis = main(FILE_PATH)

