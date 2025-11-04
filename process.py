#!/usr/bin/env python3
import csv
import re
from typing import Dict, List, Optional

def identify_phone_model(title: str) -> str:
    """
    Use pattern matching and rules to identify the phone model from the title.
    This simulates AI-based model identification using rule-based approach.
    """
    title = title.lower().strip()

    # iPhone model patterns
    iphone_patterns = {
        'iPhone 16 Pro Max': r'iphone\s*16\s*pro\s*max|16\s*pro\s*max',
        'iPhone 16 Pro': r'iphone\s*16\s*pro|16\s*pro',
        'iPhone 16 Plus': r'iphone\s*16\s*plus|16\s*plus',
        'iPhone 16': r'iphone\s*16\b|(?<!pro\s)16\b(?!\s*plus)',
        'iPhone 16 Air': r'iphone\s*16\s*air|16\s*air|air\s*16',
        'iPhone 15 Pro Max': r'iphone\s*15\s*pro\s*max|15\s*pro\s*max',
        'iPhone 15 Pro': r'iphone\s*15\s*pro|15\s*pro',
        'iPhone 15 Plus': r'iphone\s*15\s*plus|15\s*plus',
        'iPhone 15': r'iphone\s*15\b|(?<!pro\s)15\b(?!\s*plus)',
        'iPhone 15 Air': r'iphone\s*15\s*air|15\s*air|air\s*15',
        'iPhone 14 Pro Max': r'iphone\s*14\s*pro\s*max|14\s*pro\s*max',
        'iPhone 14 Pro': r'iphone\s*14\s*pro|14\s*pro',
        'iPhone 14 Plus': r'iphone\s*14\s*plus|14\s*plus',
        'iPhone 14': r'iphone\s*14\b|(?<!pro\s)14\b(?!\s*plus)',
        'iPhone 14 Air': r'iphone\s*14\s*air|14\s*air|air\s*14',
        'iPhone 13 Pro Max': r'iphone\s*13\s*pro\s*max|13\s*pro\s*max',
        'iPhone 13 Pro': r'iphone\s*13\s*pro|13\s*pro',
        'iPhone 13 mini': r'iphone\s*13\s*mini|13\s*mini',
        'iPhone 13': r'iphone\s*13\b|(?<!pro\s)13\b(?!\s*mini)',
        'iPhone 13 Air': r'iphone\s*13\s*air|13\s*air|air\s*13',
        'iPhone 12 Pro Max': r'iphone\s*12\s*pro\s*max|12\s*pro\s*max',
        'iPhone 12 Pro': r'iphone\s*12\s*pro|12\s*pro',
        'iPhone 12 mini': r'iphone\s*12\s*mini|12\s*mini',
        'iPhone 12': r'iphone\s*12\b|(?<!pro\s)12\b(?!\s*mini)',
        'iPhone 12 Air': r'iphone\s*12\s*air|12\s*air|air\s*12',
        'iPhone 11 Pro Max': r'iphone\s*11\s*pro\s*max|11\s*pro\s*max',
        'iPhone 11 Pro': r'iphone\s*11\s*pro|11\s*pro',
        'iPhone 11': r'iphone\s*11\b',
        'iPhone 11 Air': r'iphone\s*11\s*air|11\s*air|air\s*11',
        'iPhone X Air': r'iphone\s*x\s*air|x\s*air|air\s*x',
        'iPhone Air': r'iphone\s*air\b|air\b(?!.*pro|.*max|.*plus|.*mini)',
        'iPhone SE': r'iphone\s*se|se\s*\d*\s*gen|se\s*\d*\s*generation',
    }

    # Check iPhone patterns first (most specific to least specific)
    for model, pattern in iphone_patterns.items():
        if re.search(pattern, title):
            return model

    # Samsung Galaxy patterns
    samsung_patterns = {
        'Galaxy S24 Ultra': r'galaxy\s*s24\s*ultra|s24\s*ultra',
        'Galaxy S24+': r'galaxy\s*s24\s*\+|s24\+|s24\s*plus',
        'Galaxy S24': r'galaxy\s*s24\b|(?!\+|ultra)s24\b',
        'Galaxy S23 Ultra': r'galaxy\s*s23\s*ultra|s23\s*ultra',
        'Galaxy S23+': r'galaxy\s*s23\s*\+|s23\+|s23\s*plus',
        'Galaxy S23': r'galaxy\s*s23\b|(?!\+|ultra)s23\b',
        'Galaxy S22 Ultra': r'galaxy\s*s22\s*ultra|s22\s*ultra',
        'Galaxy S22+': r'galaxy\s*s22\s*\+|s22\+|s22\s*plus',
        'Galaxy S22': r'galaxy\s*s22\b|(?!\+|ultra)s22\b',
        'Galaxy S21 Ultra': r'galaxy\s*s21\s*ultra|s21\s*ultra',
        'Galaxy S21+': r'galaxy\s*s21\s*\+|s21\+|s21\s*plus',
        'Galaxy S21': r'galaxy\s*s21\b|(?!\+|ultra)s21\b',
        'Galaxy S20 Ultra': r'galaxy\s*s20\s*ultra|s20\s*ultra',
        'Galaxy S20+': r'galaxy\s*s20\s*\+|s20\+|s20\s*plus',
        'Galaxy S20': r'galaxy\s*s20\b|(?!\+|ultra)s20\b',
        'Galaxy Z Fold 6': r'galaxy\s*z\s*fold\s*6|z\s*fold\s*6|fold\s*6',
        'Galaxy Z Fold 5': r'galaxy\s*z\s*fold\s*5|z\s*fold\s*5|fold\s*5',
        'Galaxy Z Fold 4': r'galaxy\s*z\s*fold\s*4|z\s*fold\s*4|fold\s*4',
        'Galaxy Z Fold 3': r'galaxy\s*z\s*fold\s*3|z\s*fold\s*3|fold\s*3',
        'Galaxy Z Flip 5': r'galaxy\s*z\s*flip\s*5|z\s*flip\s*5|flip\s*5',
        'Galaxy Z Flip 4': r'galaxy\s*z\s*flip\s*4|z\s*flip\s*4|flip\s*4',
        'Galaxy Z Flip 3': r'galaxy\s*z\s*flip\s*3|z\s*flip\s*3|flip\s*3',
        'Galaxy Note 20 Ultra': r'galaxy\s*note\s*20\s*ultra|note\s*20\s*ultra',
        'Galaxy Note 20': r'galaxy\s*note\s*20\b|note\s*20\b',
        'Galaxy Note 10+': r'galaxy\s*note\s*10\s*\+|note\s*10\s*\+|note\s*10\s*plus',
        'Galaxy Note 10': r'galaxy\s*note\s*10\b|note\s*10\b',
        'Galaxy A54': r'galaxy\s*a54|a54',
        'Galaxy A53': r'galaxy\s*a53|a53',
        'Galaxy A52': r'galaxy\s*a52|a52',
    }

    for model, pattern in samsung_patterns.items():
        if re.search(pattern, title):
            return model

    # Google Pixel patterns
    pixel_patterns = {
        'Pixel 8 Pro': r'pixel\s*8\s*pro|8\s*pro',
        'Pixel 8': r'pixel\s*8\b',
        'Pixel 7 Pro': r'pixel\s*7\s*pro|7\s*pro',
        'Pixel 7': r'pixel\s*7\b',
        'Pixel 6 Pro': r'pixel\s*6\s*pro|6\s*pro',
        'Pixel 6': r'pixel\s*6\b',
    }

    for model, pattern in pixel_patterns.items():
        if re.search(pattern, title):
            return model

    # MacBook patterns
    macbook_patterns = {
        'MacBook Pro 16-inch': r'macbook\s*pro\s*16|16\s*macbook\s*pro',
        'MacBook Pro 15-inch': r'macbook\s*pro\s*15|15\s*macbook\s*pro',
        'MacBook Pro 14-inch': r'macbook\s*pro\s*14|14\s*macbook\s*pro',
        'MacBook Pro 13-inch': r'macbook\s*pro\s*13|13\s*macbook\s*pro',
        'MacBook Air 15-inch': r'macbook\s*air\s*15|15\s*macbook\s*air',
        'MacBook Air 13-inch': r'macbook\s*air\s*13|13\s*macbook\s*air',
        'MacBook Air 12-inch': r'macbook\s*air\s*12|12\s*macbook\s*air',
        'MacBook Pro': r'macbook\s*pro(?!\s*\d+)|mbp',
        'MacBook Air': r'macbook\s*air(?!\s*\d+)|mba',
        'MacBook': r'macbook\b(?!.*pro|.*air)',
    }

    for model, pattern in macbook_patterns.items():
        if re.search(pattern, title):
            return model

    # iPad patterns
    ipad_patterns = {
        'iPad Pro 12.9-inch': r'ipad\s*pro\s*12\.9|12\.9.*ipad.*pro|ipad.*pro.*12\.9',
        'iPad Pro 11-inch': r'ipad\s*pro\s*11|11.*ipad.*pro|ipad.*pro.*11',
        'iPad Pro 10.5-inch': r'ipad\s*pro\s*10\.5|10\.5.*ipad.*pro|ipad.*pro.*10\.5',
        'iPad Air': r'ipad\s*air|air.*ipad',
        'iPad mini': r'ipad\s*mini|mini.*ipad',
        'iPad 10th Gen': r'ipad\s*10|10th.*gen.*ipad|ipad.*10th.*gen',
        'iPad 9th Gen': r'ipad\s*9|9th.*gen.*ipad|ipad.*9th.*gen',
        'iPad 8th Gen': r'ipad\s*8|8th.*gen.*ipad|ipad.*8th.*gen',
        'iPad': r'ipad\b(?!.*pro|.*air|.*mini|.*gen)',
    }

    for model, pattern in ipad_patterns.items():
        if re.search(pattern, title):
            return model

    # Other brands
    other_patterns = {
        'OnePlus 12': r'oneplus\s*12|12\s*pro',
        'OnePlus 11': r'oneplus\s*11|11\s*pro',
        'OnePlus 10': r'oneplus\s*10|10\s*pro',
        'Nothing Phone (2)': r'nothing\s*phone\s*2|nothing\s*2',
        'Nothing Phone (1)': r'nothing\s*phone|nothing\s*1',
        'Sony Xperia 1 V': r'xperia\s*1\s*v|xperia\s*1\s*5',
        'Sony Xperia 5 V': r'xperia\s*5\s*v|xperia\s*5\s*5',
    }

    for model, pattern in other_patterns.items():
        if re.search(pattern, title):
            return model

    # Generic iPhone detection (if specific models not found)
    if 'iphone' in title:
        return 'iPhone (Unknown Model)'

    # Generic Samsung detection
    if 'galaxy' in title or 'samsung' in title:
        return 'Samsung (Unknown Model)'

    # Generic MacBook detection
    if 'macbook' in title:
        return 'MacBook (Unknown Model)'

    # Generic iPad detection
    if 'ipad' in title:
        return 'iPad (Unknown Model)'

    # Generic detection
    if any(brand in title for brand in ['pixel', 'oneplus', 'nothing', 'xperia', 'lg', 'motorola']):
        return 'Other Smartphone'

    return 'Unknown'

