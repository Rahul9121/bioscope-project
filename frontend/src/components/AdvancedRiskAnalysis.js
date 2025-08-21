import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Card, CardContent, CircularProgress, Grid, 
  Chip, Divider, LinearProgress, Alert, List, ListItem, 
  ListItemIcon, ListItemText, Accordion, AccordionSummary, 
  AccordionDetails, Paper, Tooltip, IconButton
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Nature as EcoIcon,
  LocationOn as LocationIcon
} from '@mui/icons-material';

// Risk Analysis Engine
class BiodiversityRiskAnalyzer {
  constructor() {
    this.weights = {
      invasive_species: 0.25,
      iucn_conservation: 0.30,
      freshwater_risk: 0.20,
      marine_risk: 0.15,
      terrestrial_risk: 0.10
    };
    
    this.threatLevels = {
      'high': 10,
      'moderate': 6,
      'medium': 5,
      'low': 2,
      'unknown': 1
    };
  }

  calculateOverallRiskScore(risks) {
    if (!risks || risks.length === 0) return 0;

    let totalScore = 0;
    let categoryScores = {};
    let categoryFrequency = {};

    // Categorize and score risks
    risks.forEach(risk => {
      const category = this.categorizeRisk(risk.risk_type);
      const threatScore = this.threatLevels[risk.threat_code?.toLowerCase()] || 1;
      
      if (!categoryScores[category]) {
        categoryScores[category] = 0;
        categoryFrequency[category] = 0;
      }
      
      categoryScores[category] += threatScore;
      categoryFrequency[category] += 1;
    });

    // Calculate weighted average
    Object.keys(categoryScores).forEach(category => {
      const avgScore = categoryScores[category] / categoryFrequency[category];
      const weight = this.weights[category] || 0.1;
      totalScore += avgScore * weight;
    });

    return Math.min(Math.round(totalScore * 10), 100);
  }

  categorizeRisk(riskType) {
    const type = (riskType || '').toLowerCase();
    if (type.includes('invasive')) return 'invasive_species';
    if (type.includes('iucn')) return 'iucn_conservation';
    if (type.includes('freshwater')) return 'freshwater_risk';
    if (type.includes('marine')) return 'marine_risk';
    if (type.includes('terrestrial')) return 'terrestrial_risk';
    return 'other';
  }

  generateRiskInsights(risks) {
    if (!risks || risks.length === 0) {
      return {
        criticalThreats: 0,
        moderateThreats: 0,
        lowThreats: 0,
        recommendations: ['No biodiversity data available for this location'],
        priority: 'low'
      };
    }

    const criticalThreats = risks.filter(r => (r.threat_code || '').toLowerCase() === 'high').length;
    const moderateThreats = risks.filter(r => (r.threat_code || '').toLowerCase() === 'moderate').length;
    const lowThreats = risks.filter(r => ['low', 'least concern'].includes((r.threat_code || '').toLowerCase())).length;

    let priority = 'low';
    let recommendations = [];

    if (criticalThreats > 0) {
      priority = 'critical';
      recommendations.push(`Immediate action required: ${criticalThreats} critical threat(s) identified`);
      recommendations.push('Conduct detailed environmental impact assessment');
      recommendations.push('Implement emergency conservation measures');
    } else if (moderateThreats > 2) {
      priority = 'high';
      recommendations.push('Develop comprehensive mitigation strategy');
      recommendations.push('Monitor ecosystem changes quarterly');
    } else if (moderateThreats > 0) {
      priority = 'moderate';
      recommendations.push('Implement preventive conservation measures');
      recommendations.push('Schedule bi-annual biodiversity monitoring');
    } else {
      recommendations.push('Maintain current conservation practices');
      recommendations.push('Continue routine environmental monitoring');
    }

    return {
      criticalThreats,
      moderateThreats,
      lowThreats,
      recommendations,
      priority
    };
  }

  getCategoryBreakdown(risks) {
    const categories = {};
    
    risks.forEach(risk => {
      const category = this.categorizeRisk(risk.risk_type);
      if (!categories[category]) {
        categories[category] = {
          count: 0,
          threats: { high: 0, moderate: 0, low: 0 },
          species: []
        };
      }
      
      categories[category].count += 1;
      const threat = (risk.threat_code || 'unknown').toLowerCase();
      if (categories[category].threats[threat] !== undefined) {
        categories[category].threats[threat] += 1;
      }
      
      if (risk.description) {
        categories[category].species.push(risk.description);
      }
    });

    return categories;
  }
}

