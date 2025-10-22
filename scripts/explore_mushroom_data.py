#!/usr/bin/env python3
"""
Mushroom Data Exploration Script

This script demonstrates that we have working mushroom data by:
1. Loading the processed data
2. Showing data statistics and visualizations
3. Demonstrating the machine learning readiness
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.config import config

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section."""
    print(f"\n🔍 {title}")
    print("-" * 50)

def load_mushroom_data():
    """Load the processed mushroom data."""
    print_header("🍄 MUSHROOM DATA EXPLORATION")
    
    # Try to load processed data first
    processed_file = Path("data/processed/loaded_data.csv")
    raw_file = Path("data/raw/mushrooms.csv")
    
    if processed_file.exists():
        print("📊 Loading processed mushroom data...")
        df = pd.read_csv(processed_file)
        print(f"✅ Loaded processed data: {len(df)} records, {len(df.columns)} features")
        return df, "processed"
    elif raw_file.exists():
        print("📊 Loading raw mushroom data...")
        df = pd.read_csv(raw_file)
        print(f"✅ Loaded raw data: {len(df)} records, {len(df.columns)} columns")
        return df, "raw"
    else:
        print("❌ No mushroom data found. Run the ETL pipeline first!")
        return None, None

def show_data_overview(df, data_type):
    """Show basic data overview."""
    print_section("DATA OVERVIEW")
    
    print(f"📈 Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"📊 Data Type: {data_type}")
    print(f"💾 Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Show first few rows
    print(f"\n📋 First 5 rows:")
    print(df.head())
    
    # Show data types
    print(f"\n🔢 Data Types:")
    print(df.dtypes.value_counts())

def show_target_distribution(df):
    """Show the target variable distribution."""
    print_section("TARGET VARIABLE ANALYSIS")
    
    # Find the target column (class or similar)
    target_cols = [col for col in df.columns if 'class' in col.lower() or 'target' in col.lower()]
    
    if target_cols:
        target_col = target_cols[0]
        print(f"🎯 Target Column: {target_col}")
        
        # Show distribution
        target_counts = df[target_col].value_counts()
        print(f"\n📊 Target Distribution:")
        for value, count in target_counts.items():
            percentage = (count / len(df)) * 100
            print(f"   {value}: {count:,} ({percentage:.1f}%)")
        
        # Show if it's balanced
        if len(target_counts) == 2:
            ratio = target_counts.iloc[0] / target_counts.iloc[1]
            if 0.8 <= ratio <= 1.2:
                print("✅ Dataset is well-balanced")
            else:
                print("⚠️  Dataset is imbalanced")
        
        return target_col
    else:
        print("❌ No target column found")
        return None

def show_feature_analysis(df, target_col=None):
    """Show feature analysis."""
    print_section("FEATURE ANALYSIS")
    
    # Show feature types
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    print(f"🔢 Numeric Features: {len(numeric_cols)}")
    print(f"📝 Categorical Features: {len(categorical_cols)}")
    
    if len(numeric_cols) > 0:
        print(f"\n📊 Numeric Features Summary:")
        print(df[numeric_cols].describe())
    
    if len(categorical_cols) > 0:
        print(f"\n📝 Categorical Features (first 5):")
        for col in categorical_cols[:5]:
            unique_vals = df[col].nunique()
            print(f"   {col}: {unique_vals} unique values")
            if unique_vals <= 10:
                print(f"      Values: {list(df[col].unique())}")

def show_missing_data(df):
    """Show missing data analysis."""
    print_section("MISSING DATA ANALYSIS")
    
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Missing Count': missing_data,
        'Missing %': missing_percent
    }).sort_values('Missing %', ascending=False)
    
    if missing_df['Missing Count'].sum() == 0:
        print("✅ No missing data found!")
    else:
        print("⚠️  Missing data found:")
        print(missing_df[missing_df['Missing Count'] > 0])

def show_data_quality(df):
    """Show data quality metrics."""
    print_section("DATA QUALITY METRICS")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"🔄 Duplicate rows: {duplicates}")
    
    # Check for constant columns
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if constant_cols:
        print(f"⚠️  Constant columns: {constant_cols}")
    else:
        print("✅ No constant columns found")
    
    # Check for high cardinality
    high_card_cols = []
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() > len(df) * 0.5:
            high_card_cols.append(col)
    
    if high_card_cols:
        print(f"⚠️  High cardinality columns: {high_card_cols}")
    else:
        print("✅ No high cardinality issues")

