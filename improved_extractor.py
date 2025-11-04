#!/usr/bin/env python3
"""
Improved Pricing Data Extractor
Enhanced extraction with better model, storage, and grade detection
"""

import pandas as pd
import re
import csv
from typing import List, Dict, Optional, Tuple

def extract_model_info(text: str) -> Tuple[str, str, str]:
    """
    Enhanced model, storage, and grade extraction
    """
    if not text or pd.isna(text):
        return "", "", ""

    text = str(text).strip()

    # Initialize results
    model = ""
    storage = ""
    grade = ""

    # Enhanced model patterns
    model_patterns = [
        # iPhone patterns (more specific)
        r'iPhone\s*(\d+(?:\s*(?:Pro|Plus|Max|mini|Air|SE)\s*)*(?:\s*\d+GB|\s*\d+TB)?)',
        r'iPhone\s*SE\s*(\d+)?',
        r'iPhone\s*Air',

        # Samsung patterns
        r'Galaxy\s*(S\d+(?:\s*(?:Plus|Ultra|FE)*)?|Note\s*\d+|Z\s*(?:Fold|Flip)\s*\d+|A\d+\s*(?:\d+GB)?)',

        # iPad patterns
        r'iPad\s*(Pro|Air|mini)?\s*(\d+(?:\.\d+)?)?\s*(\d+GB|\d+TB)?',

        # MacBook patterns
        r'MacBook\s*(Pro|Air)?\s*(\d+"?)?\s*(\d+GB|\d+TB)?',

        # Apple Watch
        r'Apple\s*Watch\s*(Series\s*\d+|Ultra|SE)?\s*(\d+mm)?',

        # AirPods
        r'AirPods\s*(Pro|Max|Gen\s*\d+)?',

        # General patterns
        r'(Samsung|OnePlus|Google\s*Pixel)\s*[\w\s-]+'
    ]

    for pattern in model_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            model = match.group(0).strip()
            # Clean up the model name
            model = re.sub(r'\s+', ' ', model)
            break

    # Enhanced storage extraction with better context
    storage_patterns = [
        r'(\d+)\s*GB(?![a-zA-Z])',  # \d+GB followed by non-letter
        r'(\d+)\s*TB(?![a-zA-Z])',  # \d+TB followed by non-letter
        r'(\d+)\s*G(?!\w)',          # \d+G not followed by word character
        r'(\d+)\s*T(?!\w)',          # \d+T not followed by word character
        r'(\d+)GB',
        r'(\d+)TB'
    ]

    for pattern in storage_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            storage_num = match.group(1)
            # Determine if it's TB or GB based on context
            if 'tb' in text[match.start():match.start()+10].lower():
                storage = f"{storage_num}TB"
            else:
                storage = f"{storage_num}GB"
            break

    # Enhanced grade patterns (more comprehensive)
    grade_patterns = [
        # New/Sealed
        (r'new\s*sealed|sealed\s*new|factory\s*sealed|brand\s*new|new\s*in\s*box|nib', 'New Sealed'),

        # Open Box
        (r'open\s*box|opened\s*box|box\s*open|open\s*condition', 'Open Box'),

        # Grade A (excellent condition)
        (r'\bA\s*grade|grade\s*A|excellent\s*condition|like\s*new|mint\s*condition|pristine', 'A Grade'),

        # Grade B (good condition)
        (r'\bB\s*grade|grade\s*B|good\s*condition|fair\s*condition|used\s*good', 'B Grade'),

        # Grade C (poor condition)
        (r'\bC\s*grade|grade\s*C|poor\s*condition|rough\s*condition|heavily\s*used', 'C Grade'),

        # Grade D (very poor)
        (r'\bD\s*grade|grade\s*D|very\s*poor|bad\s*condition', 'D Grade'),

        # DOA (Dead on Arrival)
        (r'DOA|dead\s*on\s*arrival|not\s*working|doesn\'t\s*work|no\s*power', 'DOA'),

        # Cracked screens
        (r'cracked\s*screen|screen\s*cracked|broken\s*screen|shattered\s*screen|cracked\s*display', 'Cracked Screen'),

        # Cracked back
        (r'cracked\s*back|back\s*cracked|broken\s*back|back\s*glass\s*cracked', 'Cracked Back'),

        # Both screen and back cracked
        (r'cracked\s*screen.*cracked\s*back|both\s*cracked|screen\s*and\s*back\s*cracked', 'Cracked Screen & Back'),

        # Water damage
        (r'water\s*damage|liquid\s*damage|water\s*logged|got\s*wet', 'Water Damage'),

        # Other damage
        (r'broken|damaged|faulty|defective|not\s*functional', 'Damaged/Other')
    ]

    for pattern, grade_name in grade_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            grade = grade_name
            break

    return model, storage, grade

def extract_price(text: str) -> Optional[float]:
    """
    Enhanced price extraction
    """
    if not text or pd.isna(text):
        return None

    text = str(text)

    # Enhanced price patterns
    price_patterns = [
        r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $1,234.56
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|dollars?)',  # 1,234.56 USD
        r'\$(\d+(?:\.\d{2})?)',  # $123.45
        r'(\d+(?:\.\d{2})?)\s*(?:USD|dollars?)',  # 123.45 USD
        r'price[:\s]*(\d+(?:\.\d{2})?)',  # price: 123.45
        r'(\d{1,4})\s*(?:dollars?|bucks?)',  # 100 dollars
    ]

    for pattern in price_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            try:
                # Get the last (most likely) price match
                price_str = matches[-1].replace(',', '')
                price = float(price_str)
                # Filter out unrealistic prices
                if 0 < price < 10000:  # Reasonable range for electronics
                    return price
            except ValueError:
                continue

    return None

