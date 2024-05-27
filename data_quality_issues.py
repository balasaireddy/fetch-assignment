# To evaluate data quality issues in the provided JSON data, I am using Python with the Pandas library to load and explore the data. 

import pandas as pd
import json
from datetime import datetime

# Function to read a JSON file line by line and load each line as a JSON object
def load_json_lines(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# Load the data from JSON files
receipts_data = load_json_lines('D:\\receipts.json')
users_data = load_json_lines('D:\\users.json')
brands_data = load_json_lines('D:\\brands.json')

# Verify the number of records read
print(f"Number of records in receipts_data: {len(receipts_data)}")
print(f"Number of records in users_data: {len(users_data)}")
print(f"Number of records in brands_data: {len(brands_data)}")

# Convert JSON data to Pandas DataFrames
receipts_df = pd.json_normalize(receipts_data)
users_df = pd.json_normalize(users_data)
brands_df = pd.json_normalize(brands_data)

# Display basic information about each DataFrame
print("Receipts DataFrame Info:")
print(receipts_df.info())
print("\nUsers DataFrame Info:")
print(users_df.info())
print("\nBrands DataFrame Info:")
print(brands_df.info())

# Check for missing values
print("\nMissing Values in Receipts DataFrame:")
print(receipts_df.isnull().sum())
print("\nMissing Values in Users DataFrame:")
print(users_df.isnull().sum())
print("\nMissing Values in Brands DataFrame:")
print(brands_df.isnull().sum())

# Check for duplicate entries, excluding columns with unhashable types
receipts_subset = receipts_df.drop(columns=['rewardsReceiptItemList'])
print("\nDuplicate Entries in Receipts DataFrame:")
print(receipts_subset.duplicated().sum())
print("\nDuplicate Entries in Users DataFrame:")
print(users_df.duplicated().sum())
print("\nDuplicate Entries in Brands DataFrame:")
print(brands_df.duplicated().sum())

# Check for unique values in key columns
print("\nUnique User IDs in Receipts DataFrame:")
print(receipts_df['userId'].nunique())
print("\nUnique IDs in Users DataFrame:")
print(users_df['_id.$oid'].nunique())
print("\nUnique Barcodes in Brands DataFrame:")
print(brands_df['barcode'].nunique())

# Convert date fields to datetime and check for any parsing errors
date_fields = ['createDate.$date', 'dateScanned.$date', 'finishedDate.$date', 'modifyDate.$date', 'pointsAwardedDate.$date', 'purchaseDate.$date']
for field in date_fields:
    receipts_df[field] = pd.to_datetime(receipts_df[field], errors='coerce', unit='ms')

print("\nReceipts DataFrame after Date Parsing Errors Check:")
print(receipts_df[date_fields].isnull().sum())

# Validate reward receipt status values
print("\nUnique Values in rewardsReceiptStatus:")
print(receipts_df['rewardsReceiptStatus'].unique())

# Validate 'pointsEarned' and 'totalSpent' fields are numeric
receipts_df['pointsEarned'] = pd.to_numeric(receipts_df['pointsEarned'], errors='coerce')
receipts_df['totalSpent'] = pd.to_numeric(receipts_df['totalSpent'], errors='coerce')

print("\nNon-numeric Values in 'pointsEarned' Field:")
print(receipts_df[receipts_df['pointsEarned'].isnull()]['pointsEarned'])
print("\nNon-numeric Values in 'totalSpent' Field:")
print(receipts_df[receipts_df['totalSpent'].isnull()]['totalSpent'])


# FINDINGS:

# Missing Values:
# Check for any missing values across all dataframes. The output will show the count of missing values for each column.

# Duplicate Entries:
# Verify if there are any duplicate entries in the dataframes. This ensures data consistency and uniqueness.

# Unique Values:
# Ensure that key fields like user IDs and barcodes are unique across the respective dataframes.

# Date Parsing Errors:
# Convert date fields to datetime objects and check for any parsing errors. This helps identify any malformed date entries.

# Data Type Validations:
# Ensure that fields like pointsEarned and totalSpent are numeric and do not contain any invalid values.

# Status Validation:
# Validate the values in the rewardsReceiptStatus field to ensure they are consistent with expected values.

# DATA QUALITY ISSUES IDENTIFIED: 

# Missing Values:
# Identify columns with missing values and determine the impact on analysis.

# Duplicate Entries:
# Identify and handle any duplicate entries to maintain data integrity.

# Date Parsing Errors:
# Identify and correct any date parsing errors to ensure accurate date-based analysis.

# Invalid Numeric Values:
# Identify and correct any non-numeric values in fields that are expected to be numeric.

# Unexpected Status Values:
# Identify any unexpected values in the rewardsReceiptStatus field to ensure data consistency.