# US National Park Tracker

This is a small web app to track which US National Parks you've visited, find the nearest park to your current location, and show a modern 3D satellite map with terrain. It uses Mapbox GL JS for the map (requires a Mapbox access token).

Features
- Mark parks as visited/unvisited (stored in your browser localStorage).
- Use your device location to find the nearest park and the nearest unvisited park.
- 3D satellite map with terrain exaggeration and sky for a modern look.

Quick start (Windows PowerShell)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Get a Mapbox access token (https://www.mapbox.com/) and set it in your environment:

```powershell
$env:MAPBOX_TOKEN = 'pk.your_mapbox_token_here'
```

3. Run the app:

```powershell
python main.py
```

4. Open http://127.0.0.1:5000/ in your browser.

Notes and limitations
- The project ships a small curated list of major national parks in `data/parks.json`. You can expand this dataset as needed.
- Mapbox is used for satellite tiles and DEM for terrain. You must provide a token. If you prefer open-source tile providers, the frontend can be adapted to MapLibre and different tile sources.
- The "trees" are represented as green points at park locations for a stylized visual—full tree coverage mapping would require additional datasets and more advanced styling.

Next steps (suggestions)
- Add park boundary polygons and draw realistic forest coverage using public datasets.
- Add user accounts or export/import visited lists.
- Use an offline tileset or tile server for production offline use.
