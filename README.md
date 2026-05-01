---
title: NoShowIQ
emoji: 🏥
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# NoShowIQ

![CI/CD](https://github.com/jawadalishafaqat/noshow-iq-06ec810/actions/workflows/ci-cd.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Live Demo:** https://jawad209-noshow-iq-06ec810.hf.space

## 🏥 Overview

**NoShowIQ** is an intelligent patient appointment no-show prediction system. It uses machine learning to predict the probability that a patient will miss their scheduled medical appointment, enabling healthcare providers to take proactive measures such as sending reminders or overbooking strategically.

## ✨ Features

- **Real-time Predictions**: Get instant no-show risk predictions for patients
- **Risk Stratification**: Classify patients into HIGH, MEDIUM, or LOW risk categories
- **Actionable Recommendations**: Get specific actions based on risk level:
  - **HIGH Risk**: Send SMS reminder + confirmation call, consider double-booking
  - **MEDIUM Risk**: Send SMS reminder 24 hours before appointment
  - **LOW Risk**: No action needed
- **REST API**: Easy integration with healthcare systems
- **Lightweight Docker Image**: ~300MB optimized container for quick deployment
- **Machine Learning Model**: Trained Random Forest classifier on historical appointment data

## 🚀 Quick Start

### Using HuggingFace Spaces (Recommended)

Visit the [live demo](https://jawad209-noshow-iq-06ec810.hf.space) to test the API directly.

### Local Development

#### Prerequisites

- Python 3.11+
- Docker (optional)

#### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jawadalishafaqat/noshow-iq-66337.git
   cd noshow-iq-66337
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API**
   ```bash
   uvicorn noshow_iq.api:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
docker build -t noshow-iq .
docker run -p 7860:7860 noshow-iq
```

## 📖 API Documentation

### Endpoint: `/predict`

**Method:** `POST`

**Request Body:**
```json
{
  "Age": 35,
  "days_in_advance": 10,
  "appointment_dow": 2
}
```

**Response:**
```json
{
  "risk_level": "MEDIUM",
  "probability": 0.35,
  "recommendation": "Send SMS reminder 24h before."
}
```

### Request Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `Age` | integer | Patient age in years | 35 |
| `days_in_advance` | integer | Days between booking and appointment | 10 |
| `appointment_dow` | integer | Day of week (0=Monday, 6=Sunday) | 2 |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `risk_level` | string | Risk classification: HIGH, MEDIUM, or LOW |
| `probability` | float | Probability of no-show (0.0 to 1.0) |
| `recommendation` | string | Recommended action |

## 🤖 Model Information

- **Algorithm**: Random Forest Classifier
- **Features**: Age, days in advance, appointment day of week
- **Training Data**: Historical appointment data
- **Performance**: Optimized for healthcare decision-making

## 📦 Project Structure

```
.
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Multi-service orchestration
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── noshow_iq/
│   ├── __init__.py
│   ├── api.py              # FastAPI application
│   ├── model.py            # Model loading and prediction logic
│   ├── db.py               # Database connections
│   ├── schema.py           # Data models and validation
│   └── preprocess.py       # Data preprocessing utilities
├── models/
│   └── model.pkl           # Trained Random Forest model
├── tests/
│   ├── test_api.py
│   ├── test_model.py
│   └── test_preprocess.py
└── notebooks/
    └── _eda.ipynb          # Exploratory Data Analysis
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run specific test:

```bash
pytest tests/test_model.py::test_predict_high_risk -v
```

## 📊 Development

### Running Tests Locally

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=noshow_iq tests/
```

### Code Quality

```bash
# Run linting
flake8 noshow_iq/

# Format code
black noshow_iq/
```

## 🐳 Docker Image Size

The Docker image is optimized to **~300MB** for efficient deployment:

- **Slim Python Base**: Reduces base image from 1GB+ to minimal size
- **Multi-stage Build**: Separates build and runtime dependencies
- **Dependency Cleanup**: Removes unnecessary files and cache

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions, please open an [issue](https://github.com/jawadalishafaqat/noshow-iq-66337/issues) on GitHub.

---

**Last Updated:** May 2026  
**Status:** Active Development  
**CI/CD**: Automated tests and deployment via GitHub Actions