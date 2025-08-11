import pandas as pd
import numpy as np


# Load your freshwater dataset
file_path = "freshwater_hci.csv"  # Change this to your actual file path
df = pd.read_csv(file_path)

# Fill missing values with column medians
df.fillna(df.median(), inplace=True)

# Select relevant columns for correlation analysis
correlation_columns = ["freshwater_hci", "popden2010", "maxrdd", "meanuse", "maxdof", "mincsi", "maxsed"]

# Compute the correlation matrix
correlation_matrix = df[correlation_columns].corr()

# Display the correlation matrix
print("🔹 Correlation Matrix:")
print(correlation_matrix)

# Save correlation matrix as CSV
correlation_matrix.to_csv("correlation_matrix.csv")

# Extract absolute correlation values for weighting
abs_corr = correlation_matrix["freshwater_hci"].abs()

# Normalize to sum to 1 (relative importance via AHP)
freshwater_ahp_weights = abs_corr / abs_corr.sum()

# Print and save AHP weights
print("🔹 Computed AHP Weights Based on Correlation:")
print(freshwater_ahp_weights)
freshwater_ahp_weights.to_csv("freshwater_ahp_weights.csv")

# Compute weighted risk score using AHP weights
df["weighted_risk"] = (
    freshwater_ahp_weights["freshwater_hci"] * df["freshwater_hci"] +
    freshwater_ahp_weights["popden2010"] * df["popden2010"] +
    freshwater_ahp_weights["maxrdd"] * df["maxrdd"] +
    freshwater_ahp_weights["meanuse"] * df["meanuse"] +
    freshwater_ahp_weights["meanuse"] * df["meanuse"] +
    freshwater_ahp_weights["maxdof"] * df["maxdof"] +
    freshwater_ahp_weights["mincsi"] * df["mincsi"] +
    freshwater_ahp_weights["maxsed"] * df["maxsed"]
)

# 🔍 Handle cases where all values in a row are 0 (baseline risk)
zero_rows = (df[["popden2010", "maxrdd", "meanuse", "maxdof", "mincsi", "maxsed"]] == 0).all(axis=1)
baseline_risk = df["weighted_risk"].median() * 0.3  # 30% of median risk

df.loc[zero_rows, "weighted_risk"] = baseline_risk  # Assign baseline risk for zero-impact rows

# 🔍 Apply log transformation before normalizing
df["log_weighted_risk"] = np.log1p(df["weighted_risk"])

# Compute min/max for normalization
min_log_risk = df["log_weighted_risk"].min()
max_log_risk = df["log_weighted_risk"].max()

# Apply a power transformation to stretch smaller values upward
df["transformed_risk"] = np.sqrt(df["weighted_risk"])

q20, q80 = df["transformed_risk"].quantile([0.20, 0.80])

df["normalized_risk"] = (df["transformed_risk"] - q20) / (q80 - q20)
df["normalized_risk"] = df["normalized_risk"].clip(0, 1)





# Define risk levels based on thresholds
def classify_risk_level(score):
    if score > 0.25:
        return "High"
    elif score > 0.05:
        return "Moderate"
    else:
        return "Low"

df["risk_level"] = df["normalized_risk"].apply(classify_risk_level)

# 🔍 Print min/max risk values to check scaling
print(f"Min Weighted Risk: {df['weighted_risk'].min()}, Max Weighted Risk: {df['weighted_risk'].max()}")

# Print first few rows
print(df[["x", "y", "normalized_risk", "risk_level"]].head())

# Save updated dataset
df.to_csv("freshwater_risk_updated.csv", index=False)

import matplotlib.pyplot as plt

plt.hist(df["normalized_risk"], bins=30, edgecolor="black")
plt.xlabel("Normalized Risk Score")
plt.ylabel("Frequency")
plt.title("Distribution of Freshwater Risk Levels")
plt.show()


df["risk_level"].value_counts()

