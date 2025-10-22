#!/usr/bin/env python3
"""
Mushroom Dataset Querying Guide

This script demonstrates various ways to query the mushroom dataset:
1. Pandas DataFrame queries
2. SQLite database queries
3. Advanced filtering and analysis
"""

import pandas as pd
import sqlite3
from pathlib import Path
import numpy as np

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def load_data():
    """Load the mushroom dataset."""
    data_file = Path("data/processed/loaded_data.csv")
    if not data_file.exists():
        print("❌ No processed data found. Run the ETL pipeline first!")
        return None
    
    print("📊 Loading mushroom dataset...")
    df = pd.read_csv(data_file)
    print(f"✅ Loaded {len(df):,} mushrooms with {len(df.columns)} features")
    return df

def basic_queries(df):
    """Demonstrate basic pandas queries."""
    print_section("BASIC PANDAS QUERIES")
    
    print("1. 📊 Dataset Overview:")
    print(f"   Shape: {df.shape}")
    print(f"   Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\n2. 🎯 Target Distribution:")
    if 'class' in df.columns:
        class_counts = df['class'].value_counts()
        for class_name, count in class_counts.items():
            percentage = (count / len(df)) * 100
            print(f"   {class_name}: {count:,} ({percentage:.1f}%)")
    
    print("\n3. 📋 First 5 rows:")
    print(df.head())
    
    print("\n4. 🔢 Data Types:")
    print(df.dtypes.value_counts())

def filtering_queries(df):
    """Demonstrate filtering queries."""
    print_section("FILTERING QUERIES")
    
    print("1. 🟢 Edible Mushrooms Only:")
    if 'class' in df.columns:
        edible = df[df['class'] == 'e']
        print(f"   Count: {len(edible):,} mushrooms")
        print(f"   Percentage: {len(edible)/len(df)*100:.1f}%")
    
    print("\n2. 🔴 Poisonous Mushrooms Only:")
    if 'class' in df.columns:
        poisonous = df[df['class'] == 'p']
        print(f"   Count: {len(poisonous):,} mushrooms")
        print(f"   Percentage: {len(poisonous)/len(df)*100:.1f}%")
    
    print("\n3. 🍄 Mushrooms with Specific Features:")
    # Find mushrooms with bell-shaped caps
    if 'cap-shape_b' in df.columns:
        bell_caps = df[df['cap-shape_b'] == True]
        print(f"   Bell-shaped caps: {len(bell_caps):,} mushrooms")
    
    # Find mushrooms with no odor
    if 'odor_n' in df.columns:
        no_odor = df[df['odor_n'] == True]
        print(f"   No odor: {len(no_odor):,} mushrooms")
    
    print("\n4. 🔍 Complex Filtering:")
    if 'class' in df.columns and 'cap-shape_b' in df.columns and 'odor_n' in df.columns:
        # Edible mushrooms with bell-shaped caps and no odor
        complex_filter = df[(df['class'] == 'e') & (df['cap-shape_b'] == True) & (df['odor_n'] == True)]
        print(f"   Edible + Bell-shaped + No odor: {len(complex_filter):,} mushrooms")

def feature_analysis(df):
    """Demonstrate feature analysis queries."""
    print_section("FEATURE ANALYSIS QUERIES")
    
    print("1. 🔢 Feature Statistics:")
    # Count True values for each feature
    feature_counts = df.select_dtypes(include=[bool]).sum()
    print(f"   Most common features:")
    top_features = feature_counts.nlargest(10)
    for feature, count in top_features.items():
        percentage = (count / len(df)) * 100
        print(f"   {feature}: {count:,} ({percentage:.1f}%)")
    
    print("\n2. 🎯 Feature Correlation with Target:")
    if 'class' in df.columns:
        # Convert class to numeric for correlation
        df_numeric = df.copy()
        df_numeric['class_numeric'] = (df_numeric['class'] == 'e').astype(int)
        
        # Calculate correlation with target
        correlations = df_numeric.select_dtypes(include=[bool]).corrwith(df_numeric['class_numeric'])
        print(f"   Top positive correlations (edible indicators):")
        top_positive = correlations.nlargest(5)
        for feature, corr in top_positive.items():
            print(f"   {feature}: {corr:.3f}")
        
        print(f"   Top negative correlations (poisonous indicators):")
        top_negative = correlations.nsmallest(5)
        for feature, corr in top_negative.items():
            print(f"   {feature}: {corr:.3f}")