const RiskScoreCard = ({ score, insights }) => {
  const getScoreColor = (score) => {
    if (score >= 70) return '#f44336'; // Red
    if (score >= 40) return '#ff9800'; // Orange
    if (score >= 20) return '#ffc107'; // Yellow
    return '#4caf50'; // Green
  };

  const getScoreIcon = (priority) => {
    switch(priority) {
      case 'critical': return <ErrorIcon sx={{ color: '#f44336' }} />;
      case 'high': return <WarningIcon sx={{ color: '#ff9800' }} />;
      case 'moderate': return <InfoIcon sx={{ color: '#ffc107' }} />;
      default: return <CheckCircleIcon sx={{ color: '#4caf50' }} />;
    }
  };

  return (
    <Card elevation={3} sx={{ background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)', color: 'white' }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography variant="h6" gutterBottom>
              Biodiversity Risk Score
            </Typography>
            <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
              {score}/100
            </Typography>
          </Box>
          <Box textAlign="center">
            <Box sx={{ 
              background: 'rgba(255,255,255,0.2)', 
              borderRadius: '50%', 
              p: 2, 
              mb: 1 
            }}>
              {getScoreIcon(insights.priority)}
            </Box>
            <Typography variant="caption" sx={{ textTransform: 'uppercase' }}>
              {insights.priority} Priority
            </Typography>
          </Box>
        </Box>
        
        <Box sx={{ mt: 2 }}>
          <LinearProgress 
            variant="determinate" 
            value={score} 
            sx={{
              height: 8,
              borderRadius: 4,
              backgroundColor: 'rgba(255,255,255,0.3)',
              '& .MuiLinearProgress-bar': {
                backgroundColor: getScoreColor(score)
              }
            }}
          />
        </Box>
      </CardContent>
    </Card>
  );
};

const ThreatBreakdownCard = ({ insights }) => (
  <Card elevation={2}>
    <CardContent>
      <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
        <TrendingUpIcon sx={{ mr: 1 }} />
        Threat Level Breakdown
      </Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={4}>
          <Box textAlign="center" sx={{ p: 2, backgroundColor: '#ffebee', borderRadius: 2 }}>
            <Typography variant="h4" sx={{ color: '#f44336', fontWeight: 'bold' }}>
              {insights.criticalThreats}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Critical
            </Typography>
          </Box>
        </Grid>
        
        <Grid item xs={4}>
          <Box textAlign="center" sx={{ p: 2, backgroundColor: '#fff3e0', borderRadius: 2 }}>
            <Typography variant="h4" sx={{ color: '#ff9800', fontWeight: 'bold' }}>
              {insights.moderateThreats}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Moderate
            </Typography>
          </Box>
        </Grid>
        
        <Grid item xs={4}>
          <Box textAlign="center" sx={{ p: 2, backgroundColor: '#e8f5e8', borderRadius: 2 }}>
            <Typography variant="h4" sx={{ color: '#4caf50', fontWeight: 'bold' }}>
              {insights.lowThreats}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Low
            </Typography>
          </Box>
        </Grid>
      </Grid>
    </CardContent>
  </Card>
);

const CategoryAnalysisCard = ({ categories }) => {
  const categoryNames = {
    invasive_species: 'Invasive Species',
    iucn_conservation: 'Conservation Status',
    freshwater_risk: 'Freshwater Risk',
    marine_risk: 'Marine Risk',
    terrestrial_risk: 'Terrestrial Risk'
  };

  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <AssessmentIcon sx={{ mr: 1 }} />
          Risk Category Analysis
        </Typography>
        
        {Object.entries(categories).map(([category, data]) => (
          <Accordion key={category} sx={{ mb: 1 }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                <EcoIcon sx={{ mr: 1 }} />
                <Typography sx={{ flexGrow: 1 }}>
                  {categoryNames[category] || category}
                </Typography>
                <Chip 
                  label={`${data.count} risks`}
                  size="small"
                  color="primary"
                  sx={{ mr: 1 }}
                />
              </Box>
            </AccordionSummary>
            
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" gutterBottom>
                    <strong>Threat Distribution:</strong>
                  </Typography>
                  <Box sx={{ pl: 2 }}>
                    <Typography variant="body2">• High: {data.threats.high}</Typography>
                    <Typography variant="body2">• Moderate: {data.threats.moderate}</Typography>
                    <Typography variant="body2">• Low: {data.threats.low}</Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={6}>
                  {data.species.length > 0 && (
                    <>
                      <Typography variant="body2" gutterBottom>
                        <strong>Species/Areas:</strong>
                      </Typography>
                      <Box sx={{ pl: 2 }}>
                        {data.species.slice(0, 3).map((species, idx) => (
                          <Typography key={idx} variant="body2">
                            • {species}
                          </Typography>
                        ))}
                        {data.species.length > 3 && (
                          <Typography variant="body2" color="textSecondary">
                            ...and {data.species.length - 3} more
                          </Typography>
                        )}
                      </Box>
                    </>
                  )}
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        ))}
      </CardContent>
    </Card>
  );
};

const RecommendationsCard = ({ recommendations }) => (
  <Card elevation={2}>
    <CardContent>
      <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
        <CheckCircleIcon sx={{ mr: 1 }} />
        Action Recommendations
      </Typography>
      
      <List>
        {recommendations.map((recommendation, index) => (
          <ListItem key={index} sx={{ pl: 0 }}>
            <ListItemIcon>
              <LocationIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary={recommendation}
              sx={{ '& .MuiListItemText-primary': { fontSize: '0.9rem' } }}
            />
          </ListItem>
        ))}
      </List>
    </CardContent>
  </Card>
);

const AdvancedRiskAnalysis = ({ risks = [], location = null }) => {
  const [analyzer] = useState(new BiodiversityRiskAnalyzer());
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (risks.length > 0) {
      setLoading(true);
      
      // Simulate processing time for better UX
      setTimeout(() => {
        const overallScore = analyzer.calculateOverallRiskScore(risks);
        const insights = analyzer.generateRiskInsights(risks);
        const categoryBreakdown = analyzer.getCategoryBreakdown(risks);
        
        setAnalysis({
          score: overallScore,
          insights,
          categories: categoryBreakdown,
          totalRisks: risks.length
        });
        
        setLoading(false);
      }, 1000);
    } else {
      setAnalysis(null);
    }
  }, [risks, analyzer]);

  if (loading) {
    return (
      <Box sx={{ textAlign: 'center', p: 4 }}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Analyzing Biodiversity Risks...
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Processing {risks.length} risk factors
        </Typography>
      </Box>
    );
  }

  if (!analysis) {
    return (
      <Alert severity="info" sx={{ m: 2 }}>
        <Typography variant="body1">
          No risk analysis available. Search for a location to begin biodiversity assessment.
        </Typography>
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom sx={{ 
        textAlign: 'center', 
        mb: 3,
        background: 'linear-gradient(45deg, #1e3c72 30%, #2a5298 90%)',
        backgroundClip: 'text',
        textFillColor: 'transparent',
        fontWeight: 'bold'
      }}>
        Advanced Risk Analysis Report
      </Typography>

      {location && (
        <Paper sx={{ p: 2, mb: 3, backgroundColor: '#f5f5f5' }}>
          <Typography variant="body1" sx={{ display: 'flex', alignItems: 'center' }}>
            <LocationIcon sx={{ mr: 1 }} />
            <strong>Analysis Location:</strong> {location.latitude?.toFixed(4)}, {location.longitude?.toFixed(4)}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Analysis completed on {new Date().toLocaleDateString()} • {analysis.totalRisks} risk factors evaluated
          </Typography>
        </Paper>
      )}

      <Grid container spacing={3}>
        {/* Overall Risk Score */}
        <Grid item xs={12} md={6}>
          <RiskScoreCard score={analysis.score} insights={analysis.insights} />
        </Grid>

        {/* Threat Breakdown */}
        <Grid item xs={12} md={6}>
          <ThreatBreakdownCard insights={analysis.insights} />
        </Grid>

        {/* Category Analysis */}
        <Grid item xs={12}>
          <CategoryAnalysisCard categories={analysis.categories} />
        </Grid>

        {/* Recommendations */}
        <Grid item xs={12}>
          <RecommendationsCard recommendations={analysis.insights.recommendations} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default AdvancedRiskAnalysis;
