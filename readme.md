```markdown
# 🌊 Water Body Detection API

This project provides a RESTful API service for detecting and locating water bodies near a given coordinate. It integrates with Overpass API (OSM), Google Places API, and the ReportAllUSA Parcel API to provide accurate parcel and landmark data around water bodies.

---

## 🚀 Features

- Detect nearby water bodies based on latitude and longitude
- Fetch parcel information from ReportAllUSA API
- Retrieve landmarks and places via Google Places API
- Async and optimized for fast response
- Modular code structure for scalability

---

## 🏗️ Architecture

```

Client ➝ FastAPI Server ➝ External APIs:
├── Overpass (OSM)
├── Google Places API
└── ReportAllUSA API

````

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
````

### Environment Variables

Create a `.env` file or set the following environment variables:

```env
GOOGLE_MAPS_KEY=your_google_maps_api_key
REPORT_ALL_KEY=your_report_all_api_key
```

---

## ⚙️ Usage

### Start the API

```bash
uvicorn main:app --reload
```

## 🧑‍💻 Developed by

**Prathamesh Apptware Team**
Built with ❤️ for geospatial intelligence and environmental awareness.