def sqlite_queries():
    """Demonstrate SQLite database queries."""
    print_section("SQLITE DATABASE QUERIES")
    
    db_file = Path("data/mushroom_etl.db")
    if not db_file.exists():
        print("❌ No database found. Run the ETL pipeline first!")
        return
    
    print("📊 Connecting to SQLite database...")
    conn = sqlite3.connect(db_file)
    
    print("\n1. 🗄️ Database Schema:")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"   Tables: {[table[0] for table in tables]}")
    
    print("\n2. 📊 Table Information:")
    cursor.execute("PRAGMA table_info(mushroom_data);")
    columns = cursor.fetchall()
    print(f"   Columns: {len(columns)}")
    print(f"   Sample columns: {[col[1] for col in columns[:5]]}...")
    
    print("\n3. 🔍 SQL Queries:")
    
    # Count total records
    cursor.execute("SELECT COUNT(*) FROM mushroom_data;")
    total_count = cursor.fetchone()[0]
    print(f"   Total mushrooms: {total_count:,}")
    
    # Count by class
    cursor.execute("SELECT class, COUNT(*) FROM mushroom_data GROUP BY class;")
    class_counts = cursor.fetchall()
    print(f"   Class distribution:")
    for class_name, count in class_counts:
        percentage = (count / total_count) * 100
        print(f"     {class_name}: {count:,} ({percentage:.1f}%)")
    
    # Find edible mushrooms with specific features
    cursor.execute("""
        SELECT COUNT(*) FROM mushroom_data 
        WHERE class = 'e' AND "cap-shape_b" = 1 AND "odor_n" = 1;
    """)
    edible_bell_no_odor = cursor.fetchone()[0]
    print(f"   Edible + Bell-shaped + No odor: {edible_bell_no_odor:,}")
    
    # Find most common cap shapes
    cursor.execute("""
        SELECT 
            CASE 
                WHEN "cap-shape_b" = 1 THEN 'bell'
                WHEN "cap-shape_c" = 1 THEN 'conical'
                WHEN "cap-shape_f" = 1 THEN 'flat'
                WHEN "cap-shape_k" = 1 THEN 'knobbed'
                WHEN "cap-shape_s" = 1 THEN 'sunken'
                WHEN "cap-shape_x" = 1 THEN 'convex'
            END as cap_shape,
            COUNT(*) as count
        FROM mushroom_data 
        GROUP BY 
            CASE 
                WHEN "cap-shape_b" = 1 THEN 'bell'
                WHEN "cap-shape_c" = 1 THEN 'conical'
                WHEN "cap-shape_f" = 1 THEN 'flat'
                WHEN "cap-shape_k" = 1 THEN 'knobbed'
                WHEN "cap-shape_s" = 1 THEN 'sunken'
                WHEN "cap-shape_x" = 1 THEN 'convex'
            END
        ORDER BY count DESC;
    """)
    cap_shapes = cursor.fetchall()
    print(f"   Most common cap shapes:")
    for shape, count in cap_shapes:
        percentage = (count / total_count) * 100
        print(f"     {shape}: {count:,} ({percentage:.1f}%)")
    
    conn.close()
    print("\n✅ Database queries completed!")

