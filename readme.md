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

### Example Endpoint

```
GET /detect?lat=38.6270&lon=-90.1994
```

**Query Parameters**:

* `lat`: Latitude of the location
* `lon`: Longitude of the location

**Response**:

```json
{
  "water_bodies": [
    {
      "name": "Mississippi River",
      "distance_km": 1.5,
      "landmarks": [...],
      "parcel_info": {...}
    },
    ...
  ]
}
```

---

## 📁 Project Structure

```
.
├── main.py                # FastAPI entry point
├── detection_service.py   # Core water body detection logic
├── utils/
│   └── google_places.py   # Google API logic
│   └── report_all.py      # Parcel API logic
├── .env                   # Environment config
└── requirements.txt       # Python dependencies
```

---

## 🧪 Sample Output

```bash
curl "http://localhost:8000/detect?lat=38.6270&lon=-90.1994"
```

---

## 🧠 Future Improvements

* Integrate satellite-based water segmentation (Sentinel-2/Landsat)
* Cache and rate-limit API requests
* Add UI dashboard for results visualization
* Dockerize and deploy on cloud (GCP/AWS)

---

## 🤝 Contributions

Pull requests and issues are welcome! Please ensure code is formatted and tested.

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 🧑‍💻 Developed by

**Prathamesh Apptware Team**
Built with ❤️ for geospatial intelligence and environmental awareness.

```


