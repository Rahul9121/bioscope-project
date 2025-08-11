import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# Database credentials
DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'Marvin20nisan21.'

# Connect to PostgreSQL
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

# Step 1: Load Violation Counts from CSV
df_violations = pd.read_csv("violations_counts.csv")

# Step 2: Compute AHP Weights
total_violations = df_violations["Violation Count"].sum()
df_violations["Weight"] = df_violations["Violation Count"] / total_violations  # Normalize

# Construct AHP Pairwise Comparison Matrix
ahp_matrix = np.array([
    [1, df_violations.loc[df_violations["Category"] == "Freshwater", "Weight"].values[0] /
     df_violations.loc[df_violations["Category"] == "Marine", "Weight"].values[0],
     df_violations.loc[df_violations["Category"] == "Freshwater", "Weight"].values[0] /
     df_violations.loc[df_violations["Category"] == "Terrestrial", "Weight"].values[0]],

    [df_violations.loc[df_violations["Category"] == "Marine", "Weight"].values[0] /
     df_violations.loc[df_violations["Category"] == "Freshwater", "Weight"].values[0], 1,
     df_violations.loc[df_violations["Category"] == "Marine", "Weight"].values[0] /
     df_violations.loc[df_violations["Category"] == "Terrestrial", "Weight"].values[0]],

    [df_violations.loc[df_violations["Category"] == "Terrestrial", "Weight"].values[0] /
     df_violations.loc[df_violations["Category"] == "Freshwater", "Weight"].values[0],
     df_violations.loc[df_violations["Category"] == "Terrestrial", "Weight"].values[0] /
     df_violations.loc[df_violations["Category"] == "Marine", "Weight"].values[0], 1]
])

# Compute the Eigenvector (Priority Weights)
eigvals, eigvecs = np.linalg.eig(ahp_matrix)
max_eigval = np.max(eigvals)
priority_vector = eigvecs[:, np.argmax(eigvals)].real
priority_vector = priority_vector / np.sum(priority_vector)  # Normalize

# Store the final AHP weights in a DataFrame
ahp_results = pd.DataFrame({
    "Category": ["Freshwater", "Marine", "Terrestrial"],
    "Final AHP Weight": priority_vector
})

# Save AHP Weights to Database
ahp_results.to_sql('ahp_weights', engine, if_exists='replace', index=False)
print("✅ AHP Weights Saved to Database!")
print(ahp_results)
