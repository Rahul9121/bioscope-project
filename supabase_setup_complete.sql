-- =====================================================
-- Bioscope Complete Database Setup for Supabase
-- Run this script in your Supabase SQL Editor
-- =====================================================

-- Enable extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. USERS TABLE (Authentication)
-- =====================================================
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    hotel_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- =====================================================
-- 2. INVASIVE SPECIES TABLE
-- =====================================================
DROP TABLE IF EXISTS invasive_species CASCADE;

CREATE TABLE invasive_species (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    common_name VARCHAR(255),
    scientific_name VARCHAR(255),
    threat_code VARCHAR(50) DEFAULT 'low',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial index for location queries
CREATE INDEX IF NOT EXISTS idx_invasive_species_location ON invasive_species(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_invasive_species_threat ON invasive_species(threat_code);

-- =====================================================
-- 3. IUCN DATA TABLE (Species Conservation Status)
-- =====================================================
DROP TABLE IF EXISTS iucn_data CASCADE;

CREATE TABLE iucn_data (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    species_name VARCHAR(255) NOT NULL,
    threat_status VARCHAR(100),
    habitat VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_iucn_data_location ON iucn_data(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_iucn_data_status ON iucn_data(threat_status);

-- =====================================================
-- 4. FRESHWATER RISK TABLE
-- =====================================================
DROP TABLE IF EXISTS freshwater_risk CASCADE;

CREATE TABLE freshwater_risk (
    id SERIAL PRIMARY KEY,
    x DECIMAL(11, 8) NOT NULL,  -- longitude
    y DECIMAL(10, 8) NOT NULL,  -- latitude
    normalized_risk DECIMAL(5, 3),
    risk_level VARCHAR(50) DEFAULT 'Low',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial index
CREATE INDEX IF NOT EXISTS idx_freshwater_risk_location ON freshwater_risk(y, x);
CREATE INDEX IF NOT EXISTS idx_freshwater_risk_level ON freshwater_risk(risk_level);

-- =====================================================
-- 5. MARINE HCI TABLE (Human-Coexistence Index)
-- =====================================================
DROP TABLE IF EXISTS marine_hci CASCADE;

CREATE TABLE marine_hci (
    id SERIAL PRIMARY KEY,
    x DECIMAL(11, 8) NOT NULL,  -- longitude
    y DECIMAL(10, 8) NOT NULL,  -- latitude
    marine_hci DECIMAL(5, 3) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial index
CREATE INDEX IF NOT EXISTS idx_marine_hci_location ON marine_hci(y, x);

-- =====================================================
-- 6. TERRESTRIAL RISK TABLE
-- =====================================================
DROP TABLE IF EXISTS terrestrial_risk CASCADE;

CREATE TABLE terrestrial_risk (
    id SERIAL PRIMARY KEY,
    x DECIMAL(11, 8) NOT NULL,  -- longitude
    y DECIMAL(10, 8) NOT NULL,  -- latitude
    normalized_risk DECIMAL(5, 3),
    risk_level VARCHAR(50) DEFAULT 'low',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial index
CREATE INDEX IF NOT EXISTS idx_terrestrial_risk_location ON terrestrial_risk(y, x);
CREATE INDEX IF NOT EXISTS idx_terrestrial_risk_level ON terrestrial_risk(risk_level);

-- =====================================================
-- INSERT SAMPLE DATA FOR NEW JERSEY
-- =====================================================

-- Sample Users (for testing)
INSERT INTO users (hotel_name, email, password_hash) VALUES
('Test Hotel NJ', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewMpsKapHWZS5BzC');

-- Sample Invasive Species Data (New Jersey coordinates)
INSERT INTO invasive_species (latitude, longitude, common_name, scientific_name, threat_code) VALUES
(40.0583, -74.4057, 'Purple Loosestrife', 'Lythrum salicaria', 'high'),
(40.7128, -74.0060, 'Japanese Knotweed', 'Fallopia japonica', 'high'),
(40.2206, -74.7563, 'Autumn Olive', 'Elaeagnus umbellata', 'moderate'),
(39.7267, -75.2835, 'Multiflora Rose', 'Rosa multiflora', 'moderate'),
(40.9176, -74.1718, 'Norway Maple', 'Acer platanoides', 'low'),
(40.3573, -74.4291, 'Japanese Barberry', 'Berberis thunbergii', 'moderate'),
(40.1907, -74.6728, 'Tree of Heaven', 'Ailanthus altissima', 'high'),
(40.5795, -74.1502, 'Japanese Honeysuckle', 'Lonicera japonica', 'moderate'),
(40.8176, -74.2291, 'Garlic Mustard', 'Alliaria petiolata', 'moderate'),
(40.4420, -74.0134, 'Mile-a-Minute Weed', 'Persicaria perfoliata', 'high');

-- Sample IUCN Conservation Data
INSERT INTO iucn_data (latitude, longitude, species_name, threat_status, habitat) VALUES
(40.0583, -74.4057, 'Bald Eagle', 'Least Concern', 'Wetlands'),
(40.7128, -74.0060, 'Peregrine Falcon', 'Least Concern', 'Urban/Cliffs'),
(40.2206, -74.7563, 'Wood Turtle', 'Vulnerable', 'Streams/Forest'),
(39.7267, -75.2835, 'Eastern Red-backed Salamander', 'Least Concern', 'Forest Floor'),
(40.9176, -74.1718, 'Bog Turtle', 'Endangered', 'Wetlands'),
(40.3573, -74.4291, 'Pine Barrens Treefrog', 'Near Threatened', 'Wetlands'),
(40.1907, -74.6728, 'Timber Rattlesnake', 'Vulnerable', 'Forest'),
(40.5795, -74.1502, 'Northern Long-eared Bat', 'Endangered', 'Forest'),
(40.8176, -74.2291, 'Bobcat', 'Least Concern', 'Forest/Suburban'),
(40.4420, -74.0134, 'Osprey', 'Least Concern', 'Coastal/Wetlands');

-- Sample Freshwater Risk Data
INSERT INTO freshwater_risk (x, y, normalized_risk, risk_level) VALUES
(-74.4057, 40.0583, 0.75, 'High'),
(-74.0060, 40.7128, 0.45, 'Moderate'),
(-74.7563, 40.2206, 0.25, 'Low'),
(-75.2835, 39.7267, 0.60, 'High'),
(-74.1718, 40.9176, 0.35, 'Moderate'),
(-74.4291, 40.3573, 0.55, 'Moderate'),
(-74.6728, 40.1907, 0.80, 'High'),
(-74.1502, 40.5795, 0.30, 'Low'),
(-74.2291, 40.8176, 0.65, 'High'),
(-74.0134, 40.4420, 0.40, 'Moderate');

-- Sample Marine HCI Data (Human-Coexistence Index)
INSERT INTO marine_hci (x, y, marine_hci) VALUES
(-74.4057, 40.0583, 0.80),
(-74.0060, 40.7128, 0.65),
(-74.7563, 40.2206, 0.45),
(-75.2835, 39.7267, 0.75),
(-74.1718, 40.9176, 0.55),
(-74.4291, 40.3573, 0.70),
(-74.6728, 40.1907, 0.85),
(-74.1502, 40.5795, 0.50),
(-74.2291, 40.8176, 0.60),
(-74.0134, 40.4420, 0.90);

-- Sample Terrestrial Risk Data
INSERT INTO terrestrial_risk (x, y, normalized_risk, risk_level) VALUES
(-74.4057, 40.0583, 0.85, 'high'),
(-74.0060, 40.7128, 0.55, 'moderate'),
(-74.7563, 40.2206, 0.25, 'low'),
(-75.2835, 39.7267, 0.70, 'high'),
(-74.1718, 40.9176, 0.40, 'moderate'),
(-74.4291, 40.3573, 0.60, 'moderate'),
(-74.6728, 40.1907, 0.90, 'high'),
(-74.1502, 40.5795, 0.35, 'low'),
(-74.2291, 40.8176, 0.75, 'high'),
(-74.0134, 40.4420, 0.50, 'moderate');

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Check table row counts
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL
SELECT 'invasive_species', COUNT(*) FROM invasive_species
UNION ALL
SELECT 'iucn_data', COUNT(*) FROM iucn_data
UNION ALL
SELECT 'freshwater_risk', COUNT(*) FROM freshwater_risk
UNION ALL
SELECT 'marine_hci', COUNT(*) FROM marine_hci
UNION ALL
SELECT 'terrestrial_risk', COUNT(*) FROM terrestrial_risk
ORDER BY table_name;

-- Test spatial queries (should return results)
SELECT 'Invasive Species Near Princeton' as test_type, COUNT(*) as result_count
FROM invasive_species 
WHERE ABS(latitude - 40.0583) <= 0.1 AND ABS(longitude - (-74.4057)) <= 0.1

UNION ALL

SELECT 'IUCN Data Near Princeton', COUNT(*)
FROM iucn_data 
WHERE ABS(latitude - 40.0583) <= 0.1 AND ABS(longitude - (-74.4057)) <= 0.1

UNION ALL

SELECT 'Freshwater Risk Near Princeton', COUNT(*)
FROM freshwater_risk 
WHERE ABS(y - 40.0583) <= 0.5 AND ABS(x - (-74.4057)) <= 0.1;

-- =====================================================
-- SUCCESS MESSAGE
-- =====================================================
DO $$
BEGIN
    RAISE NOTICE '🎉 Bioscope database setup completed successfully!';
    RAISE NOTICE '✅ All tables created with sample data';
    RAISE NOTICE '✅ Indexes created for optimal performance';
    RAISE NOTICE '✅ Ready for biodiversity risk assessment queries';
END $$;
