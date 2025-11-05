# US National Park Tracker

This is a small web app to track which US National Parks you've visited, find the nearest park to your current location, and explore a modern satellite map. The frontend uses MapLibre (open-source) with Esri World Imagery as the basemap (no Mapbox token required).

Features
- Mark parks as visited/unvisited (stored in your browser localStorage).
- Use your device location to find the nearest park and the nearest unvisited park.
- 3D-like pitched satellite view for a modern look.

Quick start (Windows PowerShell)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. (Optional) If you want richer park details from the National Park Service, set the NPS API key in your environment:

```powershell
$env:NPS_API_KEY  = 'WALq8zo8uIz6e7uCk4yxyuFCKqCdfH137ShBwICg'
```

3. Run the app:

```powershell
python main.py
```

4. Open http://127.0.0.1:5000/ in your browser.

Notes and limitations
- The project ships a small curated list of major national parks in `data/parks.json`. You can expand this dataset as needed.
- The app uses MapLibre GL JS with Esri World Imagery tiles for satellite imagery (no Mapbox token required). True terrain/exaggeration (DEM) usually requires separate elevation tile sources that may need API keys; for a free setup we provide a pitched 3D-like satellite view and stylized park/tree markers.
- The "trees" are represented as green points at park locations for a stylized visual—full tree coverage mapping would require additional datasets and more advanced styling.

Next steps (suggestions)
- Add park boundary polygons and draw realistic forest coverage using public datasets.
- Add user accounts or export/import visited lists.
- Use an offline tileset or tile server for production offline use.
