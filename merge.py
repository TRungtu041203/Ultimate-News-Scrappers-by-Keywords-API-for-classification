import pandas as pd

# Read each deduplicated CSV file into a DataFrame
df1 = pd.read_csv(r"D:\Data\vietnews\src\classified_data\categorized_articles_cleaned_2.csv")
df2 = pd.read_csv(r"D:\Data\vietnews\src\classified_data\categorized_articles_cleaned.csv")
#df3 = pd.read_csv(r"D:\Data\vietnews\src\cleaned_dataset\viresa_api_20250408_020904_deduped.csv")
#df4 = pd.read_csv(r"D:\Data\vietnews\src\cleaned_dataset\vnexpress_news_20250327_170102.csv")

# Concatenate all DataFrames into one
merged_df = pd.concat([df1, df2], ignore_index=True)

# (Optional) If you'd like to remove any duplicates across the combined data
# based on a column like 'link', uncomment the line below:
# merged_df.drop_duplicates(subset='link', keep='first', inplace=True)

#drop collumns "No"
merged_df.drop(columns=["No"], inplace=True, errors='ignore')
# Save the merged dataset to a new CSV file
merged_df.to_csv('final_data.csv', index=False, encoding='utf-8-sig')

print("Merged data saved as merged_data.csv")
print("Merged data shape:", merged_df.shape)
print("Merged data columns:", merged_df.columns.tolist())