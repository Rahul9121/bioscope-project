import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Card, CardContent, Grid, Button, 
  Table, TableBody, TableCell, TableContainer, TableHead, 
  TableRow, Paper, Chip, Divider, List, ListItem, 
  ListItemIcon, ListItemText, Alert, CircularProgress,
  Accordion, AccordionSummary, AccordionDetails, Tabs, Tab
} from '@mui/material';
import {
  Assessment as AssessmentIcon,
  Download as DownloadIcon,
  TrendingUp as TrendingUpIcon,
  Eco as EcoIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  ExpandMore as ExpandMoreIcon,
  Schedule as ScheduleIcon,
  AttachMoney as CostIcon,
  Timeline as TimelineIcon
} from '@mui/icons-material';
import Layout from './Layout';

// Mitigation Strategy Engine
class MitigationStrategyEngine {
  constructor() {
    this.strategies = {
      invasive_species: {
        high: {
          immediate: [
            'Implement emergency containment protocols',
            'Deploy rapid response teams for species removal',
            'Establish quarantine zones around affected areas',
            'Apply targeted herbicide treatments where appropriate'
          ],
          longTerm: [
            'Develop species-specific eradication programs',
            'Implement early detection and rapid response (EDRR) systems',
            'Restore native plant communities',
            'Establish monitoring protocols'
          ],
          cost: 'High ($50,000 - $200,000)',
          timeline: '6-24 months',
          effectiveness: '85%'
        },
        moderate: {
          immediate: [
            'Map and document current species distribution',
            'Begin selective removal in sensitive areas',
            'Implement prevention measures'
          ],
          longTerm: [
            'Develop integrated pest management plans',
            'Restore degraded habitats',
            'Community education and volunteer programs'
          ],
          cost: 'Moderate ($10,000 - $50,000)',
          timeline: '3-12 months',
          effectiveness: '75%'
        },
        low: {
          immediate: [
            'Document species presence and monitor spread',
            'Implement preventive measures'
          ],
          longTerm: [
            'Regular monitoring and early intervention',
            'Habitat improvement programs'
          ],
          cost: 'Low ($1,000 - $10,000)',
          timeline: '1-6 months',
          effectiveness: '90%'
        }
      },
      iucn_conservation: {
        'endangered': {
          immediate: [
            'Implement emergency species protection protocols',
            'Establish protected habitat zones',
            'Coordinate with wildlife agencies',
            'Begin captive breeding programs if appropriate'
          ],
          longTerm: [
            'Develop species recovery plans',
            'Habitat restoration and enhancement',
            'Population monitoring and research',
            'Community engagement and education'
          ],
          cost: 'Very High ($100,000 - $500,000)',
          timeline: '12-60 months',
          effectiveness: '70%'
        },
        'vulnerable': {
          immediate: [
            'Implement habitat protection measures',
            'Begin population monitoring',
            'Reduce immediate threats'
          ],
          longTerm: [
            'Habitat enhancement and connectivity',
            'Species monitoring programs',
            'Threat reduction strategies'
          ],
          cost: 'High ($25,000 - $100,000)',
          timeline: '6-36 months',
          effectiveness: '80%'
        },
        'least concern': {
          immediate: [
            'Maintain current habitat conditions',
            'Monitor for population changes'
          ],
          longTerm: [
            'Preventive conservation measures',
            'Habitat quality maintenance'
          ],
          cost: 'Low ($2,000 - $15,000)',
          timeline: '1-12 months',
          effectiveness: '95%'
        }
      }
    };
  }

