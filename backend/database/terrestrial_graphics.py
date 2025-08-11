import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your updated dataset (change path if needed)
df = pd.read_csv("terrestrial_risk_updated.csv")

# 🔹 Plot 1: Histogram of Normalized Risk
plt.figure(figsize=(8, 5))
plt.hist(df["normalized_risk"], bins=30, edgecolor="black", color="#6A1B9A")
plt.xlabel("Normalized Risk Score")
plt.ylabel("Frequency")
plt.title("Distribution of Normalized Terrestrial Risk")
plt.tight_layout()
plt.show()

# 🔹 Plot 2: Risk Level Count Bar
plt.figure(figsize=(6, 4))
df["risk_level"].value_counts().reindex(["Low", "Moderate", "High"]).plot(kind="bar", color=["green", "orange", "red"])
plt.title("Risk Level Classification")
plt.ylabel("Count")
plt.xlabel("Risk Level")
plt.tight_layout()
plt.show()

# 🔹 Plot 3: Correlation Heatmap (Top 10 most correlated features)
correlation_matrix = df.corr(numeric_only=True)
top_features = correlation_matrix["terrestrial_hci"].abs().sort_values(ascending=False)[1:11].index

plt.figure(figsize=(10, 8))
heatmap_data = df[top_features].corr()
plt.imshow(heatmap_data, cmap="coolwarm", interpolation="none")
plt.colorbar(label="Correlation Coefficient")
plt.xticks(ticks=np.arange(len(top_features)), labels=top_features, rotation=90)
plt.yticks(ticks=np.arange(len(top_features)), labels=top_features)
plt.title("Top Correlated Features with Terrestrial HCI")
plt.tight_layout()
plt.show()
