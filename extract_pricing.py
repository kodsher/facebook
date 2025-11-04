#!/usr/bin/env python3
"""
Pricing Data Extractor
Extracts model, storage, and grade information from austin.xlsx and creates a structured CSV
"""

import pandas as pd
import re
import csv
from typing import List, Dict, Optional, Tuple

def extract_model_info(text: str) -> Tuple[str, str, str]:
    """
    Extract model, storage, and grade information from text
    Returns: (model, storage, grade)
    """
    if not text or pd.isna(text):
        return "", "", ""

    text = str(text).strip()

    # Initialize results
    model = ""
    storage = ""
    grade = ""

    # Extract model information
    model_patterns = [
        r'iPhone\s*(\d+\s*(?:Pro\s*)?(?:Max\s*)?|(?:Pro\s*)?\d+\s*(?:Plus\s*)?|SE\d*|Air\d*)',
        r'Galaxy\s*(S\d+(?:\s*(?:Plus|Ultra)*)?|Note\s*\d+|Z\s*(?:Fold|Flip)\s*\d+|A\d+)',
        r'iPad\s*(Pro|Air|mini)?\s*(\d+(?:\.\d+)?)?',
        r'MacBook\s*(Pro|Air)?\s*(\d+"?)?',
        r'Apple\s*Watch\s*(Series\s*\d+|Ultra|SE)?',
        r'(AirPods|AirPods\s*Pro|AirPods\s*Max)',
        r'(Samsung|OnePlus|Google\s*Pixel)\s*[\w\s-]+'
    ]

    for pattern in model_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            model = match.group(0).strip()
            break

    # Extract storage information
    storage_patterns = [
        r'(\d+)\s*GB',
        r'(\d+)\s*TB',
        r'(\d+)G',
        r'(\d+)T'
    ]

    for pattern in storage_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            storage_num = match.group(1)
            if 'TB' in text.upper() or 'T' in text.upper():
                storage = f"{storage_num}TB"
            else:
                storage = f"{storage_num}GB"
            break

    # Extract grade information
    grade_patterns = [
        (r'new\s*sealed|sealed\s*new|factory\s*sealed|brand\s*new', 'New Sealed'),
        (r'open\s*box|opened\s*box|box\s*open', 'Open Box'),
        (r'\bA\s*grade|grade\s*A|A\b', 'A Grade'),
        (r'\bB\s*grade|grade\s*B|B\b', 'B Grade'),
        (r'\bC\s*grade|grade\s*C|C\b', 'C Grade'),
        (r'\bD\s*grade|grade\s*D|D\b', 'D Grade'),
        (r'DOA|dead\s*on\s*arrival', 'DOA'),
        (r'cracked\s*back|back\s*cracked|broken\s*back', 'Cracked Back'),
        (r'cracked\s*screen|screen\s*cracked|broken\s*screen', 'Cracked Screen'),
        (r'like\s*new|excellent|mint', 'A Grade'),
        (r'good|fair', 'B Grade'),
        (r'poor|rough', 'C Grade')
    ]

    for pattern, grade_name in grade_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            grade = grade_name
            break

    # Extract price information
    price_patterns = [
        r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|dollars?)'
    ]

    return model, storage, grade

def extract_price(text: str) -> Optional[float]:
    """
    Extract price from text
    """
    if not text or pd.isna(text):
        return None

    text = str(text)

    # Look for price patterns
    price_patterns = [
        r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|dollars?)'
    ]

    for pattern in price_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            try:
                # Clean the price string and convert to float
                price_str = matches[0].replace(',', '')
                return float(price_str)
            except ValueError:
                continue

    return None

def process_excel_file(file_path: str) -> List[Dict]:
    """
    Process the Excel file and extract pricing information
    """
    print(f"🔍 Processing {file_path}...")

    # Read the Excel file
    df = pd.read_excel(file_path)

    extracted_data = []

    # Process each column
    for col in df.columns:
        print(f"   Processing column: {col}")

        for idx, value in enumerate(df[col]):
            if pd.notna(value) and value != "":
                text = str(value).strip()

                # Skip if it looks like a policy/address text
                if any(keyword in text.lower() for keyword in [
                    'office', 'address', 'please', 'due to', 'we buy', 'we don\'t',
                    'hong kong', 'verizon', 't-mobile', 'xfinity', 'receipt'
                ]):
                    continue

                # Extract information
                model, storage, grade = extract_model_info(text)
                price = extract_price(text)

                # Only include if we found meaningful information
                if model or price:
                    extracted_data.append({
                        'model': model if model else text[:50],  # Use text as model if no pattern matched
                        'storage': storage,
                        'grade': grade,
                        'price': price,
                        'raw_text': text,
                        'row': idx + 1,
                        'column': col
                    })

    return extracted_data

def save_to_csv(data: List[Dict], output_file: str):
    """
    Save extracted data to CSV file
    """
    print(f"💾 Saving {len(data)} records to {output_file}")

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['model', 'storage', 'grade', 'price', 'row', 'column']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for item in data:
            # Only write the main fields to CSV
            writer.writerow({
                'model': item['model'],
                'storage': item['storage'],
                'grade': item['grade'],
                'price': item['price'],
                'row': item['row'],
                'column': item['column']
            })

    print(f"✅ CSV file saved: {output_file}")

def main():
    """
    Main function
    """
    input_file = "austin.xlsx"
    output_file = "austin_pricing_extracted.csv"

    # Process the Excel file
    extracted_data = process_excel_file(input_file)

    # Save to CSV
    save_to_csv(extracted_data, output_file)

    # Print summary
    print(f"\n📊 Extraction Summary:")
    print(f"   Total records extracted: {len(extracted_data)}")

    if extracted_data:
        # Count by grade
        grade_counts = {}
        storage_counts = {}
        price_sum = 0
        price_count = 0

        for item in extracted_data:
            if item['grade']:
                grade_counts[item['grade']] = grade_counts.get(item['grade'], 0) + 1
            if item['storage']:
                storage_counts[item['storage']] = storage_counts.get(item['storage'], 0) + 1
            if item['price']:
                price_sum += item['price']
                price_count += 1

        print(f"\n📈 Grade Distribution:")
        for grade, count in sorted(grade_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {grade:<20}: {count:3d} items")

        print(f"\n💾 Storage Distribution:")
        for storage, count in sorted(storage_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {storage:<10}: {count:3d} items")

        if price_count > 0:
            print(f"\n💰 Price Summary:")
            print(f"   Items with prices: {price_count}")
            print(f"   Average price: ${price_sum/price_count:,.2f}")
            print(f"   Total value: ${price_sum:,.2f}")

if __name__ == "__main__":
    main()