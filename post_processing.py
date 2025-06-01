import pandas as pd

# Read the original CSV file into a DataFrame
original_df = pd.read_csv(r"D:\Data\vietnews\src\classified_data\categorized_articles_20250408_162314.csv", encoding='utf-8-sig')

# Create a new dataframe by making a copy of the original data
new_df = original_df.copy()

# Remove rows where the Categories column is NaN or exactly the string "None"
new_df = new_df[new_df['Categories'].notna() & (new_df['Categories'] != 'None')]

# Define a mapping dictionary to replace numeric categories with full text descriptions
mapping = {
    '1': "Tổng quan ngành video games tại Việt Nam",
    '2': "Việc phát triển games tại Việt Nam, green gaming, và bảo vệ môi trường",
    '3': "Việc phát triển games và sử dụng công cụ AIs",
    '4': "Esports in Vietnam",
    1: "Tổng quan ngành video games tại Việt Nam",
    2: "Việc phát triển games tại Việt Nam, green gaming, và bảo vệ môi trường",
    3: "Việc phát triển games và sử dụng công cụ AIs",
    4: "Esports in Vietnam"
}

# Define the valid categories (both numeric and text formats)
valid_categories = list(mapping.keys()) + list(mapping.values())

# Filter to keep only rows with valid categories
print(f"Original number of rows: {len(new_df)}")
new_df = new_df[new_df['Categories'].isin(valid_categories)]
print(f"Rows after filtering for valid categories: {len(new_df)}")

# Replace numeric values in the Categories column using the mapping dictionary
new_df['Categories'] = new_df['Categories'].replace(mapping)

# Display the first few rows of the modified dataframe
print("\nFirst few rows of cleaned data:")
print(new_df.head())

# Display the count of each category
print("\nCategory distribution:")
print(new_df['Categories'].value_counts())

# Export the cleaned data to a new CSV file
new_df.to_csv(r"D:\Data\vietnews\src\classified_data\categorized_articles_cleaned.csv", index=False, encoding='utf-8-sig')

print(f"\nCleaned data saved to: categorized_articles_tinhte_20250530_191010_cleaned.csv")
