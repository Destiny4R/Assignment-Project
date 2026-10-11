using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.SignalR;

namespace Assignment.Hubs;

/// <summary>Real-time channel: public submissions -> admin dashboard/live map (Plan Phase 5).</summary>
[Authorize]
public class MonitoringHub : Hub
{
    public async Task JoinDashboard()
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, "dashboard");
    }

    public async Task LeaveDashboard()
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, "dashboard");
    }
}
