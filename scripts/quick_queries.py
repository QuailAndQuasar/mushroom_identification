#!/usr/bin/env python3
"""
Quick Mushroom Dataset Queries

Common queries for the mushroom dataset - ready to copy and paste!
"""

import pandas as pd
import sqlite3
from pathlib import Path

def quick_pandas_queries():
    """Quick pandas queries you can copy and paste."""
    print("🐍 QUICK PANDAS QUERIES")
    print("=" * 50)
    
    # Load data
    df = pd.read_csv('data/processed/loaded_data.csv')
    
    print("1. Basic Info:")
    print(f"df.shape  # {df.shape}")
    print(f"df['class'].value_counts()  # Class distribution")
    print()
    
    print("2. Filtering:")
    print("edible = df[df['class'] == 'e']  # Edible mushrooms")
    print("poisonous = df[df['class'] == 'p']  # Poisonous mushrooms")
    print("bell_caps = df[df['cap-shape_b'] == True]  # Bell-shaped caps")
    print("no_odor = df[df['odor_n'] == True]  # No odor")
    print()
    
    print("3. Complex Filtering:")
    print("safe = df[(df['class'] == 'e') & (df['cap-shape_b'] == True) & (df['odor_n'] == True)]")
    print("dangerous = df[(df['class'] == 'p') & (df['odor_f'] == True)]")
    print()
    
    print("4. Feature Analysis:")
    print("df.select_dtypes(include=[bool]).sum()  # Feature counts")
    print("df.corr()['class']  # Correlations with target")
    print()
    
    print("5. Statistical Queries:")
    print("df.groupby('class').size()  # Count by class")
    print("df.describe()  # Basic statistics")
    print("df.isnull().sum()  # Missing values")

def quick_sql_queries():
    """Quick SQL queries you can copy and paste."""
    print("\n🗄️ QUICK SQL QUERIES")
    print("=" * 50)
    
    print("1. Basic Queries:")
    print("SELECT COUNT(*) FROM mushroom_data;  -- Total count")
    print("SELECT class, COUNT(*) FROM mushroom_data GROUP BY class;  -- Class distribution")
    print()
    
    print("2. Filtering:")
    print("SELECT * FROM mushroom_data WHERE class = 'e';  -- Edible mushrooms")
    print("SELECT * FROM mushroom_data WHERE class = 'p';  -- Poisonous mushrooms")
    print("SELECT * FROM mushroom_data WHERE \"cap-shape_b\" = 1;  -- Bell-shaped caps")
    print("SELECT * FROM mushroom_data WHERE \"odor_n\" = 1;  -- No odor")
    print()
    
    print("3. Complex Filtering:")
    print("SELECT COUNT(*) FROM mushroom_data WHERE class = 'e' AND \"cap-shape_b\" = 1 AND \"odor_n\" = 1;")
    print("SELECT COUNT(*) FROM mushroom_data WHERE class = 'p' AND \"odor_f\" = 1;")
    print()
    
    print("4. Feature Analysis:")
    print("SELECT \"cap-shape_b\", COUNT(*) FROM mushroom_data WHERE \"cap-shape_b\" = 1;")
    print("SELECT \"odor_n\", COUNT(*) FROM mushroom_data WHERE \"odor_n\" = 1;")
    print()
    
    print("5. Aggregations:")
    print("SELECT class, AVG(\"cap-shape_b\") FROM mushroom_data GROUP BY class;")
    print("SELECT \"gill-size_b\", COUNT(*) FROM mushroom_data GROUP BY \"gill-size_b\";")

def practical_examples():
    """Practical query examples."""
    print("\n🎯 PRACTICAL EXAMPLES")
    print("=" * 50)
    
    print("Find safe mushrooms to eat:")
    print("safe = df[(df['class'] == 'e') & (df['odor_n'] == True) & (df['bruises_t'] == True)]")
    print("print(f'Safe mushrooms: {len(safe)}')")
    print()
    
    print("Find dangerous mushrooms to avoid:")
    print("dangerous = df[(df['class'] == 'p') & (df['odor_f'] == True)]")
    print("print(f'Dangerous mushrooms: {len(dangerous)}')")
    print()
    
    print("Find mushrooms by cap shape:")
    print("convex_caps = df[df['cap-shape_x'] == True]")
    print("flat_caps = df[df['cap-shape_f'] == True]")
    print("bell_caps = df[df['cap-shape_b'] == True]")
    print()
    
    print("Analyze feature importance:")
    print("correlations = df.select_dtypes(include=[bool]).corrwith(df['class'] == 'e')")
    print("important = correlations.abs().nlargest(10)")
    print("print(important)")

def main():
    """Show quick query examples."""
    print("🍄 QUICK MUSHROOM DATASET QUERIES")
    print("=" * 60)
    print("Copy and paste these queries to analyze your data!")
    
    quick_pandas_queries()
    quick_sql_queries()
    practical_examples()
    
    print("\n" + "=" * 60)
    print("🎉 Ready to query your mushroom dataset!")
    print("📁 Data: data/processed/loaded_data.csv")
    print("🗄️ Database: data/mushroom_etl.db")

if __name__ == "__main__":
    main()
