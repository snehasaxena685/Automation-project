from openpyxl import load_workbook
from datetime import datetime

# Set the path to your Excel file
excel_path = "Live_Herbarium_Log.xlsx"

# Step 1: Take Input
specimen_id = input("Enter Specimen ID: ")
herb_name = input("Enter Herb Name: ")
scientific_name = input("Enter Scientific Name: ")
region = input("Enter Region: ")
weight = input("Enter Weight (grams): ")

# Auto-generate collection date
collection_date = datetime.today().strftime("%Y-%m-%d")

# Step 2: Classify Priority
high_priority_regions = ["Delhi", "Punjab", "Uttar Pradesh"]
priority = "High" if region in high_priority_regions else "Low"

# Step 3: Load and update Excel
wb = load_workbook(excel_path)
sheet = wb.active

# Append the new row
new_row = [
    specimen_id,
    herb_name,
    scientific_name,
    collection_date,
    region,
    weight,
    priority
]
sheet.append(new_row)

# Step 4: Save Excel
wb.save(excel_path)

print("\n✅ Entry saved successfully to Excel!")
