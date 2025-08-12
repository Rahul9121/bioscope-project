-- Bioscope Database Setup for Supabase
-- Run this script in your Supabase SQL Editor

-- 1. Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    hotel_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Invasive Species table
CREATE TABLE IF NOT EXISTS invasive_species (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    common_name VARCHAR(255),
    scientific_name VARCHAR(255),
    threat_code VARCHAR(50) DEFAULT 'low'
);

-- 3. IUCN Data table
CREATE TABLE IF NOT EXISTS iucn_data (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    species_name VARCHAR(255),
    threat_status VARCHAR(100),
    habitat VARCHAR(255)
);

-- 4. Freshwater Risk table
CREATE TABLE IF NOT EXISTS freshwater_risk (
    id SERIAL PRIMARY KEY,
    x DECIMAL(11, 8),
    y DECIMAL(10, 8),
    normalized_risk DECIMAL(5, 3),
    risk_level VARCHAR(50) DEFAULT 'Low'
);

-- 5. Marine HCI table
CREATE TABLE IF NOT EXISTS marine_hci (
    id SERIAL PRIMARY KEY,
    x DECIMAL(11, 8),
    y DECIMAL(10, 8),
    marine_hci DECIMAL(5, 3) DEFAULT 0.0
);

-- 6. Terrestrial Risk table
CREATE TABLE IF NOT EXISTS terrestrial_risk (
    id SERIAL PRIMARY KEY,
    x DECIMAL(11, 8),
    y DECIMAL(10, 8),
    normalized_risk DECIMAL(5, 3),
    risk_level VARCHAR(50) DEFAULT 'low'
);

-- Insert sample data for testing
-- Sample invasive species data around New Jersey
INSERT INTO invasive_species (latitude, longitude, common_name, threat_code) VALUES
(40.0583, -74.4057, 'Purple Loosestrife', 'high'),
(40.7128, -74.0060, 'Japanese Knotweed', 'moderate'),
(40.2206, -74.7563, 'Autumn Olive', 'moderate'),
(39.7267, -75.2835, 'Multiflora Rose', 'low'),
(40.9176, -74.1718, 'Norway Maple', 'low');

-- Sample IUCN data
INSERT INTO iucn_data (latitude, longitude, species_name, threat_status) VALUES
(40.0583, -74.4057, 'Bald Eagle', 'Least Concern'),
(40.7128, -74.0060, 'Peregrine Falcon', 'Least Concern'),
(40.2206, -74.7563, 'Wood Turtle', 'Vulnerable'),
(39.7267, -75.2835, 'Eastern Red-backed Salamander', 'Least Concern'),
(40.9176, -74.1718, 'Bog Turtle', 'Endangered');

-- Sample freshwater risk data
INSERT INTO freshwater_risk (x, y, normalized_risk, risk_level) VALUES
(-74.4057, 40.0583, 0.75, 'High'),
(-74.0060, 40.7128, 0.45, 'Moderate'),
(-74.7563, 40.2206, 0.25, 'Low'),
(-75.2835, 39.7267, 0.60, 'High'),
(-74.1718, 40.9176, 0.35, 'Moderate');

-- Sample marine HCI data
INSERT INTO marine_hci (x, y, marine_hci) VALUES
(-74.4057, 40.0583, 0.80),
(-74.0060, 40.7128, 0.65),
(-74.7563, 40.2206, 0.45),
(-75.2835, 39.7267, 0.75),
(-74.1718, 40.9176, 0.55);

-- Sample terrestrial risk data
INSERT INTO terrestrial_risk (x, y, normalized_risk, risk_level) VALUES
(-74.4057, 40.0583, 0.85, 'high'),
(-74.0060, 40.7128, 0.55, 'moderate'),
(-74.7563, 40.2206, 0.25, 'low'),
(-75.2835, 39.7267, 0.70, 'high'),
(-74.1718, 40.9176, 0.40, 'moderate');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_invasive_species_location ON invasive_species(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_iucn_data_location ON iucn_data(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_freshwater_risk_location ON freshwater_risk(x, y);
CREATE INDEX IF NOT EXISTS idx_marine_hci_location ON marine_hci(x, y);
CREATE INDEX IF NOT EXISTS idx_terrestrial_risk_location ON terrestrial_risk(x, y);

-- Grant necessary permissions (adjust as needed)
-- Note: This might not be needed in Supabase as it handles permissions differently
