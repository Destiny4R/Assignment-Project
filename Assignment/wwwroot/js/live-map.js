// live-map.js — Plan Phase 7/9: Leaflet map with risk-coloured markers + GeoJSON layers.
let _map = null;
let _markers = null;

function riskColor(risk) {
    switch ((risk || '').toLowerCase()) {
        case 'critical': return 'red';
        case 'high': return 'orange';
        case 'medium': return 'gold';
        case 'low': return 'green';
        default: return 'blue';
    }
}

function markerFor(dto) {
    const color = riskColor(dto.riskLevel || dto.risk);
    const icon = L.divIcon({
        className: 'risk-marker',
        html: `<span style="display:inline-block;width:16px;height:16px;border-radius:50%;background:${color};border:2px solid #fff;box-shadow:0 0 4px #000;"></span>`,
        iconSize: [20, 20]
    });
    const m = L.marker([dto.latitude, dto.longitude], { icon });
    const ref = dto.referenceNumber || dto.reference || ('#' + dto.id);
    m.bindPopup(`<strong>${ref}</strong><br/>Risk: ${dto.riskLevel || dto.risk}<br/>Status: ${dto.status || ''}<br/><a href="/Incidents/Details/${dto.id}">View incident</a>`);
    return m;
}

function initLiveMap(elementId, seed, opts) {
    const el = document.getElementById(elementId);
    if (!el || typeof L === 'undefined') return null;
    const center = (opts && opts.center) || [7.7322, 8.5391];
    const zoom = (opts && opts.zoom) || 10;
    _map = L.map(elementId).setView(center, zoom);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(_map);
    _markers = L.layerGroup().addTo(_map);
    (seed || []).forEach(addLiveMarker);
    return _map;
}

function addLiveMarker(dto) {
    if (!_markers) return;
    try { _markers.addLayer(markerFor(dto)); } catch (e) { console.warn(e); }
}

function loadGeoJson(geojson) {
    if (!_map || !geojson) return;
    L.geoJSON(geojson, {
        pointToLayer: (feature, latlng) => {
            const p = feature.properties || {};
            if (p.kind === 'hotspot') {
                return L.circle(latlng, { radius: (p.radiusKm || 5) * 1000, color: 'red', fillOpacity: 0.15 });
            }
            if (p.kind === 'alert') {
                return L.circleMarker(latlng, { radius: 10, color: 'red' })
                    .bindPopup(`<strong>${p.title}</strong><br/>${p.count} incidents within ${p.radiusKm}km`);
            }
            const color = riskColor(p.risk);
            return L.circleMarker(latlng, { radius: 7, color, fillColor: color, fillOpacity: 0.9 })
                .bindPopup(`<strong>${p.reference}</strong><br/>Risk: ${p.risk}<br/>Status: ${p.status}<br/><a href="/Incidents/Details/${p.id}">View incident</a>`);
        }
    }).addTo(_map);
}

function focusOn(lat, lon, zoom) {
    if (_map) _map.setView([lat, lon], zoom || 14);
}