  generateMitigationPlan(risks) {
    const plan = {
      totalRisks: risks.length,
      priorityActions: [],
      immediateActions: [],
      longTermActions: [],
      estimatedCost: 0,
      estimatedTimeline: '1-12 months',
      expectedEffectiveness: '85%',
      risksByCategory: {}
    };

    let totalCostMin = 0;
    let totalCostMax = 0;

    risks.forEach(risk => {
      const category = this.categorizeRisk(risk.risk_type);
      const threatLevel = this.normalizeThreatLevel(risk.threat_code);
      
      if (!plan.risksByCategory[category]) {
        plan.risksByCategory[category] = [];
      }
      plan.risksByCategory[category].push(risk);

      const strategy = this.strategies[category]?.[threatLevel];
      if (strategy) {
        plan.immediateActions.push(...strategy.immediate);
        plan.longTermActions.push(...strategy.longTerm);
        
        // Parse cost range
        const costMatch = strategy.cost.match(/\$([0-9,]+)\s*-\s*\$([0-9,]+)/);
        if (costMatch) {
          totalCostMin += parseInt(costMatch[1].replace(',', ''));
          totalCostMax += parseInt(costMatch[2].replace(',', ''));
        }
      }
    });

    // Remove duplicates and prioritize actions
    plan.immediateActions = [...new Set(plan.immediateActions)];
    plan.longTermActions = [...new Set(plan.longTermActions)];
    
    // Set estimated cost range
    plan.estimatedCostRange = `$${totalCostMin.toLocaleString()} - $${totalCostMax.toLocaleString()}`;

    return plan;
  }

  categorizeRisk(riskType) {
    const type = (riskType || '').toLowerCase();
    if (type.includes('invasive')) return 'invasive_species';
    if (type.includes('iucn')) return 'iucn_conservation';
    return 'other';
  }

  normalizeThreatLevel(threatCode) {
    const threat = (threatCode || '').toLowerCase();
    if (threat === 'high' || threat === 'critically endangered' || threat === 'endangered') return 'high';
    if (threat === 'moderate' || threat === 'vulnerable' || threat === 'near threatened') return 'moderate';
    if (threat === 'low' || threat === 'least concern') return 'low';
    return 'low';
  }
}

