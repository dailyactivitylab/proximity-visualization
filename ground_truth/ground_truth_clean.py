import pandas as pd

file_path = "include/your/file/path"  
df = pd.read_csv(file_path, header=None)

# Define column names without replacing the first row
df.columns = ["Column1", "Column2", "Distress_Level"]

# Add a new column based on the third column's values
df["Distress_Status"] = df["Distress_Level"].apply(lambda x: "No Distress" if x == 0 else "Distress")

# Save the updated CSV file
updated_file_path = "include/your/file/path"
df.to_csv(updated_file_path, index=False)

print(f"Updated CSV saved as: {updated_file_path}")