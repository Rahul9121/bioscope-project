import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  CircularProgress
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import PetsIcon from "@mui/icons-material/Pets";
import ForestIcon from "@mui/icons-material/Forest";
import OpacityIcon from "@mui/icons-material/Opacity";
import PublicIcon from "@mui/icons-material/Public";
import TerrainIcon from "@mui/icons-material/Terrain";

const iconStyles = {
  IUCN: { icon: <PetsIcon />, color: "#E53935" },
  "Invasive Species": { icon: <ForestIcon />, color: "#388E3C" },
  "Freshwater Risk": { icon: <OpacityIcon />, color: "#1976D2" },
  "Marine Risk": { icon: <PublicIcon />, color: "#4DD0E1" },
  "Terrestrial Risk": { icon: <TerrainIcon />, color: "#A1887F" },
};

const riskOrder = { HIGH: 1, MODERATE: 2, LOW: 3 };

const groupByThreatLevel = (risks) => {
  const grouped = { HIGH: {}, MODERATE: {}, LOW: {} };
  risks.forEach((risk) => {
    const threat = (risk.threat_code || "LOW").toUpperCase();
    const type = risk.risk_type;
    const desc = risk.description;
    if (!grouped[threat]) grouped[threat] = {};
    if (!grouped[threat][type]) grouped[threat][type] = {};
    if (!grouped[threat][type][desc]) grouped[threat][type][desc] = risk.mitigation?.action;
  });
  return grouped;
};

const MitigationReport = () => {
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMitigation = async () => {
      try {
        const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5001';
        const response = await fetch(`${apiUrl}/session-risks`, {
          credentials: "include"
        });
        let data = await response.json();
        let risksData = data.risks;
        if (!risksData || risksData.length === 0) {
          const local = localStorage.getItem("mitigation_risks");
          if (local) risksData = JSON.parse(local);
        }
        if (risksData && risksData.length > 0) {
          setRisks(risksData);
        }
      } catch (err) {
        console.error("Failed to fetch mitigation risks:", err);
        const local = localStorage.getItem("mitigation_risks");
        if (local) setRisks(JSON.parse(local));
      } finally {
        setLoading(false);
      }
    };
    fetchMitigation();
  }, []);

  const grouped = groupByThreatLevel(risks);
  const totalRisks = risks.length;

  if (loading) return <Box p={4}><CircularProgress /></Box>;

  return (
    <Box p={4} sx={{ fontFamily: 'Roboto, sans-serif', fontSize: '1.1rem', backgroundColor: '#f9f9f9' }}>
      <Paper elevation={3} sx={{ p: 4, backgroundColor: '#ffffff', borderRadius: 2 }}>
        <Typography variant="h3" sx={{ mb: 3, fontWeight: "bold", color: '#1B3A57' }}>
          🧪 Full Mitigation Action Report
        </Typography>
        <Typography variant="h5" sx={{ mb: 4, fontWeight: "bold", color: '#4B82C7' }}>
          Total Environmental Risks in your area : {totalRisks}
        </Typography>

        {Object.entries(grouped).sort(([a], [b]) => (riskOrder[a] || 99) - (riskOrder[b] || 99)).map(([threat, riskTypes], idx) => (
          <Box key={idx} mb={4}>
            <Typography variant="h4" sx={{ fontWeight: "bold", color: threat === 'HIGH' ? 'red' : threat === 'MODERATE' ? 'orange' : 'green', mb: 2 }}>
              {threat.charAt(0).toUpperCase() + threat.slice(1).toLowerCase()} Risk
            </Typography>

            {Object.entries(riskTypes || {}).map(([type, speciesMap], j) => (
              <Accordion key={j} defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography sx={{ fontWeight: "bold", color: iconStyles[type]?.color || "black" }}>
                    {iconStyles[type]?.icon} {type}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  {Object.entries(speciesMap).map(([species, action], k) => {
                    const match = risks.find(r => r.description === species && r.risk_type === type && r.threat_code.toUpperCase() === threat);
                    const coords = match
                      ? `(Latitude: ${parseFloat(match.latitude).toFixed(4)}, Longitude: ${parseFloat(match.longitude).toFixed(4)})`
                      : "";

                    let displayName = null;

                    if (type === "Marine Risk" && match?.description?.includes("Marine HCI")) {
                      const score = parseFloat(match.description.match(/[\d.]+/)?.[0] || 0).toFixed(2);
                      displayName = `Marine Risk Level: ${score}`;
                    } else if (type === "Terrestrial Risk" && match?.description?.includes("Terrestrial Risk Level")) {
                      const score = parseFloat(match.description.match(/[\d.]+/)?.[0] || 0).toFixed(2);
                      displayName = `Terrestrial Risk Level: ${score}`;
                    } else if (type === "Freshwater Risk" && match?.description?.includes("Freshwater HCI")) {
                      const score = parseFloat(match.description.match(/[\d.]+/)?.[0] || 0).toFixed(2);
                      displayName = `Freshwater Risk Level: ${score}`;
                    } else if (typeof species === "string") {
                      const parts = species.trim().split(/\s+/);
                      if (parts.length === 2) {
                        const genus = parts[0].charAt(0).toUpperCase() + parts[0].slice(1).toLowerCase();
                        const speciesName = parts[1].toLowerCase();
                        displayName = <em>{`${genus} ${speciesName}`}</em>;
                      } else {
                        displayName = <em>{species.charAt(0).toUpperCase() + species.slice(1).toLowerCase()}</em>;
                      }
                    } else {
                      displayName = <em>{String(species)}</em>;
                    }

                    return (
                      <Typography key={k} sx={{ ml: 2 }}>
                        {k + 1}. {displayName} {coords}
                      </Typography>
                    );
                  })}

                  <Typography variant="subtitle1" sx={{ mt: 2, ml: 2, fontWeight: "bold", fontSize: "1.15rem", color: "#1B3A57" }}>
                    Action: {Object.values(speciesMap)[0]}
                  </Typography>
                </AccordionDetails>
              </Accordion>
            ))}
          </Box>
        ))}
      </Paper>
    </Box>
  );
};

export default MitigationReport;