const TabPanel = ({ children, value, index, ...other }) => (
  <div
    role="tabpanel"
    hidden={value !== index}
    id={`tabpanel-${index}`}
    aria-labelledby={`tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
  </div>
);

const ExecutiveSummaryTab = ({ mitigationPlan, location }) => (
  <Box>
    <Typography variant="h5" gutterBottom sx={{ color: '#1e3c72', fontWeight: 'bold' }}>
      Executive Summary
    </Typography>
    
    {location && (
      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body1">
          <strong>Assessment Location:</strong> {location.latitude?.toFixed(4)}, {location.longitude?.toFixed(4)}
        </Typography>
        <Typography variant="body2">
          Report generated on {new Date().toLocaleDateString()} • {mitigationPlan.totalRisks} risk factors analyzed
        </Typography>
      </Alert>
    )}

    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card elevation={2}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              📊 Risk Assessment Overview
            </Typography>
            <List>
              <ListItem>
                <ListItemText 
                  primary="Total Risk Factors Identified"
                  secondary={mitigationPlan.totalRisks}
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="Risk Categories Affected"
                  secondary={Object.keys(mitigationPlan.risksByCategory).length}
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="Immediate Actions Required"
                  secondary={mitigationPlan.immediateActions.length}
                />
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={6}>
        <Card elevation={2}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              💰 Implementation Estimate
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon><CostIcon /></ListItemIcon>
                <ListItemText 
                  primary="Estimated Cost Range"
                  secondary={mitigationPlan.estimatedCostRange}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon><ScheduleIcon /></ListItemIcon>
                <ListItemText 
                  primary="Implementation Timeline"
                  secondary={mitigationPlan.estimatedTimeline}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon><TrendingUpIcon /></ListItemIcon>
                <ListItemText 
                  primary="Expected Effectiveness"
                  secondary={mitigationPlan.expectedEffectiveness}
                />
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  </Box>
);

const ActionPlanTab = ({ mitigationPlan }) => (
  <Box>
    <Typography variant="h5" gutterBottom sx={{ color: '#1e3c72', fontWeight: 'bold' }}>
      Detailed Action Plan
    </Typography>

    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card elevation={2} sx={{ height: '100%' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <ErrorIcon sx={{ mr: 1, color: '#f44336' }} />
              Immediate Actions (0-6 months)
            </Typography>
            
            <List>
              {mitigationPlan.immediateActions.map((action, index) => (
                <ListItem key={index} sx={{ pl: 0 }}>
                  <ListItemIcon>
                    <CheckCircleIcon color="error" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={action}
                    sx={{ '& .MuiListItemText-primary': { fontSize: '0.9rem' } }}
                  />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={6}>
        <Card elevation={2} sx={{ height: '100%' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <TimelineIcon sx={{ mr: 1, color: '#2196f3' }} />
              Long-term Strategies (6+ months)
            </Typography>
            
            <List>
              {mitigationPlan.longTermActions.map((action, index) => (
                <ListItem key={index} sx={{ pl: 0 }}>
                  <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={action}
                    sx={{ '& .MuiListItemText-primary': { fontSize: '0.9rem' } }}
                  />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  </Box>
);

const DetailedAnalysisTab = ({ mitigationPlan }) => (
  <Box>
    <Typography variant="h5" gutterBottom sx={{ color: '#1e3c72', fontWeight: 'bold' }}>
      Detailed Risk Analysis by Category
    </Typography>

    {Object.entries(mitigationPlan.risksByCategory).map(([category, risks]) => (
      <Accordion key={category} sx={{ mb: 2 }}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
            <EcoIcon sx={{ mr: 2 }} />
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              {category.replace('_', ' ').toUpperCase()} RISKS
            </Typography>
            <Chip 
              label={`${risks.length} risks`}
              color="primary"
              size="small"
            />
          </Box>
        </AccordionSummary>
        
        <AccordionDetails>
          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell><strong>Species/Area</strong></TableCell>
                  <TableCell><strong>Threat Level</strong></TableCell>
                  <TableCell><strong>Location</strong></TableCell>
                  <TableCell><strong>Priority Action</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {risks.map((risk, index) => (
                  <TableRow key={index}>
                    <TableCell>{risk.description || 'Unknown'}</TableCell>
                    <TableCell>
                      <Chip 
                        label={risk.threat_code?.toUpperCase() || 'UNKNOWN'}
                        color={
                          (risk.threat_code || '').toLowerCase() === 'high' ? 'error' :
                          (risk.threat_code || '').toLowerCase() === 'moderate' ? 'warning' : 'success'
                        }
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {risk.latitude?.toFixed(3)}, {risk.longitude?.toFixed(3)}
                    </TableCell>
                    <TableCell>
                      Monitor and assess
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </AccordionDetails>
      </Accordion>
    ))}
  </Box>
);

const MitigationReport = () => {
  const [risks, setRisks] = useState([]);
  const [mitigationPlan, setMitigationPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentTab, setCurrentTab] = useState(0);
  const [location, setLocation] = useState(null);

  useEffect(() => {
    // Load risks from localStorage (set by RiskMap component)
    const storedRisks = localStorage.getItem('mitigation_risks');
    const storedLocation = localStorage.getItem('current_location');
    
    if (storedRisks) {
      const parsedRisks = JSON.parse(storedRisks);
      setRisks(parsedRisks);
      
      if (storedLocation) {
        setLocation(JSON.parse(storedLocation));
      }
      
      // Generate mitigation plan
      const engine = new MitigationStrategyEngine();
      const plan = engine.generateMitigationPlan(parsedRisks);
      setMitigationPlan(plan);
    }
    
    setLoading(false);
  }, []);

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  const downloadReport = (format) => {
    if (!mitigationPlan) return;

    const reportData = {
      location: location,
      generatedOn: new Date().toISOString(),
      totalRisks: mitigationPlan.totalRisks,
      immediateActions: mitigationPlan.immediateActions,
      longTermActions: mitigationPlan.longTermActions,
      estimatedCost: mitigationPlan.estimatedCostRange,
      risks: risks
    };

    // Create downloadable content
    const blob = new Blob([JSON.stringify(reportData, null, 2)], { 
      type: 'application/json' 
    });
    
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `biodiversity_mitigation_report_${new Date().toISOString().split('T')[0]}.${format}`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <Layout>
        <Box sx={{ textAlign: 'center', p: 4 }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>
            Generating Mitigation Report...
          </Typography>
        </Box>
      </Layout>
    );
  }

  if (!mitigationPlan || risks.length === 0) {
    return (
      <Layout>
        <Box sx={{ p: 4 }}>
          <Alert severity="warning">
            <Typography variant="h6" gutterBottom>
              No Risk Data Available
            </Typography>
            <Typography variant="body1">
              Please search for a location on the Risk Map first to generate a mitigation report.
            </Typography>
            <Button 
              variant="contained" 
              sx={{ mt: 2 }}
              onClick={() => window.location.href = '/risk-map'}
            >
              Go to Risk Map
            </Button>
          </Alert>
        </Box>
      </Layout>
    );
  }

  return (
    <Layout>
      <Box sx={{ p: 3 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h3" gutterBottom sx={{ 
            background: 'linear-gradient(45deg, #1e3c72 30%, #2a5298 90%)',
            backgroundClip: 'text',
            textFillColor: 'transparent',
            fontWeight: 'bold'
          }}>
            Biodiversity Mitigation Report
          </Typography>
          
          <Typography variant="h6" color="textSecondary" gutterBottom>
            Comprehensive Action Plan for Environmental Protection
          </Typography>

          {/* Download Buttons */}
          <Box sx={{ mt: 2 }}>
            <Button 
              variant="contained" 
              startIcon={<DownloadIcon />}
              onClick={() => downloadReport('json')}
              sx={{ mr: 2, mb: 1 }}
            >
              Download JSON
            </Button>
            <Button 
              variant="outlined" 
              startIcon={<DownloadIcon />}
              onClick={() => window.print()}
              sx={{ mr: 2, mb: 1 }}
            >
              Print Report
            </Button>
          </Box>
        </Box>

        {/* Tabs Navigation */}
        <Paper sx={{ mb: 3 }}>
          <Tabs 
            value={currentTab} 
            onChange={handleTabChange}
            centered
            textColor="primary"
            indicatorColor="primary"
          >
            <Tab label="Executive Summary" />
            <Tab label="Action Plan" />
            <Tab label="Detailed Analysis" />
          </Tabs>
        </Paper>

        {/* Tab Content */}
        <TabPanel value={currentTab} index={0}>
          <ExecutiveSummaryTab mitigationPlan={mitigationPlan} location={location} />
        </TabPanel>

        <TabPanel value={currentTab} index={1}>
          <ActionPlanTab mitigationPlan={mitigationPlan} />
        </TabPanel>

        <TabPanel value={currentTab} index={2}>
          <DetailedAnalysisTab mitigationPlan={mitigationPlan} />
        </TabPanel>

        {/* Footer */}
        <Box sx={{ mt: 4, textAlign: 'center', borderTop: '1px solid #eee', pt: 3 }}>
          <Typography variant="body2" color="textSecondary">
            This report was generated by the Bioscope Biodiversity Risk Assessment System
          </Typography>
          <Typography variant="body2" color="textSecondary">
            For technical support or questions, contact your environmental consulting team
          </Typography>
        </Box>
      </Box>
    </Layout>
  );
};

// Add missing method to MitigationStrategyEngine prototype
MitigationStrategyEngine.prototype.getPriorityAction = function(risk) {
  const category = this.categorizeRisk(risk.risk_type);
  const threatLevel = this.normalizeThreatLevel(risk.threat_code);
  
  const strategy = this.strategies[category]?.[threatLevel];
  if (strategy && strategy.immediate.length > 0) {
    return strategy.immediate[0];
  }
  
  return 'Monitor and assess';
};

export default MitigationReport;
