# 🌿 BiodivProScope - Biodiversity Protection Scope

<div align="center">
  <img src="https://img.shields.io/badge/React-18.3.1-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React" />
  <img src="https://img.shields.io/badge/Flask-2.2.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/PostgreSQL-12+-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Material--UI-6.4.1-0081CB?style=for-the-badge&logo=mui&logoColor=white" alt="Material-UI" />
</div>

<div align="center">
  <h3>🚀 A comprehensive full-stack platform for biodiversity assessment and environmental risk analysis</h3>
  <p>Empowering researchers, conservationists, and environmental professionals with advanced tools for biodiversity protection and ecosystem management.</p>
</div>

---

## 🌟 Key Features

### 🗺️ **Interactive Mapping & Visualization**
- **Leaflet-based mapping** with MarkerCluster support for large datasets
- **Real-time location tracking** and GPS integration
- **Multi-layer ecosystem visualization** (freshwater, marine, terrestrial)
- **Custom markers and overlays** for species distribution

### 🔬 **Advanced Risk Assessment**
- **IUCN Red List integration** for species conservation status
- **Threat level analysis** with automated classification
- **Environmental impact scoring** using machine learning
- **Invasive species monitoring** and risk prediction

### 📊 **Comprehensive Reporting**
- **PDF report generation** with detailed analysis and visualizations
- **Excel export functionality** for data analysis
- **Mitigation action recommendations** based on threat assessment
- **Historical trend analysis** and comparative studies

### 🔐 **Secure User Management**
- **JWT-based authentication** with session management
- **Role-based access control** for different user types
- **Cross-platform compatibility** with responsive design
- **Secure API endpoints** with CORS configuration

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern JavaScript framework
- **Material-UI** - Component library
- **Tailwind CSS** - Utility-first CSS framework
- **Leaflet** - Interactive mapping library
- **Axios** - HTTP client
- **Framer Motion** - Animation library
- **jsPDF** - PDF generation

### Backend
- **Flask 2.2.3** - Python web framework
- **PostgreSQL** - Primary database
- **SQLAlchemy** - Database ORM
- **ChromaDB** - Vector database for ML operations
- **ReportLab** - PDF generation
- **Flask-CORS** - Cross-origin resource sharing

## 📋 Prerequisites

- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **PostgreSQL** (v12 or higher)
- **Git**

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/bioscope-project.git
cd bioscope-project
```

### 2. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/bioscope_db
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=bioscope_db
DB_PORT=5432

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
PORT=5001

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com

# Optional: Railway/Production Settings
RAILWAY_ENVIRONMENT=development
```

### 3. Database Setup

#### Option A: Local PostgreSQL
```bash
# Install PostgreSQL (if not already installed)
# Create database
psql -U postgres
CREATE DATABASE bioscope_db;
\q

# Run database initialization scripts
python db_info.py  # Check database connection
python final_import.py  # Import initial data
```

