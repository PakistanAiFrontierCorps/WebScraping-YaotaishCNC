#step 4

import pandas as pd
import os

df = pd.read_csv("./Output CSV\products.csv")

# Drop rows where any cell contains 'N/A'
# df_cleaned = df.replace("N/A", pd.NA).dropna()
df_cleaned = df
# Add 'Brand' column with all values set to 'Fanuc'
df_cleaned["Brands"] = "AB"

# Create the output folder if it doesn't exist
output_folder = "OutPut final"
os.makedirs(output_folder, exist_ok=True)

# Save the cleaned DataFrame
output_path = os.path.join(output_folder, "cleaned_file.csv")
df_cleaned.to_csv(output_path, index=False)

print(f"Cleaned file saved to: {output_path}")