def advanced_queries(df):
    """Demonstrate advanced analytical queries."""
    print_section("ADVANCED ANALYTICAL QUERIES")
    
    print("1. 📊 Statistical Analysis:")
    if 'class' in df.columns:
        # Convert to numeric for analysis
        df_numeric = df.copy()
        df_numeric['is_edible'] = (df_numeric['class'] == 'e').astype(int)
        
        # Calculate feature importance (correlation with target)
        correlations = df_numeric.select_dtypes(include=[bool]).corrwith(df_numeric['is_edible'])
        
        print(f"   Most important features for classification:")
        important_features = correlations.abs().nlargest(10)
        for feature, importance in important_features.items():
            corr_value = correlations[feature]
            direction = "edible" if corr_value > 0 else "poisonous"
            print(f"     {feature}: {importance:.3f} (indicates {direction})")
    
    print("\n2. 🎯 Classification Patterns:")
    if 'class' in df.columns:
        # Find features that perfectly separate classes
        perfect_separators = []
        for col in df.select_dtypes(include=[bool]).columns:
            if col != 'class':
                # Check if feature perfectly separates classes
                edible_with_feature = df[(df['class'] == 'e') & (df[col] == True)]
                poisonous_with_feature = df[(df['class'] == 'p') & (df[col] == True)]
                
                if len(edible_with_feature) > 0 and len(poisonous_with_feature) == 0:
                    perfect_separators.append((col, 'edible_only'))
                elif len(poisonous_with_feature) > 0 and len(edible_with_feature) == 0:
                    perfect_separators.append((col, 'poisonous_only'))
        
        print(f"   Perfect class separators: {len(perfect_separators)}")
        for feature, direction in perfect_separators[:5]:
            print(f"     {feature}: only in {direction}")
    
    print("\n3. 🔍 Data Quality Checks:")
    # Check for constant features
    constant_features = []
    for col in df.select_dtypes(include=[bool]).columns:
        if df[col].nunique() <= 1:
            constant_features.append(col)
    
    print(f"   Constant features: {len(constant_features)}")
    if constant_features:
        print(f"     Examples: {constant_features[:3]}")
    
    # Check for highly correlated features
    print(f"   Feature redundancy analysis:")
    feature_matrix = df.select_dtypes(include=[bool])
    correlation_matrix = feature_matrix.corr()
    
    # Find highly correlated feature pairs
    high_corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_value = correlation_matrix.iloc[i, j]
            if abs(corr_value) > 0.9:  # High correlation threshold
                high_corr_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_value))
    
    print(f"   Highly correlated feature pairs: {len(high_corr_pairs)}")
    if high_corr_pairs:
        for feat1, feat2, corr in high_corr_pairs[:3]:
            print(f"     {feat1} <-> {feat2}: {corr:.3f}")

def query_examples():
    """Show practical query examples."""
    print_section("PRACTICAL QUERY EXAMPLES")
    
    print("🐍 Python/Pandas Examples:")
    print("""
# Load data
import pandas as pd
df = pd.read_csv('data/processed/loaded_data.csv')

# Basic queries
edible_mushrooms = df[df['class'] == 'e']
poisonous_mushrooms = df[df['class'] == 'p']

# Feature-specific queries
bell_caps = df[df['cap-shape_b'] == True]
no_odor = df[df['odor_n'] == True]

# Complex filtering
safe_mushrooms = df[(df['class'] == 'e') & (df['cap-shape_b'] == True) & (df['odor_n'] == True)]

# Statistical analysis
feature_importance = df.select_dtypes(include=[bool]).corrwith(df['class'] == 'e')
    """)
    
    print("\n🗄️ SQL Examples:")
    print("""
# Connect to database
import sqlite3
conn = sqlite3.connect('data/mushroom_etl.db')

# Basic queries
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM mushroom_data WHERE class = 'e';")
edible_count = cursor.fetchone()[0]

# Complex queries
cursor.execute('''
    SELECT COUNT(*) FROM mushroom_data 
    WHERE class = 'e' AND cap_shape_b = 1 AND odor_n = 1;
''')
safe_count = cursor.fetchone()[0]

# Aggregation queries
cursor.execute('''
    SELECT class, COUNT(*) as count 
    FROM mushroom_data 
    GROUP BY class;
''')
class_distribution = cursor.fetchall()
    """)

def main():
    """Main querying demonstration."""
    print("🍄 MUSHROOM DATASET QUERYING GUIDE")
    print("=" * 60)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Run all query demonstrations
    basic_queries(df)
    filtering_queries(df)
    feature_analysis(df)
    sqlite_queries()
    advanced_queries(df)
    query_examples()
    
    print_section("🎉 QUERYING COMPLETE")
    print("✅ You now know how to query the mushroom dataset!")
    print("📁 Data files:")
    print("   - CSV: data/processed/loaded_data.csv")
    print("   - Database: data/mushroom_etl.db")
    print("🔧 Tools: Pandas, SQLite, NumPy")

if __name__ == "__main__":
    main()