#### Option B: Supabase (Recommended for production)
1. Create a [Supabase](https://supabase.com) account
2. Create a new project
3. Copy the database URL from Settings > Database
4. Update your `.env` file with the Supabase URL

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the backend setup
python test_app.py  # Run comprehensive tests

# Start the Flask application
python app.py
```

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### 6. Verify Installation

- **Backend Health Check**: http://localhost:5001/health
- **JWT Test Endpoint**: http://localhost:5001/test-jwt
- **Frontend Application**: http://localhost:3000

### 7. Development Tools

```bash
# Backend testing and debugging
python check_db.py          # Verify database connection
python check_iucn.py        # Test IUCN data integration
python test_app.py          # Run comprehensive backend tests

# Data management
python import_all_data.py   # Import complete dataset
python analyze_data_coverage.py  # Analyze data completeness
```

## 🛠️ API Documentation

### Core Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/health` | Health check | None |
| `GET` | `/test-jwt` | JWT token test | None |
| `POST` | `/account/register` | User registration | None |
| `POST` | `/account/login` | User authentication | None |
| `GET` | `/account/profile` | Get user profile | JWT Required |
| `GET` | `/locations/search` | Location-based search | Optional |
| `POST` | `/locations/risk-assessment` | Generate risk assessment | JWT Required |
| `GET` | `/locations/species-data` | Get species information | Optional |
| `POST` | `/reports/generate` | Generate PDF reports | JWT Required |

### Request Examples

#### User Registration
```bash
curl -X POST http://localhost:5001/account/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password",
    "full_name": "John Doe"
  }'
```

#### Risk Assessment
```bash
curl -X POST http://localhost:5001/locations/risk-assessment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "latitude": 40.7128,
    "longitude": -74.0060,
    "ecosystem_type": "urban"
  }'
```

## 🌐 Deployment

### Free Hosting Options

#### Frontend (React)
- **Vercel** ✅ Recommended for React apps
  - Connect your GitHub repository
  - Automatic deployments on push
  - Built-in SSL certificates

- **Netlify** - Great for static sites with continuous deployment
- **GitHub Pages** - Free hosting for static sites

#### Backend (Flask)
- **Railway** ✅ Modern platform with PostgreSQL support
  - One-click PostgreSQL deployment
  - Environment variable management
  - Automatic HTTPS

- **Render** - Free tier with easy deployment
- **Heroku** - Classic platform (limited free tier)

#### Database
- **Railway** - Integrated PostgreSQL
- **Supabase** ✅ PostgreSQL with additional features (Recommended)
- **ElephantSQL** - Managed PostgreSQL

### Production Deployment Steps

#### 1. Frontend Deployment (Vercel)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel --prod
```

#### 2. Backend Deployment (Railway)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

#### 3. Environment Variables for Production
```env
# Production settings
FLASK_ENV=production
RAILWAY_ENVIRONMENT=production
SECRET_KEY=your_secure_production_key
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
```

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database connection
python check_db.py

# Test database with detailed output
python db_info.py

# Verify environment variables
echo $DATABASE_URL  # On Unix/Linux/macOS
echo %DATABASE_URL% # On Windows CMD
echo $env:DATABASE_URL # On Windows PowerShell
```

#### Session Authentication Problems
```bash
# Test JWT token generation
curl http://localhost:5001/test-jwt

# Run session debugging
python debug_session_flow.py

# Interactive session testing
python interactive_session_test.py
```

#### Frontend-Backend Communication
```bash
# Check CORS configuration
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS http://localhost:5001/health

# Test backend endpoints
python test_backend_connectivity.py
```

#### Data Import Issues
```bash
# Check data coverage
python analyze_data_coverage.py

# Import remaining data
python import_remaining_data.py

# Verify IUCN data integration
python check_iucn.py
```

### Performance Optimization

- **Database Indexing**: Ensure proper indexes on frequently queried columns
- **API Caching**: Implement Redis caching for frequent requests
- **Frontend Optimization**: Use React.memo and useMemo for expensive components
- **Image Optimization**: Compress and optimize map tiles and assets

### Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| Database | Local PostgreSQL | Supabase/Railway |
| Sessions | Filesystem | Secure cookies |
| CORS | Permissive | Restricted origins |
| Logging | Debug level | Error level |
| SSL | Not required | Required |

## 📝 Project Structure

```
bioscope-project/
├── backend/                    # Flask backend application
│   ├── routes/                 # API route definitions
│   │   ├── account_routes.py   # User authentication routes
│   │   └── location_routes.py  # Location and mapping routes
│   ├── app.py                 # Main Flask application
│   ├── mitigation_action.py   # Mitigation strategy logic
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React frontend application
│   ├── public/                # Static assets and index.html
│   ├── src/                   # React components and logic
│   │   ├── components/        # Reusable React components
│   │   ├── pages/             # Main page components
│   │   ├── services/          # API service functions
│   │   └── utils/             # Utility functions
│   ├── package.json           # Node.js dependencies
│   └── tailwind.config.js     # Tailwind CSS configuration
│
├── docs/                       # Documentation and guides
│   ├── DEPLOYMENT.md          # Deployment instructions
│   ├── TESTING_GUIDE.md       # Testing procedures
│   └── SETUP_GUIDE.md         # Detailed setup instructions
│
├── scripts/                    # Utility and setup scripts
│   ├── import_all_data.py     # Data import utilities
│   ├── test_app.py            # Application testing
│   └── check_db.py            # Database verification
│
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker containerization
├── Procfile                   # Process configuration for deployment
└── README.md                  # This file
```

## 🧪 Testing

### Backend Testing
```bash
# Comprehensive application testing
python test_app.py

# Database connectivity testing
python test_backend_connectivity.py

# Authentication flow testing
python test_session_fix.py

# API endpoint testing
powershell -ExecutionPolicy Bypass -File test_api_endpoints.ps1  # Windows
```

### Frontend Testing
```bash
cd frontend

# Run React tests
npm test

# Build production version
npm run build

# Test production build locally
npx serve -s build
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions, please reach out through:
- GitHub Issues
- Project documentation
- Contact the development team

## 🎯 Future Enhancements

- [ ] Mobile application development
- [ ] Advanced ML models for species prediction
- [ ] Real-time data integration
- [ ] Multi-language support
- [ ] API documentation with Swagger
- [ ] Docker containerization

---

**Built with ❤️ for biodiversity conservation**
