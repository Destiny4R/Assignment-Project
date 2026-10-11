using Assignment.Data;
using Assignment.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Pages.Dashboard;

[Authorize]
public class IndexModel(ApplicationDbContext db, IIncidentService incidents, IAlertService alerts) : PageModel
{
    public DashboardStats Stats { get; set; } = new(0, 0, 0, 0, 0);
    public List<Models.IncidentReport> Recent { get; set; } = [];
    public List<Models.ConflictAlert> Alerts { get; set; } = [];

    public async Task OnGetAsync()
    {
        Stats = await incidents.GetStatsAsync();
        Recent = await db.IncidentReports
            .Include(i => i.IncidentType)
            .OrderByDescending(i => i.ReportedAt)
            .Take(30)
            .ToListAsync();
        Alerts = await alerts.GetActiveAsync(10);
    }
}
