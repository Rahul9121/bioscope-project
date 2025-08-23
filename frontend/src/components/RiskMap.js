import React, { useState, useEffect, useCallback } from "react";
import _ from "lodash";
import {
  Box, Typography, TextField, Button, Paper, List, ListItem, ListItemText, ToggleButton, ToggleButtonGroup
} from "@mui/material";
import {
  MapContainer, TileLayer, Marker, Circle, Popup, useMap, useMapEvents
} from "react-leaflet";
import MarkerClusterGroup from "@changey/react-leaflet-markercluster";
import "leaflet/dist/leaflet.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import L from "leaflet";
import axios from "axios";
import Layout from "./Layout";
// Removed mock data service - now using backend API only
import AdvancedRiskAnalysis from "./AdvancedRiskAnalysis";
import FileDownloadIcon from "@mui/icons-material/FileDownload";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import PublicIcon from "@mui/icons-material/Public";       // Marine
import TerrainIcon from "@mui/icons-material/Terrain";     // Terrestrial

import SearchIcon from "@mui/icons-material/Search"; // Make sure this is imported at the top
import ClusterLegend from "./ClusterLegend"; // adjust path if needed
import ForestIcon from "@mui/icons-material/Forest";      // Invasive
import ScienceIcon from "@mui/icons-material/Science";    // IUCN
import OpacityIcon from "@mui/icons-material/Opacity";    // Freshwater
import HelpOutlineIcon from "@mui/icons-material/HelpOutline"; // Unknown
import { Chip, Divider } from "@mui/material";
import PetsIcon from "@mui/icons-material/Pets";
import LandscapeIcon from "@mui/icons-material/Landscape"; // 🌿 Terrestrial Risk

import VisibilityIcon from "@mui/icons-material/Visibility"; // Add this at the top


// inside JSX:



const getMarkerColor = (threat_code) => {
  if (!threat_code || typeof threat_code !== "string") return "blue"; // default/fallback color

  const normalizedThreat = threat_code.toLowerCase().replace(" risk", "");
  switch (normalizedThreat) {
    case "high": return "red";
    case "moderate": return "orange";
    case "low": return "green";
    default: return "blue";
  }
};


delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: "",
});

const customMarker = new L.Icon({
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: "",
});

const createCustomIcon = (color) => {
  return L.divIcon({
    className: "custom-marker",
    html: `<div style="background-color:${color}; width:14px; height:14px; border-radius:50%; border:2px solid black;"></div>`,
    iconSize: [16, 16],
  });
};
const RiskPopupCard = ({ risk }) => {
  const { risk_type, threat_code, description } = risk;
  const normalizedType = (risk_type || "").toLowerCase();
  const threat = (threat_code || "").toLowerCase();

  let icon = <HelpOutlineIcon />;
  let bg = "#CFD8DC";
  let label = "Unknown";

  if (normalizedType.includes("invasive")) {
    icon = <ForestIcon />;
    bg = "#81C784";
    label = "Invasive Species";
  } else if (normalizedType.includes("iucn")) {
    icon = <PetsIcon />;
    bg = "#E53935";
    label = "IUCN Red List";
  } else if (normalizedType.includes("freshwater")) {
    icon = <OpacityIcon />;
    bg = "#64B5F6";
    label = "Freshwater Risk";
  } else if (normalizedType.includes("marine")) {
  icon = <PublicIcon />;
  bg = "#4DD0E1";
  label = "Marine Water Risk";
} else if (normalizedType.includes("terrestrial")) {
  icon = <TerrainIcon />;
  bg = "#A1887F";
  label = "Terrestrial Risk";
}

  const threatColor = {
    high: "error",
    moderate: "warning",
    low: "success",
  }[threat] || "default";

  return (
    <Box sx={{ p: 1, maxWidth: 250 }}>
      <Chip
        icon={icon}
        label={label}
        sx={{ backgroundColor: bg, color: "black", mb: 1 }}
      />

      {description && (
        <Typography variant="subtitle2" sx={{ mb: 0.5, fontWeight: "bold" }}>
          Species: {description}
        </Typography>
      )}

      <Chip
        label={`Threat Level: ${threat_code?.toUpperCase()}`}
        color={threatColor}
        size="small"
        sx={{ mb: 1 }}
      />

      {/* Optional mitigation preview */}


    </Box>
  );
};


