// gps.js — Consent-only location share (no form fields).
// Flow: consent checkbox -> Share button -> geolocation -> OSM reverse geocode
// (nearest place name) -> POST ?handler=Submit. No continuous tracking.
(function () {
    const btn = document.getElementById('btnShare');
    const retry = document.getElementById('btnRetry');
    const status = document.getElementById('gpsStatus');
    const box = document.getElementById('submitResult');
    const consent = document.getElementById('consent');
    if (!btn) return;

    function setStatus(msg, cls) {
        if (!status) return;
        status.textContent = msg;
        status.className = 'alert ' + cls;
    }
    function show(id, v) {
        const el = document.getElementById(id);
        if (el) el.textContent = v;
    }
    function setBusy(busy) {
        btn.disabled = busy;
        btn.textContent = busy ? 'Sharing…' : 'Share my location now';
    }

    async function reverseGeocode(lat, lon) {
        // OpenStreetMap Nominatim reverse geocode (best-effort; may be unavailable offline).
        try {
            const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}&zoom=14`;
            const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
            if (!res.ok) return null;
            const json = await res.json();
            return json.display_name || null;
        } catch {
            return null;
        }
    }

    async function submitShare(pos) {
        const { latitude, longitude, accuracy, altitude, speed, heading } = pos.coords;
        show('showLat', latitude.toFixed(6));
        show('showLon', longitude.toFixed(6));
        show('showAcc', accuracy != null ? Math.round(accuracy) + ' m' : 'n/a');

        setStatus('Resolving nearest known place…', 'alert-warning');
        const place = await reverseGeocode(latitude, longitude);
        show('showPlace', place || 'resolving on server…');

        setStatus('Sending your location…', 'alert-warning');
        const token = document.querySelector('input[name="__RequestVerificationToken"]')?.value;
        const data = {
            latitude, longitude,
            accuracy: accuracy ?? null,
            altitude: altitude ?? null,
            speed: speed ?? null,
            heading: heading ?? null,
            capturedAt: new Date(pos.timestamp).toISOString(),
            consent: true,
            nearestPlace: place
        };
        const res = await fetch('?handler=Submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'RequestVerificationToken': token || '' },
            body: JSON.stringify(data)
        });
        if (res.ok) {
            const json = await res.json();
            show('showPlace', json.nearestPlace || place || '—');
            setStatus('Location shared. Thank you — officers have been notified.', 'alert-success');
            if (box) box.innerHTML = `<div class="alert alert-success">Location received. Reference: <strong>${json.referenceNumber}</strong><br/>Nearest place: ${json.nearestPlace || '—'}</div>`;
            if (retry) retry.classList.remove('d-none');
        } else {
            const text = await res.text();
            setStatus('Sharing failed. You can retry.', 'alert-danger');
            if (box) box.innerHTML = `<div class="alert alert-danger">Submission failed: ${text}</div>`;
            if (retry) retry.classList.remove('d-none');
        }
        setBusy(false);
    }

    function fail(err) {
        setBusy(false);
        if (retry) retry.classList.remove('d-none');
        switch (err.code) {
            case err.PERMISSION_DENIED:
                setStatus('Permission denied. Enable location access and try again.', 'alert-danger');
                break;
            case err.POSITION_UNAVAILABLE:
                setStatus('Position unavailable. Check GPS signal and retry.', 'alert-danger');
                break;
            case err.TIMEOUT:
                setStatus('Location request timed out. Try again.', 'alert-danger');
                break;
            default:
                setStatus('Could not obtain location: ' + err.message, 'alert-danger');
        }
    }

    btn.addEventListener('click', () => {
        if (box) box.innerHTML = '';
        if (!consent || !consent.checked) {
            setStatus('Please tick the consent box first — your location is only shared with consent.', 'alert-warning');
            return;
        }
        if (!('geolocation' in navigator)) {
            setStatus('Geolocation is not supported by this browser.', 'alert-danger');
            return;
        }
        setStatus('Requesting location permission…', 'alert-warning');
        setBusy(true);
        navigator.geolocation.getCurrentPosition(submitShare, fail, {
            enableHighAccuracy: true, timeout: 15000, maximumAge: 0
        });
    });

    if (retry) retry.addEventListener('click', () => btn.click());
})();
