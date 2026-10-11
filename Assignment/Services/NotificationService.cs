using Assignment.DTOs;
using Assignment.Hubs;
using Assignment.Services;
using Microsoft.AspNetCore.SignalR;

namespace Assignment.Services;

public class NotificationService(IHubContext<MonitoringHub> hub) : INotificationService
{
    public Task BroadcastIncidentAsync(LiveLocationDto dto, CancellationToken ct = default)
        => hub.Clients.Group("dashboard").SendAsync("ReceiveIncident", dto, ct);

    public Task BroadcastAlertAsync(AlertDto dto, CancellationToken ct = default)
        => hub.Clients.Group("dashboard").SendAsync("ReceiveAlert", dto, ct);
}
