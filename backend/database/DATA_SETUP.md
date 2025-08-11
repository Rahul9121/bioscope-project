# Database Setup Instructions

## Large Data Files

Some data files are too large to store in the Git repository (>100MB GitHub limit). These files need to be added manually during deployment:

### Missing Files:
1. `cleaned_IUCN_data.csv` (357MB)
2. `iucn_cleaned_data.csv` (116MB)
3. `marine_risk_updated-2.csv` (58MB)
4. `terrestrial_human_coexistence_nj.csv` (69MB)

### Options for Deployment:

#### Option 1: Cloud Storage (Recommended)
1. Upload large CSV files to a cloud storage service (AWS S3, Google Cloud Storage, etc.)
2. Modify the data loading scripts to download from cloud storage
3. Use environment variables to store cloud storage URLs

#### Option 2: Database Import
1. Import the CSV data directly into your PostgreSQL database
2. Use database queries instead of CSV file reading
3. This is more efficient for production

#### Option 3: Compressed/Sample Data
1. Use compressed versions of the data files
2. Create sample datasets for development
3. Use full datasets only in production

### For Development:
You can create smaller sample files with the same structure:
```bash
# Create sample files with first 1000 rows
head -n 1000 original_file.csv > sample_file.csv
```

### For Production:
Upload the full data files to your hosting platform or use a database import script.

## Data Sources:
- IUCN Red List data
- Marine biodiversity data
- Terrestrial species data
- Human coexistence indices
