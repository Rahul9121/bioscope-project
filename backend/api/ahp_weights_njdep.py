import pdfplumber
import pandas as pd
import re

# Path to the enforcement PDF file
pdf_path = "static/Enforcement_Actions_Issued_By_Program_and_Date.pdf"  # Update with the correct file path

# Define keywords for each risk category
categories = {
    "Freshwater": ["Water Quality", "Stormwater", "Drinking Water", "Wastewater"],
    "Marine": ["Marine", "Coastal", "Oil Spill", "Waterway Enforcement"],
    "Terrestrial": ["Land Use", "Deforestation", "Habitat", "Soil Contamination"]
}

# Initialize violation count dictionary
violation_counts = {category: 0 for category in categories}

# Extract text from the PDF
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            # Count violations for each category
            for category, keywords in categories.items():
                violation_counts[category] += sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)

# Save violation counts to CSV for AHP calculations
df_violations = pd.DataFrame(list(violation_counts.items()), columns=["Category", "Violation Count"])
df_violations.to_csv("violations_counts.csv", index=False)

# Print results
print(df_violations)
