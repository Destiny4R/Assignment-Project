using Assignment.Data;
using Assignment.Models;
using Assignment.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Pages.Map;

[Authorize]
public class IndexModel(ApplicationDbContext db, IGisService gis) : PageModel
{
    [BindProperty(SupportsGet = true)] public string? Risk { get; set; }
    [BindProperty(SupportsGet = true)] public string? Status { get; set; }
    [BindProperty(SupportsGet = true)] public DateTime? From { get; set; }
    [BindProperty(SupportsGet = true)] public DateTime? To { get; set; }
    [BindProperty(SupportsGet = true)] public bool ShowHotspots { get; set; } = true;

    public SelectList RiskOptions => new(Enum.GetNames<RiskLevel>());
    public SelectList StatusOptions => new(Enum.GetNames<IncidentStatus>());

    public void OnGet() { }

    public async Task<IActionResult> OnGetGeoJsonAsync(string? risk, string? status, DateTime? from, DateTime? to, bool showHotspots = true)
    {
        var q = db.IncidentReports.Include(i => i.IncidentType).AsQueryable();
        if (Enum.TryParse<RiskLevel>(risk, out var rl)) q = q.Where(i => i.RiskLevel == rl);
        if (Enum.TryParse<IncidentStatus>(status, out var st)) q = q.Where(i => i.Status == st);
        if (from.HasValue) q = q.Where(i => i.ReportedAt >= from.Value);
        if (to.HasValue) q = q.Where(i => i.ReportedAt <= to.Value.AddDays(1));
        var incidents = await q.OrderByDescending(i => i.ReportedAt).Take(500).ToListAsync();
        var alerts = await db.ConflictAlerts.OrderByDescending(a => a.CreatedAt).Take(20).ToListAsync();
        var hotspots = showHotspots ? await gis.DetectHotspotsAsync() : [];
        return new JsonResult(gis.ToGeoJson(incidents, alerts, hotspots));
    }
}
