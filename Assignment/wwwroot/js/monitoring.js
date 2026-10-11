// monitoring.js — Plan Phase 5: SignalR live feed, no page refresh.
function connectMonitoring(handlers) {
    if (typeof signalR === 'undefined') {
        console.warn('SignalR client not loaded.');
        return null;
    }
    const connection = new signalR.HubConnectionBuilder()
        .withUrl('/monitoringHub')
        .withAutomaticReconnect()
        .build();

    connection.on('ReceiveIncident', (dto) => {
        if (typeof addLiveMarker === 'function') addLiveMarker(dto);
        const rows = document.getElementById('incidentRows');
        if (rows) {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td class="small fw-bold">${dto.referenceNumber}</td>` +
                `<td class="small">${dto.incidentType || ''}</td>` +
                `<td><span class="badge bg-warning text-dark">${dto.riskLevel}</span></td>` +
                `<td class="small">${new Date(dto.reportedAt).toLocaleTimeString()}</td>` +
                `<td class="small">${dto.status}</td>` +
                `<td><a class="btn btn-sm btn-outline-primary" href="/Incidents/Details/${dto.id}">View location</a></td>`;
            rows.prepend(tr);
        }
        toast(`New incident ${dto.referenceNumber} (${dto.riskLevel})`);
        if (handlers && handlers.onStats) handlers.onStats({});
    });

    connection.on('ReceiveAlert', (dto) => {
        const banner = document.getElementById('alertBanner');
        if (banner) {
            banner.innerHTML = `<div class="alert alert-danger"><strong>${dto.title}</strong><br/>${dto.message} ` +
                `<a href="/Map/Index?focus=${dto.latitude},${dto.longitude}" class="alert-link">View on map</a></div>`;
        }
        toast(dto.title);
    });

    connection.start()
        .then(() => connection.invoke('JoinDashboard'))
        .catch((err) => console.error(err));
    return connection;
}

function toast(msg) {
    // Minimal non-blocking notification; replace with Toastr if desired.
    const el = document.createElement('div');
    el.textContent = msg;
    el.style.cssText = 'position:fixed;bottom:16px;right:16px;background:#212529;color:#fff;padding:10px 14px;border-radius:6px;z-index:9999;opacity:0.95;';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 4500);
}
