#!/usr/bin/env python3
"""
Simple Excel File Reader
Reads and displays basic information about Excel files
"""

import pandas as pd
from pathlib import Path

def analyze_excel_file(file_path):
    """
    Read and analyze an Excel file
    """
    print(f"📊 Analyzing Excel file: {file_path}")
    print("=" * 60)

    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Basic file information
        print(f"📋 File Information:")
        print(f"   - Total rows: {len(df)}")
        print(f"   - Total columns: {len(df.columns)}")
        print(f"   - File size: {Path(file_path).stat().st_size:,} bytes")
        print()

        # Column information
        print(f"📝 Column Information:")
        for i, col in enumerate(df.columns, 1):
            non_null_count = df[col].notna().sum()
            data_type = str(df[col].dtype)
            print(f"   {i:2d}. {col:<30} | Type: {data_type:<15} | Non-null: {non_null_count:3d}/{len(df)}")
        print()

        # Sample data (first 5 rows)
        print(f"🔍 Sample Data (First 5 rows):")
        print("-" * 80)
        print(df.head().to_string(index=False, max_cols=8))
        print()

        # Data quality analysis
        print(f"📈 Data Quality Analysis:")
        print("-" * 30)

        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.any():
            print("Missing values:")
            for col, missing_count in missing_data.items():
                if missing_count > 0:
                    percentage = (missing_count / len(df)) * 100
                    print(f"   {col:<30}: {missing_count:3d} ({percentage:5.1f}%)")
        else:
            print("✅ No missing values found!")
        print()

        # Numeric columns analysis
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print(f"🔢 Numeric Columns Summary:")
            print("-" * 30)
            print(df[numeric_cols].describe().to_string())
            print()

        # Text columns analysis
        text_cols = df.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            print(f"📝 Text Columns Analysis:")
            print("-" * 30)
            for col in text_cols[:5]:  # Show first 5 text columns
                unique_values = df[col].nunique()
                print(f"   {col:<30}: {unique_values} unique values")
                if unique_values <= 10:  # Show all values if few
                    for val in df[col].unique():
                        if pd.notna(val):
                            count = df[col].value_counts()[val]
                            print(f"      - {str(val)[:40]:<40}: {count} occurrences")
        print()

        # Potential insights based on column names
        print(f"💡 Potential Insights:")
        print("-" * 25)

        # Look for price-related columns
        price_cols = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['price', 'cost', 'amount', '$', 'fee'])]
        if price_cols:
            print(f"💰 Price-related columns found: {price_cols}")
            for col in price_cols:
                if df[col].dtype in ['int64', 'float64']:
                    print(f"   - {col}: Min=${df[col].min():,.2f}, Max=${df[col].max():,.2f}, Avg=${df[col].mean():,.2f}")

        # Look for date-related columns
        date_cols = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['date', 'time', 'created', 'updated'])]
        if date_cols:
            print(f"📅 Date-related columns found: {date_cols}")

        # Look for location-related columns
        location_cols = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['city', 'state', 'address', 'location', 'zip'])]
        if location_cols:
            print(f"📍 Location-related columns found: {location_cols}")

        # Look for product/item columns
        product_cols = [col for col in df.columns if any(keyword in str(col).lower() for keyword in ['product', 'item', 'name', 'title', 'description'])]
        if product_cols:
            print(f"📦 Product/Item columns found: {product_cols}")

        return df

    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

# Run the analysis
if __name__ == "__main__":
    df = analyze_excel_file("austin.xlsx")
    if df is not None:
        print(f"\n✅ Analysis complete! Successfully analyzed austin.xlsx")
        print(f"📊 Data contains {len(df)} rows and {len(df.columns)} columns")