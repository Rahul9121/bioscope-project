// Mock data service for testing when backend is unavailable

export const mockGeocodingData = {
  // New Jersey ZIP codes with coordinates
  "07001": { latitude: 40.7056, longitude: -74.2111, city: "Avenel", state: "NJ" },
  "07002": { latitude: 40.7237, longitude: -74.1943, city: "Bayonne", state: "NJ" },
  "07003": { latitude: 40.8843, longitude: -74.0465, city: "Bloomfield", state: "NJ" },
  "07004": { latitude: 40.7951, longitude: -74.1085, city: "Fairfield", state: "NJ" },
  "07005": { latitude: 40.7218, longitude: -74.0718, city: "Boonton", state: "NJ" },
  "08540": { latitude: 40.3479, longitude: -74.6516, city: "Princeton", state: "NJ" },
  "08542": { latitude: 40.3321, longitude: -74.6182, city: "Princeton Junction", state: "NJ" },
  "08701": { latitude: 40.0951, longitude: -74.2174, city: "Lakewood", state: "NJ" },
  "08902": { latitude: 40.4862, longitude: -74.4518, city: "North Brunswick", state: "NJ" }
};

export const mockBiodiversityData = [
  {
    id: 1,
    latitude: 40.3479,
    longitude: -74.6516,
    risk_type: "IUCN Red List Species",
    threat_code: "High Risk",
    description: "Endangered Pine Barrens Tree Frog",
    scientific_name: "Hyla andersonii"
  },
  {
    id: 2,
    latitude: 40.3321,
    longitude: -74.6182,
    risk_type: "Invasive Species",
    threat_code: "Moderate Risk",
    description: "Purple Loosestrife",
    scientific_name: "Lythrum salicaria"
  },
  {
    id: 3,
    latitude: 40.0951,
    longitude: -74.2174,
    risk_type: "Freshwater Risk",
    threat_code: "Low Risk",
    description: "Brook Trout Habitat",
    scientific_name: "Salvelinus fontinalis"
  },
  {
    id: 4,
    latitude: 40.4862,
    longitude: -74.4518,
    risk_type: "Terrestrial Risk",
    threat_code: "High Risk",
    description: "Bobcat Population",
    scientific_name: "Lynx rufus"
  },
  {
    id: 5,
    latitude: 40.7056,
    longitude: -74.2111,
    risk_type: "Marine Risk",
    threat_code: "Moderate Risk",
    description: "Atlantic Sturgeon",
    scientific_name: "Acipenser oxyrinchus"
  }
];

// Mock geocoding function
export const getMockLocationFromZip = (zipCode) => {
  const location = mockGeocodingData[zipCode];
  if (location) {
    return {
      success: true,
      data: location
    };
  }
  return {
    success: false,
    error: `ZIP code ${zipCode} not found in mock data. Try: 07001, 08540, 08701, or 08902`
  };
};

// Mock biodiversity risk assessment
export const getMockBiodiversityRisks = (latitude, longitude, radius = 5) => {
  // Filter mock data within radius (simplified calculation)
  const risks = mockBiodiversityData.filter(risk => {
    const distance = Math.sqrt(
      Math.pow(risk.latitude - latitude, 2) + 
      Math.pow(risk.longitude - longitude, 2)
    );
    return distance <= (radius / 100); // Rough approximation
  });

  return {
    success: true,
    data: {
      risks: risks,
      total_risks: risks.length,
      location: { latitude, longitude },
      radius: radius
    }
  };
};

// Check if backend is available
export const checkBackendAvailability = async (apiUrl) => {
  try {
    const response = await fetch(`${apiUrl}/health`, {
      method: 'GET',
      timeout: 5000
    });
    return response.ok;
  } catch (error) {
    console.log('Backend unavailable, using mock data');
    return false;
  }
};