def process_csv(input_file: str, output_file: str) -> None:
    """
    Process the CSV file and add a 'Model' column with AI-detected phone models.
    """
    print(f"Processing {input_file}...")

    # Read the original CSV
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Add 'Model' to fieldnames if not present
    if 'Model' not in fieldnames:
        fieldnames.append('Model')

    # Process each row and identify the model
    processed_rows = []
    model_counts = {}

    for i, row in enumerate(rows, 1):
        title = row.get('Title', '')
        model = identify_phone_model(title)
        row['Model'] = model
        processed_rows.append(row)

        # Count models
        model_counts[model] = model_counts.get(model, 0) + 1

        print(f"Row {i}/{len(rows)}: {title[:50]}... -> {model}")

    # Write the processed CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_rows)

    # Print statistics
    print(f"\nProcessing complete! Output saved to: {output_file}")
    print(f"\nModel distribution:")
    for model, count in sorted(model_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {model}: {count}")

def main():
    """
    Main function to process the CSV file.
    """
    input_file = 'public/191_listings.csv'
    output_file = 'public/191_listings_with_models.csv'

    try:
        process_csv(input_file, output_file)
        print(f"\n✅ Success! The file '{output_file}' now contains AI-detected phone models.")
        print("📊 You can now update your React app to use this new CSV file.")
    except FileNotFoundError:
        print(f"❌ Error: Could not find input file '{input_file}'")
        print("Make sure the 191_listings.csv file exists in the public folder.")
    except Exception as e:
        print(f"❌ Error processing file: {e}")

if __name__ == "__main__":
    main()