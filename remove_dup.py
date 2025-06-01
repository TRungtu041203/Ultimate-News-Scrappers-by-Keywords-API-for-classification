import pandas as pd
import os

# Load the CSV file into a pandas DataFrame.
df = pd.read_csv(r"D:\Data\vietnews\output\dantri_20250530_184654.csv", encoding='utf-8-sig')
print("Original dataframe shape:", df.shape)

# Remove duplicate rows based on the 'link' column.
df_deduped = df.drop_duplicates(subset='Link', keep='first')
print("Dataframe shape after removing duplicates:", df_deduped.shape)

# Define the output folder name
output_dir = "cleaned_dataset"

# Create the folder if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Folder '{output_dir}' created.")

# Construct the full path for the output CSV file
output_file_path = os.path.join(output_dir, "dantri_20250530_184654_deduped.csv")

# Save the deduplicated DataFrame to the CSV file in the specified folder
df_deduped.to_csv(output_file_path, index=False, encoding='utf-8-sig')
print(f"Deduplicated CSV saved to: {output_file_path}")
