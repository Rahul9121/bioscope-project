import { Paper, Typography, Box, Chip } from "@mui/material";
import ForestIcon from "@mui/icons-material/Forest";       // Invasive
import OpacityIcon from "@mui/icons-material/Opacity";     // Freshwater
import PetsIcon from "@mui/icons-material/Pets";           // IUCN
import PublicIcon from "@mui/icons-material/Public";       // Marine Water
import TerrainIcon from "@mui/icons-material/Terrain";     // Terrestrial
import HelpOutlineIcon from "@mui/icons-material/HelpOutline"; // Unknown

const ClusterLegend = () => {
  return (
    <Paper sx={{ p: 2, mb: 2, backgroundColor: "#f9f9f9", borderRadius: 2 }}>
      <Typography variant="h6" sx={{ fontWeight: "bold", mb: 1 }}>
        📍 What Do the Clusters Represent?
      </Typography>

      <Typography variant="body2" sx={{ mb: 1 }}>
        Clusters are <strong>bubbles</strong> on the map representing multiple biodiversity risks grouped by location.
        The number inside the cluster shows how many risks exist in that area.
      </Typography>

      <Box sx={{ mt: 1, mb: 1 }}>
        <Typography variant="body2" sx={{ mb: 0.5 }}>
          🔴 <strong>Red Cluster:</strong> Contains at least one <strong>High Risk</strong> (e.g., critically endangered species or severe invasives).
        </Typography>
        <Typography variant="body2" sx={{ mb: 0.5 }}>
          🟠 <strong>Orange Cluster:</strong> Mostly <strong>Moderate Risks</strong> like vulnerable species or moderate water issues.
        </Typography>
        <Typography variant="body2" sx={{ mb: 0.5 }}>
          🟢 <strong>Green Cluster:</strong> Primarily <strong>Low Risk</strong> threats.
        </Typography>
      </Box>

      <Typography variant="body2" sx={{ fontWeight: "bold", mb: 1 }}>
        Risk Types Found Inside Clusters:
      </Typography>

      <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
        <Chip
          icon={<ForestIcon />}
          label="Invasive Species"
          sx={{ backgroundColor: "#81C784", color: "black" }}
        />
        <Chip
          icon={<PetsIcon />}
          label="IUCN Red List"
          sx={{ backgroundColor: "#E53935", color: "black" }}
        />
        <Chip
          icon={<OpacityIcon />}
          label="Freshwater Risk"
          sx={{ backgroundColor: "#64B5F6", color: "black" }}
        />
        <Chip
          icon={<PublicIcon />}
          label="Marine Water Risk"
          sx={{ backgroundColor: "#4DD0E1", color: "black" }}
        />
        <Chip
          icon={<TerrainIcon />}
          label="Terrestrial Risk"
          sx={{ backgroundColor: "#A1887F", color: "black" }}
        />
      </Box>

      <Typography variant="body2" sx={{ mt: 2 }}>
        👉 Click a cluster to zoom in and explore individual risk markers.
      </Typography>
    </Paper>
  );
};

export default ClusterLegend;