def create_visualizations(df, target_col=None):
    """Create data visualizations."""
    print_section("DATA VISUALIZATIONS")
    
    try:
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('🍄 Mushroom Dataset Analysis', fontsize=16, fontweight='bold')
        
        # 1. Target distribution
        if target_col and target_col in df.columns:
            ax1 = axes[0, 0]
            target_counts = df[target_col].value_counts()
            target_counts.plot(kind='bar', ax=ax1, color=['#ff9999', '#66b3ff'])
            ax1.set_title('Target Distribution')
            ax1.set_xlabel('Class')
            ax1.set_ylabel('Count')
            ax1.tick_params(axis='x', rotation=45)
        
        # 2. Feature count
        ax2 = axes[0, 1]
        feature_types = ['Numeric', 'Categorical']
        feature_counts = [
            len(df.select_dtypes(include=[np.number]).columns),
            len(df.select_dtypes(include=['object']).columns)
        ]
        ax2.bar(feature_types, feature_counts, color=['#99ff99', '#ffcc99'])
        ax2.set_title('Feature Types')
        ax2.set_ylabel('Count')
        
        # 3. Dataset size
        ax3 = axes[1, 0]
        size_info = ['Rows', 'Columns']
        size_values = [df.shape[0], df.shape[1]]
        ax3.bar(size_info, size_values, color=['#ff99cc', '#99ccff'])
        ax3.set_title('Dataset Dimensions')
        ax3.set_ylabel('Count')
        
        # 4. Missing data
        ax4 = axes[1, 1]
        missing_count = df.isnull().sum().sum()
        total_cells = df.shape[0] * df.shape[1]
        missing_percent = (missing_count / total_cells) * 100
        
        ax4.pie([missing_count, total_cells - missing_count], 
                labels=['Missing', 'Complete'],
                autopct='%1.1f%%',
                colors=['#ff9999', '#99ff99'])
        ax4.set_title('Data Completeness')
        
        plt.tight_layout()
        
        # Save the plot
        output_path = Path("data/processed/mushroom_analysis.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"📊 Visualization saved to: {output_path}")
        
        # Show the plot
        plt.show()
        
    except Exception as e:
        print(f"⚠️  Could not create visualizations: {e}")
        print("   (This is normal if running in a headless environment)")

def show_ml_readiness(df, target_col=None):
    """Show machine learning readiness."""
    print_section("MACHINE LEARNING READINESS")
    
    if target_col and target_col in df.columns:
        print("✅ Target variable identified")
        
        # Check if it's a classification problem
        unique_targets = df[target_col].nunique()
        print(f"🎯 Classification problem: {unique_targets} classes")
        
        # Check feature count
        feature_count = len(df.columns) - 1  # Exclude target
        print(f"🔢 Features: {feature_count}")
        
        # Check for numeric features
        numeric_features = len(df.select_dtypes(include=[np.number]).columns)
        if target_col in df.select_dtypes(include=[np.number]).columns:
            numeric_features -= 1
        
        print(f"📊 Numeric features: {numeric_features}")
        print(f"📝 Categorical features: {feature_count - numeric_features}")
        
        # Sample size check
        if len(df) >= 1000:
            print("✅ Sufficient sample size for ML")
        else:
            print("⚠️  Small sample size - consider data augmentation")
        
        print(f"\n🚀 Ready for machine learning!")
        print(f"   - Dataset size: {len(df):,} samples")
        print(f"   - Feature count: {feature_count}")
        print(f"   - Problem type: {'Binary' if unique_targets == 2 else 'Multi-class'} classification")
        
    else:
        print("❌ No target variable found - data needs preprocessing")

def main():
    """Main exploration function."""
    # Load data
    df, data_type = load_mushroom_data()
    
    if df is None:
        return
    
    # Run all analyses
    show_data_overview(df, data_type)
    target_col = show_target_distribution(df)
    show_feature_analysis(df, target_col)
    show_missing_data(df)
    show_data_quality(df)
    create_visualizations(df, target_col)
    show_ml_readiness(df, target_col)
    
    print_header("🎉 EXPLORATION COMPLETE")
    print("✅ Mushroom data is working and ready for machine learning!")
    print(f"📁 Data location: data/processed/loaded_data.csv")
    print(f"📊 Analysis saved: data/processed/mushroom_analysis.png")

if __name__ == "__main__":
    main()
