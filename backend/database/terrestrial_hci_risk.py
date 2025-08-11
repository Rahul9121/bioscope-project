# STEP 1: Load terrestrial dataset
import pandas as pd
import numpy as np
df = pd.read_csv("terrestrial_human_coexistence_nj.csv")

# STEP 2: Drop rows with missing terrestrial_hci (target)
df = df.dropna(subset=["terrestrial_hci"])

# STEP 3: Fill missing numeric values with median
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# STEP 4: Select features for correlation
features = [col for col in numeric_cols if col != "terrestrial_hci"]
correlation_matrix = df[["terrestrial_hci"] + features].corr()

# STEP 5: Compute AHP weights based on absolute correlation with terrestrial_hci
abs_corr = correlation_matrix["terrestrial_hci"].abs().drop("terrestrial_hci")
weights = abs_corr / abs_corr.sum()

# STEP 6: Compute weighted risk score
df["weighted_risk"] = sum(df[feat] * weights[feat] for feat in features)

# STEP 7: Assign fallback risk for rows with all zero inputs
zero_rows = (df[features] == 0).all(axis=1)
baseline_risk = df["weighted_risk"].median() * 0.3
df.loc[zero_rows, "weighted_risk"] = baseline_risk

# STEP 8: Normalize using square root transform + percentile clipping
df["transformed_risk"] = np.sqrt(df["weighted_risk"])
q20, q80 = df["transformed_risk"].quantile([0.2, 0.8])
df["normalized_risk"] = (df["transformed_risk"] - q20) / (q80 - q20)
df["normalized_risk"] = df["normalized_risk"].clip(0, 1)

# STEP 9: Classify risk level
def classify(score):
    if score > 0.25:
        return "High"
    elif score > 0.05:
        return "Moderate"
    else:
        return "Low"
df["risk_level"] = df["normalized_risk"].apply(classify)

# STEP 10: Save results
df.to_csv("terrestrial_risk_updated.csv", index=False)
weights.to_csv("terrestrial_ahp_weights.csv")
correlation_matrix.to_csv("terrestrial_correlation_matrix.csv")
