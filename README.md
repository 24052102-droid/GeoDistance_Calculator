# 🌍 GeoDistance Visualizer

A Python-based geographic distance calculator that retrieves location coordinates from Wikipedia, calculates real-world distances using the Haversine formula, and generates an interactive map visualization between places.

---

## 📌 Features

✅ Automatic coordinate extraction from Wikipedia API  
✅ Persistent local caching for faster lookups  
✅ Great-circle distance calculation using Haversine formula  
✅ Interactive map generation with markers and routes  
✅ Coordinate validation and error handling  
✅ Modular and maintainable project structure  
✅ Automatic browser launch for generated maps  

---

## 🏗️ Project Structure

```text
GeoDistance-Visualizer/
│
├── src/
│   ├── extraction/
│   │   ├── wiki_fetcher.py
│   │   └── coordinate_extractor.py
│   │
│   ├── preprocessing/
│   │   └── validation.py
│   │
│   ├── distance/
│   │   ├── haversine.py
│   │   └── distance_engine.py
│   │
│   ├── visualization/
│   │   └── map_plotter.py
│   │
│   └── utils/
│       ├── cache_manager.py
│       └── logger.py
│
├── data/
│   └── cache/
│       └── location_cache.json
│
├── outputs/
│   └── maps/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/GeoDistance-Visualizer.git
```

Move into the project directory:

```bash
cd GeoDistance-Visualizer
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS / Git Bash

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📦 Required Packages

```txt
requests>=2.31.0
folium>=0.16.0
```

Install manually:

```bash
pip install requests folium
```

---

## ▶️ Running the Project

Run:

```bash
python main.py
```

The program will ask for two locations:

Example:

```text
=== Geographic Distance Calculator ===

Enter first place: Tokyo
Enter second place: London
```

Output:

```text
----------------------------------------
RESULTS
----------------------------------------

Tokyo                    35.68972, 139.69222
London                   51.50722, -0.12750

Distance: 9,558.72 km

Map saved → outputs/maps/distance_map.html
```

The generated map opens automatically in your browser.

---

## 🗺️ Example Visualization

The generated map contains:

- Location markers
- Connecting route line
- Distance label
- Interactive zoom and navigation

---

## 🔍 How it Works

### Step 1:
User enters two place names

⬇

### Step 2:
Coordinates are searched in local cache

⬇

### Step 3:
If not cached, Wikipedia API fetches coordinates

⬇

### Step 4:
Coordinates are validated

⬇

### Step 5:
Distance is calculated using the Haversine formula

⬇

### Step 6:
An interactive map is generated using Folium

---

## 🧮 Distance Formula

The project uses the Haversine formula to compute great-circle distances between two points on Earth:

:contentReference[oaicite:0]{index=0}

Where:

- `r` = Earth's radius (6371 km)
- Latitude and longitude values are converted to radians

---

## 🚀 Future Improvements

- GUI using Tkinter or PyQt
- Multiple route support
- Distance unit conversion (km/miles)
- Use OpenStreetMap or Google Maps APIs
- Route optimization between multiple cities
- Docker deployment
