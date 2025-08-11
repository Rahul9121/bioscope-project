#!/usr/bin/env python3
"""
Script to create sample data files for missing large datasets.
This is for development and testing purposes.
"""

import pandas as pd
import numpy as np
import os

def create_sample_data():
    """Create sample data files for development"""
    
    # Create sample_data directory if it doesn't exist
    sample_dir = 'backend/database/sample_data'
    os.makedirs(sample_dir, exist_ok=True)
    
    # Generate sample coordinates around New Jersey
    nj_lat_range = (39.0, 41.5)
    nj_lon_range = (-75.5, -73.9)
    
    # Sample IUCN data
    species_list = [
        "American Robin", "Blue Jay", "Red Cardinal", "Bald Eagle", "Great Blue Heron",
        "Eastern Bluebird", "Wood Duck", "Mallard", "Canada Goose", "Red-winged Blackbird"
    ]
    
    threat_statuses = [
        "Least Concern", "Near Threatened", "Vulnerable", "Endangered", "Critically Endangered"
    ]
    
    n_records = 1000
    
    iucn_data = {
        'latitude': np.random.uniform(nj_lat_range[0], nj_lat_range[1], n_records),
        'longitude': np.random.uniform(nj_lon_range[0], nj_lon_range[1], n_records),
        'species_name': np.random.choice(species_list, n_records),
        'threat_status': np.random.choice(threat_statuses, n_records, 
                                         p=[0.5, 0.25, 0.15, 0.08, 0.02]),
        'habitat': np.random.choice(['Forest', 'Wetland', 'Urban', 'Grassland', 'Marine'], n_records)
    }
    
    iucn_df = pd.DataFrame(iucn_data)
    iucn_df.to_csv(f'{sample_dir}/cleaned_IUCN_data_sample.csv', index=False)
    print(f"Created cleaned_IUCN_data_sample.csv with {n_records} records")
    
    # Sample marine risk data
    marine_data = {
        'x': np.random.uniform(nj_lon_range[0], nj_lon_range[1], 500),
        'y': np.random.uniform(nj_lat_range[0], nj_lat_range[1], 500),
        'marine_hci': np.random.uniform(0.1, 0.9, 500)
    }
    
    marine_df = pd.DataFrame(marine_data)
    marine_df.to_csv(f'{sample_dir}/marine_risk_updated_sample.csv', index=False)
    print(f"Created marine_risk_updated_sample.csv with 500 records")
    
    # Sample terrestrial coexistence data
    terrestrial_data = {
        'x': np.random.uniform(nj_lon_range[0], nj_lon_range[1], 800),
        'y': np.random.uniform(nj_lat_range[0], nj_lat_range[1], 800),
        'hci_score': np.random.uniform(0.2, 0.95, 800),
        'risk_category': np.random.choice(['Low', 'Moderate', 'High'], 800, p=[0.4, 0.4, 0.2])
    }
    
    terrestrial_df = pd.DataFrame(terrestrial_data)
    terrestrial_df.to_csv(f'{sample_dir}/terrestrial_human_coexistence_nj_sample.csv', index=False)
    print(f"Created terrestrial_human_coexistence_nj_sample.csv with 800 records")
    
    print("\n✅ Sample data files created successfully!")
    print(f"📁 Location: {sample_dir}/")
    print("\n📝 Note: These are sample files for development.")
    print("   For production, replace with actual large datasets.")

if __name__ == "__main__":
    create_sample_data()