const buttonBlueStyle = {
  width: "100%",
  padding: "14px 0",
  fontSize: "1.1rem",
  fontWeight: "bold",
  borderRadius: "12px",
  background: "linear-gradient(90deg, #1B3A57, #4B82C7)",
  color: "white",
  textTransform: "none",
  "&:hover": {
    background: "linear-gradient(90deg, #174268, #3F71B0)",
    transform: "scale(1.03)",
    boxShadow: "0px 4px 12px rgba(75, 130, 199, 0.4)",
  },
  "&:disabled": {
    background: "rgba(75, 130, 199, 0.3)",
    color: "#eee",
    cursor: "not-allowed",
  },
};



const FlyToSearchPointButton = ({ location }) => {
  const map = useMap();

  const handleClick = () => {
    if (location) {
      map.flyTo([location.latitude, location.longitude], 13, {
        animate: true,
        duration: 1.5,
      });
    }
  };

  return (
    <Box sx={{ position: "absolute", top: 10, right: 20, zIndex: 1000, minWidth: 220 }}>
      <Button
        variant="contained"
        onClick={handleClick}
        startIcon={<ArrowBackIcon />}
        sx={buttonBlueStyle}
      >
        Back to Search Point
      </Button>

    </Box>
  );
};


const MapUpdater = ({ location }) => {
  const map = useMap();
  useEffect(() => {
    if (map) {
      setTimeout(() => {
        map.invalidateSize();
        if (location) {
          map.flyTo([location.latitude, location.longitude], 13, {
            animate: true,
            duration: 1.5,
          });
        }
      }, 300);
    }
  }, [location, map]);
  return null;
};

const MapPaginationHandler = ({ location, setRisks, offset, setOffset, loadedAreas, setLoadedAreas }) => {
  const map = useMapEvents({
    moveend: () => handleMapMove(),
    zoomend: () => handleMapMove(),
  });

  const handleMapMove = () => {
    const center = map.getCenter();
    debouncedFetch(center);
  };

  const debouncedFetch = useCallback(_.debounce(async (center) => {
    const key = `${center.lat.toFixed(3)},${center.lng.toFixed(3)}`;
    if (loadedAreas.includes(key)) return;

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5001';
      const response = await axios.post(`${apiUrl}/search`, {
        input_text: `${center.lat}, ${center.lng}`,
        offset: offset + 50
      }, {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      });

      setRisks(prev => [...prev, ...response.data.risks]);
      setOffset(prev => prev + 50);
      setLoadedAreas(prev => [...prev, key]);
    } catch (err) {
      console.error("Pagination fetch error:", err);
    }
  }, 800), [offset, loadedAreas]);

  return null;
};

