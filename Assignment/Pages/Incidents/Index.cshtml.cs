using Assignment.Data;
using Assignment.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Pages.Incidents;

[Authorize]
public class IndexModel(ApplicationDbContext db) : PageModel
{
    public string? Q { get; set; }
    public string? Status { get; set; }
    public string? Risk { get; set; }
    public int? TypeId { get; set; }

    public List<IncidentReport> Items { get; set; } = [];
    public SelectList StatusOptions => new(Enum.GetNames<IncidentStatus>());
    public SelectList RiskOptions => new(Enum.GetNames<RiskLevel>());
    public SelectList TypeOptions { get; set; } = default!;

    public async Task OnGetAsync(string? q, string? status, string? risk, int? typeId)
    {
        Q = q; Status = status; Risk = risk; TypeId = typeId;
        var query = db.IncidentReports.Include(i => i.IncidentType).Include(i => i.AssignedOfficer).AsQueryable();
        if (!string.IsNullOrWhiteSpace(q))
            query = query.Where(i => i.ReferenceNumber.Contains(q) || i.Description.Contains(q) || (i.Community != null && i.Community.Contains(q)));
        if (Enum.TryParse<IncidentStatus>(status, out var st)) query = query.Where(i => i.Status == st);
        if (Enum.TryParse<RiskLevel>(risk, out var rl)) query = query.Where(i => i.RiskLevel == rl);
        if (typeId.HasValue) query = query.Where(i => i.IncidentTypeId == typeId);
        Items = await query.OrderByDescending(i => i.ReportedAt).Take(200).ToListAsync();
        var types = await db.IncidentTypes.OrderBy(t => t.Name).ToListAsync();
        TypeOptions = new SelectList(types, nameof(IncidentType.Id), nameof(IncidentType.Name));
    }
}
