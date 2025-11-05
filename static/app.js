// Minimal frontend for National Park Tracker using MapLibre (open-source)
// We use Esri World Imagery raster tiles for satellite imagery (no API key required).

const style = {
  version: 8,
  sources: {
    'esri': {
      type: 'raster',
      tiles: ['https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
      tileSize: 256
    }
  },
  layers: [
    { id: 'esri', type: 'raster', source: 'esri' }
  ]
};

const map = new maplibregl.Map({
  container: 'map',
  style: style,
  center: [-98.5795, 39.8283], // center of USA
  zoom: 3.5,
  pitch: 45,
  bearing: -17.6,
  antialias: true
});

map.on('load', () => {
  // MapLibre doesn't provide Mapbox DEM tiles for free; true terrain/exaggeration
  // needs separate DEM tiles which often require an API key. For now we keep a pitched
  // satellite view and add stylized park/tree markers.

  fetch('/api/parks').then(r => r.json()).then(parks => {
    window.PARKS = parks;
    renderParks(parks);
  });
});

// Haversine distance in kilometers
function haversine(lat1, lon1, lat2, lon2) {
  function toRad(x){return x*Math.PI/180;}
  const R = 6371; // km
  const dLat = toRad(lat2-lat1);
  const dLon = toRad(lon2-lon1);
  const a = Math.sin(dLat/2)*Math.sin(dLat/2) + Math.cos(toRad(lat1))*Math.cos(toRad(lat2))*Math.sin(dLon/2)*Math.sin(dLon/2);
  const c = 2*Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R*c;
}

function renderParks(parks){
  const list = document.getElementById('park-list');
  list.innerHTML = '';

  const visited = loadVisited();

  parks.forEach(park => {
    // add marker (simple circle)
    const el = document.createElement('div');
    el.className = 'marker';
    if (visited.includes(park.id)) el.classList.add('visited');

    const marker = new maplibregl.Marker({element: el})
      .setLngLat([park.lon, park.lat])
      .setPopup(new maplibregl.Popup({offset:25}).setHTML(`<strong>${park.name}</strong><div>${park.state}</div>`))
      .addTo(map);

  // list item
  const li = document.createElement('li');
  li.innerHTML = `<div class="park-row"><div class="park-info"><a href="#" class="park-link" data-id="${park.id}"><strong>${park.name}</strong></a><div class="muted">${park.state}</div></div><div class="park-actions"><button data-id="${park.id}" class="visit-toggle">${visited.includes(park.id)?'Visited':'Mark visited'}</button></div></div>`;
  list.appendChild(li);
  });

  // add tree-like visual layer: small green circles at park locations
  if (map.getLayer && map.getLayer('parks-points')) map.removeLayer('parks-points');
  if (map.getSource && map.getSource('parks-points')) map.removeSource('parks-points');

  const features = parks.map(p => ({ type: 'Feature', geometry: { type: 'Point', coordinates: [p.lon, p.lat] }, properties: { id: p.id } }));
  map.addSource('parks-points', { type: 'geojson', data: { type: 'FeatureCollection', features } });
  map.addLayer({
    id: 'parks-points',
    type: 'circle',
    source: 'parks-points',
    paint: {
      'circle-color': '#2b9348',
      'circle-radius': 6,
      'circle-opacity': 0.9,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#072'
    }
  });

  attachListHandlers();
  updateNearestInfo();
}

function attachListHandlers(){
  document.querySelectorAll('.visit-toggle').forEach(btn => {
    btn.onclick = () => {
      const id = btn.getAttribute('data-id');
      toggleVisited(id);
      // update label and refresh markers
      btn.textContent = isVisited(id) ? 'Visited' : 'Mark visited';
      // rebuild map markers quickly by re-rendering parks
      renderParks(window.PARKS || []);
    };
  });
  // park link clicks -> show details
  document.querySelectorAll('.park-link').forEach(a => {
    a.addEventListener('click', (ev) => {
      ev.preventDefault();
      const id = a.getAttribute('data-id');
      showParkDetails(id);
    });
  });
}

function loadVisited(){
  try{
    const raw = localStorage.getItem('visited_parks') || '[]';
    return JSON.parse(raw);
  }catch(e){return []}
}

function saveVisited(arr){ localStorage.setItem('visited_parks', JSON.stringify(arr)); }

function isVisited(id){ return loadVisited().includes(id); }

function toggleVisited(id){
  const arr = loadVisited();
  const idx = arr.indexOf(id);
  if (idx >= 0) arr.splice(idx,1); else arr.push(id);
  saveVisited(arr);
}

function resetVisited(){ localStorage.removeItem('visited_parks'); renderParks(window.PARKS || []); }

document.getElementById('reset-visited').addEventListener('click', () => {
  if (confirm('Reset visited parks?')) resetVisited();
});

document.getElementById('locate-btn').addEventListener('click', () => {
  if (!navigator.geolocation) return alert('Geolocation not supported');
  navigator.geolocation.getCurrentPosition(pos => {
    const lat = pos.coords.latitude, lon = pos.coords.longitude;
    document.getElementById('your-location').textContent = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
    map.flyTo({ center: [lon, lat], zoom: 6 });
    updateNearestInfo(lat, lon);
  }, err => alert('Could not get location: ' + err.message));
});

function updateNearestInfo(lat=null, lon=null){
  if (!lat || !lon){
    // try to use browser geolocation silently
    if (navigator.geolocation){
      navigator.geolocation.getCurrentPosition(pos => updateNearestInfo(pos.coords.latitude, pos.coords.longitude), ()=>{
        // fallback: center of USA
        calcNearest(39.8283, -98.5795);
      });
      return;
    } else {
      calcNearest(39.8283, -98.5795);
      return;
    }
  }
  calcNearest(lat, lon);
}

function calcNearest(lat, lon){
  const parks = window.PARKS || [];
  if (!parks.length) return;
  let nearest = null, nearestDist = Infinity;
  let nearestUnvisited = null, nearestUnvisitedDist = Infinity;
  const visited = loadVisited();

  parks.forEach(p => {
    const d = haversine(lat, lon, p.lat, p.lon);
    if (d < nearestDist){ nearestDist = d; nearest = p; }
    if (!visited.includes(p.id) && d < nearestUnvisitedDist){ nearestUnvisitedDist = d; nearestUnvisited = p; }
  });

  document.getElementById('nearest-park').textContent = nearest ? `${nearest.name} (${nearestDist.toFixed(1)} km)` : '—';
  document.getElementById('nearest-unvisited').textContent = nearestUnvisited ? `${nearestUnvisited.name} (${nearestUnvisitedDist.toFixed(1)} km)` : '—';

  // highlight nearest on the map with a popup and camera
  if (nearest){
    new maplibregl.Popup({closeOnClick:false})
      .setLngLat([nearest.lon, nearest.lat])
      .setHTML(`<strong>${nearest.name}</strong><div>${nearest.state}</div><div>${nearestDist.toFixed(1)} km away</div>`)
      .addTo(map);
  }
}

// Modal helpers
function showModal(){ document.getElementById('park-modal').classList.remove('hidden'); }
function hideModal(){ document.getElementById('park-modal').classList.add('hidden'); }
document.getElementById('modal-close').addEventListener('click', hideModal);

let lastKnownLocation = null;
if (navigator.geolocation){
  navigator.geolocation.getCurrentPosition(pos => { lastKnownLocation = {lat: pos.coords.latitude, lon: pos.coords.longitude}; }, ()=>{});
}

function showParkDetails(id){
  const url = `/api/park/${encodeURIComponent(id)}`;
  fetch(url).then(r => r.json()).then(data => {
    const park = data.park || data;
    document.getElementById('modal-title').textContent = park.name || (park.fullName || 'Park');
    const gallery = document.getElementById('modal-gallery');
    gallery.innerHTML = '';
    if (data.nps && data.nps.images && data.nps.images.length){
      data.nps.images.slice(0,6).forEach(img => {
        const im = document.createElement('img');
        im.src = img.url;
        im.alt = img.altText || img.title || '';
        im.className = 'modal-img';
        gallery.appendChild(im);
      });
    } else {
      gallery.innerHTML = '<div class="muted">No images available</div>';
    }

    const info = document.getElementById('modal-info');
    let html = '';
    if (data.nps && data.nps.description) html += `<p>${data.nps.description}</p>`;
    if (data.nps && data.nps.directionsInfo) html += `<p><strong>Directions:</strong> ${data.nps.directionsInfo}</p>`;
    if (data.nps && data.nps.url) html += `<p><a target="_blank" href="${data.nps.url}">Official site</a></p>`;
    if (data.bestTimeToGo) html += `<p><strong>Best time to go:</strong> ${data.bestTimeToGo}</p>`;

    // distance
    if (lastKnownLocation){
      const d = haversine(lastKnownLocation.lat, lastKnownLocation.lon, park.lat, park.lon);
      html += `<p><strong>Distance:</strong> ${d.toFixed(1)} km</p>`;
    } else {
      html += `<p class="muted">Distance: enable location or use the "Use my location" button.</p>`;
    }

    info.innerHTML = html;
    showModal();
  }).catch(err => {
    alert('Failed to load park details: ' + err.message);
  });
}

// initial call
updateNearestInfo();
