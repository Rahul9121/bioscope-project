import React from "react";
import { Box, Typography, Card, CardContent, Grid, Container } from "@mui/material";
import Layout from "./Layout";
import { motion } from "framer-motion";

const AboutPage = () => {
  return (
    <Layout>
      {/* ✅ Hero Section - Left Smaller, Right Wider */}
      <Box
        sx={{
          width: "100vw",
          minHeight: "70vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "linear-gradient(135deg, #1B3A57, #4b82c7)", // Professional, premium blue gradient
          color: "white",
          padding: "5% 0",
          overflowX: "hidden",
        }}
      >
        <Grid container spacing={4} sx={{ width: "95%", maxWidth: "1400px" }}>
          {/* Left Side (Smaller Header Section) */}
          <Grid item xs={12} sm={4} md={4} sx={{ textAlign: "left" }}>
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 }}>
              <Typography
                variant="h3"
                fontWeight="bold"
                sx={{
                  fontSize: "clamp(2.5rem, 4vw, 3rem)",
                  mb: 2,
                }}
              >
                About Us
              </Typography>
              <Typography
                variant="h6"
                sx={{
                  opacity: 0.9,
                  fontSize: "clamp(1rem, 1.5vw, 1.3rem)",
                  margin: "0 auto",
                  lineHeight: 1.5,
                }}
              >
                Discover how BiodivProScope helps hotels ensure biodiversity compliance and sustainability.
              </Typography>
            </motion.div>
          </Grid>

          {/* Right Side (Larger Main Content) */}
          <Grid item xs={12} sm={8} md={8}>
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6, delay: 0.3 }}>
              <Box
                sx={{
                  background: "rgba(255, 255, 255, 0.15)",
                  borderRadius: "15px",
                  backdropFilter: "blur(10px)",
                  boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.3)",
                  padding: "3%",
                }}
              >
                <Typography
                  variant="h4"
                  fontWeight="bold"
                  sx={{
                    fontSize: "clamp(1.8rem, 3vw, 2.5rem)",
                    textAlign: "center",
                    mb: 3,
                  }}
                >
                  Why BiodivProScope?
                </Typography>

                <Grid container spacing={2}>
                  {/* Feature 1 */}
                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        background: "white",
                        borderRadius: "15px",
                        boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)",
                        padding: 3,
                        borderLeft: "8px solid #4b82c7",
                      }}
                    >
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">
                          🌍 Environmental Compliance
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1, lineHeight: 1.6 }}>
                          BiodivProScope helps hotels meet New Jersey’s biodiversity regulations effortlessly.
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Feature 2 */}
                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        background: "white",
                        borderRadius: "15px",
                        boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)",
                        padding: 3,
                        borderLeft: "8px solid #FF9800",
                      }}
                    >
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">
                          📊 Data-Driven Insights
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1, lineHeight: 1.6 }}>
                          Gain real-time biodiversity risk analysis based on geospatial and environmental data.
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Feature 3 */}
                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        background: "white",
                        borderRadius: "15px",
                        boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)",
                        padding: 3,
                        borderLeft: "8px solid #E53935",
                      }}
                    >
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">
                          🏨 Tailored for Hotels
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1, lineHeight: 1.6 }}>
                          Specifically built for hotel industry needs, ensuring smooth risk management.
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Feature 4 */}
                  <Grid item xs={12} sm={6}>
                    <Card
                      sx={{
                        background: "white",
                        borderRadius: "15px",
                        boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)",
                        padding: 3,
                        borderLeft: "8px solid #FFB300",
                      }}
                    >
                      <CardContent>
                        <Typography variant="h5" fontWeight="bold">
                          🔍 Interactive Mapping
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1, lineHeight: 1.6 }}>
                          Visualize risks in real-time with our advanced geospatial tools.
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

export default AboutPage;
