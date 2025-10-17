# CureHelp+   |    AI-Powered Health Risk Analyzer

<div align="center">

![CureHelp+](https://img.shields.io/badge/CureHelp+-Healthcare_AI-blue?style=for-the-badge&logo=medical)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)

**Your Personal Health Companion for Predictive Diagnostics and Medical Assistance**

[![Demo](https://img.shields.io/badge/🚀-Live_Demo-2EA043?style=for-the-badge)](https://curehelp.streamlit.app)
[![Documentation](https://img.shields.io/badge/📚-Documentation-8A2BE2?style=for-the-badge)](#documentation)
[![Issues](https://img.shields.io/badge/🐛-Report_Issues-FF6B6B?style=for-the-badge)](https://github.com/your-repo/issues)

</div>

## 🌟 Overview

CureHelp+ is an advanced healthcare analytics platform that leverages machine learning to provide comprehensive health risk assessments, predictive diagnostics, and personalized medical guidance. Our application combines cutting-edge AI models with user-friendly interfaces to deliver actionable health insights. Also medical assistant is integrated with large amount of medical data.

---

## Author
Made with ❤️ By: **Asim Husain** https://www.asimhusain.dev

---

## Accessibility
- **Custom Domain** www.curehelplus.me
- **Docker Image** https://hub.docker.com/r/asimhusain/myapp
- **Azure ContainerApp** https://curehelplus.yellowforest-948fb34f.centralindia.azurecontainerapps.io

---

### Key Features

- 🧠 **Multi-Disease Risk Prediction** - Diabetes, Heart Disease, Fever, Anemia
- 🤖 **AI Medical Assistant** - Symptom analysis and disease information
- 📊 **Interactive Visualizations** - Risk gauges and comparative analysis
- 👨‍⚕️ **Healthcare Provider Directory** - Nearby hospitals and specialists
- 📋 **Patient Profile Management** - Secure health record storage
- 📄 **PDF Report Generation** - Comprehensive health reports
- 💊 **Clinical Guidance** - Prevention measures and medication suggestions
- 🐳 **Dockerized Deployment** - Easy setup with Docker image and container
- 🌐 **Azure & Custom Domain Deployment** - Accessible via cloud and personalized domain


---

## Machine Learning Models
## Model Architecture

| Disease | Algorithm | Accuracy | Features | Special Notes |
|---------|-----------|----------|----------|---------------|
| **Diabetes** | Ensemble Classifier | 95% | 8 features | Handles gender-specific parameters |
| **Heart Disease** | Random Forest | 96% | 13 features | Comprehensive cardiac assessment |
| **Fever** | Dual Random Forest | 96% | 18 features | Severity + Risk classification |
| **Anemia** | Multi-output RF | 94% | 14 features | Risk + Type prediction |

---

## Usage

1.  **Landing Page:** Upon launching the application, you will be greeted by the landing page. Click on "Get Started" to proceed.
2.  **Patient Details:** Fill in your personal details to create a profile. This information will be used to personalize the predictions and reports.
3.  **Input Health Metrics:** Navigate through the different tabs for each disease (Diabetes, Heart Disease, Fever, Anemia) and enter your health metrics.
4.  **Predict Risk:** Click on the "Predict" button to get your risk assessment.
5.  **View Results:** The results will be displayed with interactive gauges and charts, along with AI-powered recommendations.
6.  **Generate Report:** Go to the "Report" tab to view a summary of all your predictions and download a consolidated PDF report.
7.  **Docker Usage:** Pull the Docker image from [Docker Hub](https://hub.docker.com/r/asimhusain/myapp) and run it locally.
      - docker pull asimhusain/myapp
      - docker run -p 8501:8501 asimhusain/myapp
8.  **Cloud Deployment:** Access the deployed app on Azure Container Apps here or via the custom domain www.curehelplus.me


## Performance Metrics

### Model Performance
- **Overall Accuracy**: 84.75% average across all models
- **Precision**: 90-94% range depending on disease
- **Recall**: 89-94% for critical condition detection  
- **F1-Score**: 91% balanced performance metric

### System Performance
- **Response Time**: < 2 seconds for predictions
- **Concurrent Users**: Support for multiple simultaneous sessions
- **Memory Usage**: Optimized model loading and caching
- **Scalability**: Modular architecture for easy expansion

### Privacy & Security

### Data Protection
- **Local Storage**: All user data stored locally
- **No Cloud Transmission**: Privacy-first approach
- **Anonymous Analytics**: Optional usage statistics
- **Data Encryption**: Secure profile management

---

### Medical Disclaimer
> ⚠️ **Important**: CureHelp+ is designed for informational purposes only and does not provide medical diagnosis. Always consult qualified healthcare professionals for medical advice and treatment. The predictions are based on machine learning models and should be used as supplementary information only.

---

## 🌟 Contributing

I welcome contributions from the community!

---

##  Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/curehelp-plus.git
   cd curehelp-plus

2. **Start On Local**
   ```bash
   streamlit run app.py
   - http://localhost:8501
   
3. **Run Using Docker (Optional)**
   ```bash
   docker pull asim123/myapp
   docker run -p 8501:8501 asim123/myapp
   - Open http://localhost:8501 in your browser.

4. **Cloud Access**
- Azure Container Apps Deployment: https://curehelplus.yellowforest-948fb34f.centralindia.azurecontainerapps.io
- Custom Domain: www.curehelplus.me