const RiskMap = () => {
  const [inputText, setInputText] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [location, setLocation] = useState(null);
  const [risks, setRisks] = useState([]);
  const [error, setError] = useState("");
  const [reportFormat, setReportFormat] = useState(null);
  const [offset, setOffset] = useState(0);
  const [loadedAreas, setLoadedAreas] = useState([]);

  const handleFormatChange = (event, newFormat) => {
    if (newFormat) setReportFormat(newFormat);
  };

const downloadReport = async () => {
  const storedRisks = localStorage.getItem("mitigation_risks");
  const risks = storedRisks ? JSON.parse(storedRisks) : [];


  if (!reportFormat || risks.length === 0) {
    alert("No risks to download. Please search first.");
    return;
  }

  try {
    const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5001';
    const response = await axios.post(
      `${apiUrl}/download-report-direct`,
      { format: reportFormat, risks },
      {
        responseType: "blob",
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const blob = new Blob([response.data], { type: response.headers["content-type"] });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `biodiv_report.${reportFormat}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    console.error("❌ Report download failed:", err);
    alert("Failed to download the report. Make sure you searched first.");
  }
};




  const fetchAddressSuggestions = useCallback(
    _.debounce(async (query) => {
      if (!query) return setSuggestions([]);
      try {
        const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5001';
        const response = await axios.get(`${apiUrl}/address-autocomplete`, {
          params: { query },
          headers: { "Content-Type": "application/json" },
        });
        setSuggestions(response.data);
      } catch (err) {
        console.error("Error fetching address suggestions:", err);
      }
    }, 500), []);

  useEffect(() => { fetchAddressSuggestions(inputText); }, [inputText]);
  useEffect(() => {
    console.log("🧪 Received risks:", risks);
  }, [risks]);

  const handleSuggestionClick = (suggestion) => {
    setInputText(suggestion.display_name);
    setSuggestions([]);
  };

  const handleSearch = async () => {
    try {
      setError("");
      setOffset(0);
      setLoadedAreas([]);
      
      console.log('🔍 Searching for input:', inputText);
      
      // Use backend API for all searches (ZIP codes, addresses, coordinates)
      const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5001';
      
      const response = await axios.post(`${apiUrl}/search`, { input_text: inputText }, {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
        timeout: 15000
      });
      
      if (response.data.center && response.data.risks) {
        setLocation(response.data.center);
        setRisks(response.data.risks);
        localStorage.setItem("mitigation_risks", JSON.stringify(response.data.risks));
        localStorage.setItem("current_location", JSON.stringify(response.data.center));
        console.log('✅ Search successful!');
        console.log('📍 Location:', response.data.center);
        console.log('🦋 Risks found:', response.data.risks.length);
        setError(""); // Clear any previous errors
      } else {
        setError("No data found for this location. Please try a different New Jersey location.");
      }
      
    } catch (err) {
      console.error('❌ Search error:', err);
      
      let errorMessage = "Search failed. ";
      
      if (err.response) {
        // Server responded with an error
        errorMessage += err.response.data?.error || `Server error: ${err.response.status}`;
      } else if (err.request) {
        // Network error - server not reachable
        errorMessage += "Cannot connect to the backend server. Please make sure the backend is running on the correct port.";
      } else {
        // Other error
        errorMessage += err.message;
      }
      
      setError(errorMessage);
      setLocation(null);
      setRisks([]);
    }
  };

  return (
    <Layout>
      <Box sx={{ display: "flex", minHeight: "calc(100vh - 64px)", width: "100vw" }}>
        <Box sx={{ width: { xs: "100%", md: "25%" }, maxHeight: "calc(100vh - 64px)", overflowY: "auto", backgroundColor: "#f9f9f9", padding: 3, borderRight: "2px solid #ddd", boxShadow: "0px 4px 15px rgba(0, 0, 0, 0.1)" }}>
          <Typography variant="h6" sx={{ fontWeight: "bold", mb: 1 }}>Search for Biodiversity Risk</Typography>
          
          <Box sx={{ mb: 2, p: 2, backgroundColor: "#e8f5e8", borderRadius: 2 }}>
            <Typography variant="body2" sx={{ fontWeight: "bold", color: "#2e7d32" }}>
              🌿 Try any New Jersey location:
            </Typography>
            <Typography variant="body2" sx={{ mt: 0.5 }}>
              • ZIP codes: 08037, 08540, 07001, 08701<br/>
              • Addresses: "123 Main St, Trenton, NJ"<br/>
              • Cities: "Princeton, NJ" or "Newark, NJ"
            </Typography>
          </Box>
          
          <TextField label="Enter Address or ZIP Code" value={inputText} onChange={(e) => {
            setInputText(e.target.value);
            fetchAddressSuggestions(e.target.value);
          }} onKeyDown={(e) => e.key === "Enter" && handleSearch()} size="small" variant="outlined" sx={{ width: "100%", mb: 1 }} />
          <List>
            {suggestions.map((s, index) => (
              <ListItem button key={index} onClick={() => handleSuggestionClick(s)}>
                <ListItemText primary={s.display_name} />
              </ListItem>
            ))}
          </List>
          <Button
            variant="contained"
            onClick={handleSearch}
            startIcon={<SearchIcon />}
            sx={{ ...buttonBlueStyle, mt: 2 }}
          >
            Search
          </Button>

          {error && (
            <Box sx={{ mt: 2, p: 2, backgroundColor: "#ffebee", borderRadius: 2, border: "1px solid #f44336" }}>
              <Typography variant="body2" sx={{ color: "#d32f2f" }}>
                {error}
              </Typography>
            </Box>
          )}

          <Paper sx={{ p: 2, mb: 2, backgroundColor: "#f9f9f9", borderRadius: 2 }}>
            <ClusterLegend />
          </Paper>

          {/* Advanced Risk Analysis */}
          {risks.length > 0 && (
            <Paper sx={{ p: 2, mb: 2, backgroundColor: "#fff", borderRadius: 2 }}>
              <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2, color: "#1B3A57" }}>
                📊 Advanced Analysis
              </Typography>
              <AdvancedRiskAnalysis risks={risks} location={location} />
            </Paper>
          )}

          <Box sx={{ mt: 3 }}>
            {/* 🔹 Mitigation Report Scrollable Preview */}
              <Paper sx={{ mt: 3, p: 2, borderRadius: 2, backgroundColor: "#fff", maxHeight: 300, overflowY: "auto" }}>
                <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2, color: "#1B3A57" }}>
                  🧪 Mitigation Strategy Report
                </Typography>

                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => window.open("/mitigation-report", "_blank")}
                  startIcon={<VisibilityIcon />}
                  sx={{ ...buttonBlueStyle, mt: 1 }}
                >
                  View Full Report
                </Button>


              </Paper>




            <ToggleButtonGroup value={reportFormat} exclusive onChange={handleFormatChange} sx={{ display: "flex", justifyContent: "center", border: "1px solid #ccc", borderRadius: "8px", overflow: "hidden", mb: 2 }}>
              <ToggleButton value="pdf">PDF</ToggleButton>
              <ToggleButton value="csv">CSV</ToggleButton>
              <ToggleButton value="excel">Excel</ToggleButton>
            </ToggleButtonGroup>
            <Button
              variant="contained"
              fullWidth
              onClick={downloadReport}
              disabled={!reportFormat}
              startIcon={<FileDownloadIcon />}
              sx={{ ...buttonBlueStyle, mt: 2 }}
            >
              Download
            </Button>

          </Box>
        </Box>

        <Box sx={{ width: { xs: "100%", md: "75%" }, height: "calc(100vh - 64px)" }}>
          <MapContainer center={[40.8172, -74.2007]} zoom={12} style={{ height: "100%", width: "100%" }}>
            <MapUpdater location={location} />
            <MapPaginationHandler location={location} setRisks={setRisks} offset={offset} setOffset={setOffset} loadedAreas={loadedAreas} setLoadedAreas={setLoadedAreas} />
            <TileLayer url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}" />

            {location && (
              <>
                <Marker position={[location.latitude, location.longitude]} icon={customMarker} />
                <Circle center={[location.latitude, location.longitude]} radius={8046.72} pathOptions={{ fillColor: "blue", fillOpacity: 0.3, color: "blue", weight: 2 }} />
              </>
            )}

            <MarkerClusterGroup
              iconCreateFunction={(cluster) => {
                const markers = cluster.getAllChildMarkers();
                const levels = markers.map(m => m.options.threatLevel || "low");
                let color = "blue";
                if (levels.includes("high")) color = "red";
                else if (levels.includes("moderate")) color = "orange";
                else if (levels.includes("low")) color = "green";

                return L.divIcon({
                  html: `<div style="background-color:${color}; color:white; border-radius:50%; width:40px; height:40px; display:flex; align-items:center; justify-content:center; font-weight:bold; border: 2px solid black;">${cluster.getChildCount()}</div>`,
                  className: "custom-cluster-icon",
                  iconSize: [40, 40],
                });
              }}
            >
              {risks.map((risk, index) => (
                <Marker
                  key={index}
                  position={[risk.latitude, risk.longitude]}
                  icon={createCustomIcon(getMarkerColor(risk.threat_code))}
                  threatLevel={(risk.threat_code || "unknown").toLowerCase()}

                >
                  <Popup>
                    <RiskPopupCard risk={risk} />
                  </Popup>

                </Marker>
              ))}
            </MarkerClusterGroup>
            {location && <FlyToSearchPointButton location={location} />}
          </MapContainer>
        </Box>
      </Box>
    </Layout>
  );
};

export default RiskMap;
