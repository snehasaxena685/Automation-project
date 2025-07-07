import re
import pandas as pd

# Read the OCR output
with open("ocr_output_rhmd.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Split entries (based on assumption that each starts with serial number or scientific name)
# You might need to tune this depending on how OCR extracted the structure
entries = re.split(r"\n(?=[A-Z][a-z]+\s+[a-z]+)", text)

# Initialize data list
data = []

# Simple parsing attempt (you may adjust patterns as needed)
for entry in entries:
    lines = entry.strip().split("\n")
    if len(lines) < 3:
        continue

    common_name = lines[0].strip()
    scientific_name = lines[1].strip()
    plant_part = ""
    family = ""
    region = ""
    auth_code = ""

    for line in lines[2:]:
        if "Part Used" in line:
            plant_part = line.split(":")[-1].strip()
        elif "Family" in line:
            family = line.split(":")[-1].strip()
        elif "Institute" in line:
            region = line.strip()
        elif "RHMD-" in line:
            auth_code = line.strip()

    data.append({
        "Common Name": common_name,
        "Scientific Name": scientific_name,
        "Plant Part Used": plant_part,
        "Family": family,
        "Region/Institute": region,
        "Authentication Code": auth_code
    })

# Create DataFrame and save
df = pd.DataFrame(data)
df.to_csv("rhmd_herbs.csv", index=False)

print("✅ Extracted herb data saved to rhmd_herbs.csv")
