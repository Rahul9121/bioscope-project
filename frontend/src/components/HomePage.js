import React from "react";
import { Box, Typography, Button, Grid, Container, Card, CardContent, IconButton } from "@mui/material";
import { Eco, Science, Assessment, TrendingUp, LocationOn, Shield } from "@mui/icons-material";
import Layout from "./Layout";
import { motion } from "framer-motion";

const HomePage = () => {
  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.8 }
  };

  const staggerChildren = {
    initial: {},
    animate: {
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const features = [
    {
      icon: <Eco sx={{ fontSize: 50, color: "#4CAF50" }} />,
      title: "Biodiversity Analysis",
      description: "Advanced algorithms to assess ecosystem health and species diversity patterns."
    },
    {
      icon: <Assessment sx={{ fontSize: 50, color: "#2196F3" }} />,
      title: "Risk Assessment",
      description: "Comprehensive environmental risk evaluation with predictive modeling."
    },
    {
      icon: <Science sx={{ fontSize: 50, color: "#FF9800" }} />,
      title: "Scientific Insights",
      description: "Data-driven reports based on latest research and environmental standards."
    },
    {
      icon: <LocationOn sx={{ fontSize: 50, color: "#E91E63" }} />,
      title: "Location Mapping",
      description: "Interactive maps with precise geographic biodiversity data visualization."
    },
    {
      icon: <TrendingUp sx={{ fontSize: 50, color: "#9C27B0" }} />,
      title: "Trend Analysis",
      description: "Monitor changes over time with comprehensive temporal data analysis."
    },
    {
      icon: <Shield sx={{ fontSize: 50, color: "#F44336" }} />,
      title: "Compliance Reports",
      description: "Generate regulatory compliance reports for environmental assessments."
    }
  ];

  return (
    <Layout>
      {/* Enhanced Hero Section */}
      <motion.div initial="initial" animate="animate" variants={fadeInUp}>
        <Box
          sx={{
            width: "100vw",
            minHeight: "80vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            textAlign: "center",
            background: "linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%)",
            color: "white",
            padding: "5% 0",
            position: "relative",
            overflow: "hidden"
          }}
        >
          {/* Animated background elements */}
          <Box
            sx={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              background: "url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIgZmlsbC1vcGFjaXR5PSIwLjMiPjxwYXRoIGQ9Im0yMCAxMGMwIDUuNTIzLTQuNDc3IDEwLTEwIDEwcy0xMC00LjQ3Ny0xMC0xMCA0LjQ3Ny0xMCAxMC0xMCAxMCA0LjQ3NyAxMCAxMHoiLz48L2c+PC9nPjwvc3ZnPg==')",
              opacity: 0.1
            }}
          />
          
          <Box
            sx={{
              width: "90%",
              maxWidth: "900px",
              textAlign: "center",
              padding: "4%",
              borderRadius: "20px",
              background: "rgba(255, 255, 255, 0.08)",
              backdropFilter: "blur(20px)",
              border: "1px solid rgba(255, 255, 255, 0.1)",
              boxShadow: "0px 20px 50px rgba(0, 0, 0, 0.3)",
              margin: "0 auto",
              zIndex: 1
            }}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.2 }}
            >
              <Typography 
                variant="h1" 
                fontWeight="bold" 
                sx={{ 
                  fontSize: "clamp(2.5rem, 6vw, 4rem)",
                  background: "linear-gradient(45deg, #4CAF50, #81C784)",
                  backgroundClip: "text",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  mb: 2
                }}
              >
                BiodivProScope
              </Typography>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <Typography 
                variant="h4" 
                sx={{ 
                  mt: 2, 
                  mb: 3,
                  opacity: 0.95,
                  fontWeight: 300,
                  fontSize: "clamp(1.2rem, 3vw, 1.8rem)",
                  lineHeight: 1.6
                }}
              >
                Discover biodiversity insights and protect your environment with 
                <Box component="span" sx={{ color: "#4CAF50", fontWeight: "bold" }}>
                  data-driven assessments
                </Box>
              </Typography>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
            >
              <Box sx={{ display: "flex", gap: 3, justifyContent: "center", flexWrap: "wrap", mt: 4 }}>
                <Button 
                  variant="contained" 
                  size="large"
                  href="/map"
                  sx={{ 
                    background: "linear-gradient(45deg, #4CAF50, #66BB6A)",
                    fontSize: "1.3rem",
                    padding: "12px 32px",
                    borderRadius: "30px",
                    textTransform: "none",
                    boxShadow: "0 8px 30px rgba(76, 175, 80, 0.4)",
                    ':&hover': {
                      background: "linear-gradient(45deg, #388E3C, #4CAF50)",
                      transform: "translateY(-3px)",
                      boxShadow: "0 12px 40px rgba(76, 175, 80, 0.6)"
                    },
                    transition: "all 0.3s ease"
                  }}
                >
                  Start Assessment
                </Button>
                
                <Button 
                  variant="outlined" 
                  size="large"
                  href="/about"
                  sx={{ 
                    color: "white",
                    borderColor: "rgba(255, 255, 255, 0.5)",
                    fontSize: "1.3rem",
                    padding: "12px 32px",
                    borderRadius: "30px",
                    textTransform: "none",
                    borderWidth: "2px",
                    ':&hover': {
                      borderColor: "#4CAF50",
                      backgroundColor: "rgba(76, 175, 80, 0.1)",
                      transform: "translateY(-3px)"
                    },
                    transition: "all 0.3s ease"
                  }}
                >
                  Learn More
                </Button>
              </Box>
            </motion.div>
          </Box>
        </Box>
      </motion.div>

      {/* Features Section */}
      <Box sx={{ py: 8, px: 3, background: "linear-gradient(to bottom, #f8f9fa, #e9ecef)" }}>
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <Typography 
              variant="h2" 
              textAlign="center" 
              sx={{ 
                mb: 2,
                fontWeight: "bold",
                color: "#2C5364"
              }}
            >
              Powerful Features
            </Typography>
            <Typography 
              variant="h5" 
              textAlign="center" 
              sx={{ 
                mb: 6,
                color: "#666",
                fontWeight: 300
              }}
            >
              Everything you need for comprehensive biodiversity assessment
            </Typography>
          </motion.div>

          <motion.div
            initial="initial"
            whileInView="animate"
            variants={staggerChildren}
            viewport={{ once: true }}
          >
            <Grid container spacing={4}>
              {features.map((feature, index) => (
                <Grid item xs={12} md={6} lg={4} key={index}>
                  <motion.div variants={fadeInUp}>
                    <Card 
                      sx={{ 
                        height: "100%",
                        textAlign: "center",
                        padding: 3,
                        borderRadius: "16px",
                        boxShadow: "0 8px 32px rgba(0,0,0,0.1)",
                        border: "1px solid rgba(255,255,255,0.2)",
                        background: "rgba(255, 255, 255, 0.9)",
                        backdropFilter: "blur(10px)",
                        transition: "all 0.3s ease",
                        ':&hover': {
                          transform: "translateY(-8px)",
                          boxShadow: "0 16px 48px rgba(0,0,0,0.15)"
                        }
                      }}
                    >
                      <CardContent>
                        <Box sx={{ mb: 2 }}>
                          {feature.icon}
                        </Box>
                        <Typography 
                          variant="h5" 
                          component="h3" 
                          sx={{ 
                            mb: 2,
                            fontWeight: "bold",
                            color: "#2C5364"
                          }}
                        >
                          {feature.title}
                        </Typography>
                        <Typography 
                          variant="body1" 
                          sx={{ 
                            color: "#666",
                            lineHeight: 1.6
                          }}
                        >
                          {feature.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          </motion.div>
        </Container>
      </Box>

      {/* Call-to-Action Section */}
      <Box 
        sx={{ 
          py: 8,
          px: 3,
          background: "linear-gradient(135deg, #4CAF50, #2E7D32)",
          color: "white",
          textAlign: "center"
        }}
      >
        <Container maxWidth="md">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <Typography 
              variant="h3" 
              sx={{ 
                mb: 3,
                fontWeight: "bold"
              }}
            >
              Ready to Start Your Assessment?
            </Typography>
            <Typography 
              variant="h5" 
              sx={{ 
                mb: 4,
                opacity: 0.9,
                fontWeight: 300
              }}
            >
              Join thousands of environmental professionals using BiodivProScope for accurate biodiversity assessments
            </Typography>
            <Box sx={{ display: "flex", gap: 3, justifyContent: "center", flexWrap: "wrap" }}>
              <Button 
                variant="contained" 
                size="large"
                href="/register"
                sx={{ 
                  background: "white",
                  color: "#4CAF50",
                  fontSize: "1.2rem",
                  padding: "12px 32px",
                  borderRadius: "30px",
                  textTransform: "none",
                  fontWeight: "bold",
                  boxShadow: "0 8px 30px rgba(0,0,0,0.2)",
                  ':&hover': {
                    background: "#f5f5f5",
                    transform: "translateY(-3px)",
                    boxShadow: "0 12px 40px rgba(0,0,0,0.3)"
                  },
                  transition: "all 0.3s ease"
                }}
              >
                Get Started Free
              </Button>
              <Button 
                variant="outlined" 
                size="large"
                href="/how-it-works"
                sx={{ 
                  color: "white",
                  borderColor: "rgba(255, 255, 255, 0.8)",
                  fontSize: "1.2rem",
                  padding: "12px 32px",
                  borderRadius: "30px",
                  textTransform: "none",
                  borderWidth: "2px",
                  ':&hover': {
                    borderColor: "white",
                    backgroundColor: "rgba(255, 255, 255, 0.1)",
                    transform: "translateY(-3px)"
                  },
                  transition: "all 0.3s ease"
                }}
              >
                How It Works
              </Button>
            </Box>
          </motion.div>
        </Container>
      </Box>
    </Layout>
  );
};

export default HomePage;
