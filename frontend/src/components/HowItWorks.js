import React from "react";
import { Box, Typography, Grid, Card, CardContent } from "@mui/material";
import Layout from "./Layout";
import { motion } from "framer-motion";

const HowItWorks = () => {
  return (
    <Layout>
      <Box
        sx={{
          width: "100vw",
          minHeight: "70vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "linear-gradient(135deg, #1B3A57, #4b82c7)",
          color: "white",
          padding: "5% 0",
          overflowX: "hidden",
        }}
      >
        <Grid container spacing={4} sx={{ width: "95%", maxWidth: "1400px" }}>
          <Grid item xs={12} sm={4}>
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 }}>
              <Typography variant="h3" fontWeight="bold" sx={{ fontSize: "clamp(2.5rem, 4vw, 3rem)", mb: 2 }}>
                How It Works
              </Typography>
              <Typography variant="h6" sx={{ opacity: 0.9, fontSize: "clamp(1rem, 1.5vw, 1.3rem)", lineHeight: 1.5 }}>
                Discover how <strong>BiodivProScope</strong> enables hotels to <strong>analyze biodiversity risks</strong> and access <strong>AI-powered mitigation</strong> strategies.
              </Typography>
            </motion.div>
          </Grid>

          <Grid item xs={12} sm={8}>
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6, delay: 0.3 }}>
              <Box
                sx={{
                  background: "rgba(255, 255, 255, 0.15)",
                  borderRadius: "15px",
                  backdropFilter: "blur(10px)",
                  boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.3)",
                  padding: "4%",
                }}
              >
                <Typography variant="h4" fontWeight="bold" sx={{ textAlign: "center", mb: 3 }}>
                  Step-by-Step Process
                </Typography>

                <Grid container spacing={4} direction="column">
                  <Grid item xs={12}>
                    <Card sx={{ background: "white", borderRadius: "15px", boxShadow: "0px 10px 30px rgba(0,0,0,0.2)", padding: 4, borderLeft: "8px solid #4b82c7" }}>
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">🔐 Step 1: Log In</Typography>
                        <Typography sx={{ mt: 1, lineHeight: 1.6 }}>
                          Start by <strong>logging in</strong> or creating an account. This allows you to <strong>manage locations</strong> and access personalized risk reports.
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12}>
                    <Card sx={{ background: "white", borderRadius: "15px", boxShadow: "0px 10px 30px rgba(0,0,0,0.2)", padding: 4, borderLeft: "8px solid #43A047" }}>
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">📍 Step 2: Add a Hotel Location</Typography>
                        <Typography sx={{ mt: 1, lineHeight: 1.6 }}>
                          Enter a <strong>New Jersey ZIP code</strong> to add a hotel location. The system validates it and fetches geospatial data.
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12}>
                    <Card sx={{ background: "white", borderRadius: "15px", boxShadow: "0px 10px 30px rgba(0,0,0,0.2)", padding: 4, borderLeft: "8px solid #FF9800" }}>
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">📊 Step 3: Generate a Risk Report</Typography>
                        <Typography sx={{ mt: 1, lineHeight: 1.6 }}>
                          Click on <strong>"View Report"</strong> in your dashboard. The system will analyze biodiversity risks within a <strong>5-mile radius</strong> and return a report.
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12}>
                    <Card sx={{ background: "white", borderRadius: "15px", boxShadow: "0px 10px 30px rgba(0,0,0,0.2)", padding: 4, borderLeft: "8px solid #E53935" }}>
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">💡 Step 4: View AI-Powered Mitigation</Typography>
                        <Typography sx={{ mt: 1, lineHeight: 1.6 }}>
                          Your report includes <strong>categorized risks</strong> (IUCN, invasive, freshwater, marine, terrestrial) with <strong>AI-powered mitigation strategies</strong> based on real environmental data.
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12}>
                    <Card sx={{ background: "white", borderRadius: "15px", boxShadow: "0px 10px 30px rgba(0,0,0,0.2)", padding: 4, borderLeft: "8px solid #6D4C41" }}>
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">📥 Step 5: Download the Report</Typography>
                        <Typography sx={{ mt: 1, lineHeight: 1.6 }}>
                          You can <strong>export your biodiversity report</strong> in multiple formats: <strong>PDF, CSV, or Excel</strong>. Choose the format that best suits your compliance, documentation, or analysis needs.
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                </Grid>
              </Box>
            </motion.div>
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
};

export default HowItWorks;
