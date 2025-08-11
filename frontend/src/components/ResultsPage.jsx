import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Circle, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const ResultsPage = ({ results }) => {
    const [mapData, setMapData] = useState(null);

    useEffect(() => {
        setMapData(results);
    }, [results]);

    if (!mapData) return <p>Loading...</p>;

    const { center, risks } = mapData;
    const radiusInMeters = 5 * 1609.34; // 5 miles in meters

    const normalizeThreatCode = (code) => {
        return code.toLowerCase().trim().replace(/[^a-z]/g, ""); // remove non-alpha chars
    };

    const prettyThreatLabel = (code) => {
        const normalized = normalizeThreatCode(code);
        switch (normalized) {
            case "high": return "High Risk";
            case "moderate": return "Moderate Risk";
            case "medium": return "Medium Risk";
            case "low": return "Low Risk";
            default: return code;
        }
    };

    const getThreatColor = (threat) => {
        const normalized = normalizeThreatCode(threat);
        switch (normalized) {
            case "high":
                return "#8B0000"; // Dark Red
            case "moderate":
                return "#FFA500"; // Orange
            case "medium":
                return "#FF6347"; // Light Red
            case "low":
                return "#90EE90"; // Light Green
            default:
                return "#808080"; // Gray
        }
    };

    return (
        <div className="results-container">
            <h1>Biodiversity Risks in Your Area</h1>

            <div className="results-content">
                {/* Left Panel: Risks List */}
                <div className="risks-list">
                    <h2>Identified Risks</h2>
                    {risks.length > 0 ? (
                        Object.entries(
                            risks.reduce((acc, risk) => {
                                const code = normalizeThreatCode(risk.threat_code);
                                if (!acc[code]) acc[code] = [];
                                acc[code].push(risk);
                                return acc;
                            }, {})
                        ).map(([normalizedCode, groupRisks]) => (
                            <details key={normalizedCode} open>
                                <summary style={{ fontWeight: "bold", color: getThreatColor(normalizedCode), fontSize: "1.1rem" }}>
                                    {prettyThreatLabel(normalizedCode)} ({groupRisks.length})
                                </summary>
                                <ul>
                                    {groupRisks.map((risk, index) => (
                                        <li key={index}>
                                            <strong>{risk.risk_type}</strong>: {risk.description}
                                            <div className="mitigation">
                                                <strong>Mitigation Action:</strong> {risk.mitigation.action}
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            </details>
                        ))
                    ) : (
                        <p>No biodiversity risks found in this area.</p>
                    )}
                </div>

                {/* Right Panel: Map */}
                <div className="map-container">
                    <MapContainer center={[center.latitude, center.longitude]} zoom={13} style={{ height: "500px", width: "100%" }}>
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                        {/* Center Point */}
                        <Marker position={[center.latitude, center.longitude]}>
                            <Popup>Center Point</Popup>
                        </Marker>

                        {/* 5-Mile Radius Circle */}
                        <Circle
                            center={[center.latitude, center.longitude]}
                            radius={radiusInMeters}
                            color="blue"
                            fillColor="#add8e6"
                            fillOpacity={0.3}
                        />

                        {/* Risk Markers */}
                        {risks.map((risk, index) => (
                            <CircleMarker
                                key={index}
                                center={[risk.latitude, risk.longitude]}
                                radius={8}
                                fillColor={getThreatColor(risk.threat_code)}
                                color={getThreatColor(risk.threat_code)}
                                fillOpacity={0.8}
                            >
                                <Popup>
                                    <strong>{risk.risk_type}</strong><br />
                                    {risk.description}<br />
                                    Threat Level: {prettyThreatLabel(risk.threat_code)}
                                </Popup>
                            </CircleMarker>
                        ))}
                    </MapContainer>
                </div>
            </div>
        </div>
    );
};

export default ResultsPage;