def clean_model_name(model: str, text: str) -> str:
    """
    Clean and enhance model name extraction
    """
    if not model:
        return ""

    # Try to extract better model info from the text
    text_lower = text.lower()

    # Look for specific model mentions
    if 'iphone' in text_lower:
        # Extract specific iPhone model
        iphone_match = re.search(r'iphone\s*([\w\s-]+)', text_lower)
        if iphone_match:
            potential_model = iphone_match.group(1).strip()
            # Clean up the model name
            if any(word in potential_model for word in ['pro', 'plus', 'max', 'mini', 'se', 'air']):
                model = f"iPhone {potential_model.title()}"
            elif potential_model.isdigit():
                model = f"iPhone {potential_model}"

    return model

def process_excel_file(file_path: str) -> List[Dict]:
    """
    Process Excel file with enhanced extraction
    """
    print(f"🔍 Processing {file_path} with enhanced extraction...")

    df = pd.read_excel(file_path)
    extracted_data = []

    for col in df.columns:
        print(f"   Processing column: {col}")

        for idx, value in enumerate(df[col]):
            if pd.notna(value) and value != "":
                text = str(value).strip()

                # Skip policy/address content
                skip_keywords = [
                    'office', 'address', 'please', 'due to', 'we buy', 'we don\'t',
                    'hong kong', 'verizon', 't-mobile', 'xfinity', 'receipt',
                    'minimum quantity', 'fedex shipping', 'blacklist', 'locked',
                    'unlocked', 'provide', 'ask us', 'contact'
                ]

                if any(keyword in text.lower() for keyword in skip_keywords):
                    continue

                # Only process if text looks like it contains device info
                device_keywords = [
                    'iphone', 'samsung', 'galaxy', 'ipad', 'macbook', 'apple',
                    'watch', 'airpods', 'pixel', 'oneplus', 'gb', 'tb', 'grade',
                    'sealed', 'cracked', 'broken', 'new', 'used', 'refurbished'
                ]

                if not any(keyword in text.lower() for keyword in device_keywords):
                    continue

                # Extract information
                model, storage, grade = extract_model_info(text)
                model = clean_model_name(model, text)
                price = extract_price(text)

                # Only include meaningful data
                if model or price:
                    extracted_data.append({
                        'model': model,
                        'storage': storage,
                        'grade': grade,
                        'price': price,
                        'raw_text': text[:100],  # Truncate for readability
                        'row': idx + 1,
                        'column': col
                    })

    return extracted_data

def save_to_csv(data: List[Dict], output_file: str):
    """
    Save enhanced data to CSV
    """
    print(f"💾 Saving {len(data)} enhanced records to {output_file}")

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['model', 'storage', 'grade', 'price', 'row', 'column']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Sort by model name for better readability
        data.sort(key=lambda x: (x['model'] or '', x['storage'] or ''))

        for item in data:
            writer.writerow({
                'model': item['model'],
                'storage': item['storage'],
                'grade': item['grade'],
                'price': item['price'],
                'row': item['row'],
                'column': item['column']
            })

    print(f"✅ Enhanced CSV file saved: {output_file}")

def main():
    """
    Main function with enhanced processing
    """
    input_file = "austin.xlsx"
    output_file = "austin_pricing_enhanced.csv"

    # Process the Excel file
    extracted_data = process_excel_file(input_file)

    # Save to CSV
    save_to_csv(extracted_data, output_file)

    # Enhanced summary
    print(f"\n📊 Enhanced Extraction Summary:")
    print(f"   Total records extracted: {len(extracted_data)}")

    if extracted_data:
        # Enhanced statistics
        grade_counts = {}
        storage_counts = {}
        model_counts = {}
        price_sum = 0
        price_count = 0

        for item in extracted_data:
            if item['grade']:
                grade_counts[item['grade']] = grade_counts.get(item['grade'], 0) + 1
            if item['storage']:
                storage_counts[item['storage']] = storage_counts.get(item['storage'], 0) + 1
            if item['model']:
                model_counts[item['model']] = model_counts.get(item['model'], 0) + 1
            if item['price']:
                price_sum += item['price']
                price_count += 1

        print(f"\n📈 Grade Distribution:")
        for grade, count in sorted(grade_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {grade:<25}: {count:3d} items")

        print(f"\n💾 Storage Distribution:")
        for storage, count in sorted(storage_counts.items(), key=lambda x: (len(x[0]), x[1]), reverse=True):
            print(f"   {storage:<10}: {count:3d} items")

        print(f"\n📱 Top Models:")
        sorted_models = sorted(model_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for model, count in sorted_models:
            print(f"   {model[:30]:<30}: {count:3d} items")

        if price_count > 0:
            print(f"\n💰 Price Summary:")
            print(f"   Items with prices: {price_count}")
            print(f"   Average price: ${price_sum/price_count:,.2f}")
            print(f"   Total value: ${price_sum:,.2f}")

            # Price range
            prices = [item['price'] for item in extracted_data if item['price']]
            if prices:
                print(f"   Price range: ${min(prices):,.2f} - ${max(prices):,.2f}")

if __name__ == "__main__":
    main()