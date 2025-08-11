# BiodivProScope - Biodiversity Protection Scope

A full-stack application for biodiversity assessment and environmental risk analysis.

## 🌿 About

BiodivProScope is a comprehensive platform designed to help researchers, conservationists, and environmental professionals assess biodiversity risks and implement effective mitigation strategies. The application provides interactive mapping, species analysis, and risk assessment tools.

## 🚀 Features

- **Interactive Map Visualization**: Leaflet-based mapping with MarkerCluster support
- **Species Risk Assessment**: Advanced algorithms for biodiversity risk calculation
- **Environmental Data Analysis**: Comprehensive analysis of freshwater, marine, and terrestrial ecosystems
- **Report Generation**: PDF report generation with detailed analysis
- **User Management**: Secure authentication and user profiles
- **Responsive Design**: Modern UI with Material-UI and Tailwind CSS

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

### 2. Backend Setup

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

# Set up environment variables (create .env file)
# Add your database URL and other configurations

# Run the Flask application
python app.py
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

## 🌐 Deployment

### Free Hosting Options

#### Frontend (React)
- **Vercel** - Recommended for React apps
- **Netlify** - Great for static sites with continuous deployment
- **GitHub Pages** - Free hosting for static sites

#### Backend (Flask)
- **Railway** - Modern platform with PostgreSQL support
- **Render** - Free tier with easy deployment
- **Heroku** - Classic platform (limited free tier)

#### Database
- **Railway** - Integrated PostgreSQL
- **Supabase** - PostgreSQL with additional features
- **ElephantSQL** - Managed PostgreSQL

## 📁 Project Structure

```
bioscope-project/
├── backend/
│   ├── api/                 # API routes
│   ├── database/            # Database models and setup
│   ├── services/            # Business logic
│   ├── utils/               # Utility functions
│   ├── ML Strategy/         # Machine learning components
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/             # Static assets
│   ├── src/                # React components and logic
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind configuration
└── README.md
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
