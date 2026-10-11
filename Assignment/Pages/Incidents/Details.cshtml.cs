using Assignment.Data;
using Assignment.Models;
using Assignment.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Pages.Incidents;

[Authorize]
public class DetailsModel(
    ApplicationDbContext db,
    IIncidentService incidents,
    UserManager<ApplicationUser> users) : PageModel
{
    public IncidentReport? Item { get; set; }
    public SelectList Officers { get; set; } = default!;
    public SelectList StatusOptions => new(Enum.GetNames<IncidentStatus>());

    public async Task<IActionResult> OnGetAsync(int id)
    {
        Item = await db.IncidentReports
            .Include(i => i.IncidentType).Include(i => i.UserLocation)
            .Include(i => i.AssignedOfficer).Include(i => i.StatusHistory)
            .FirstOrDefaultAsync(i => i.Id == id);
        if (Item is null) return Page();
        var officers = await users.Users.OrderBy(u => u.Email).Take(100).ToListAsync();
        Officers = new SelectList(officers, nameof(ApplicationUser.Id), nameof(ApplicationUser.Email), Item.AssignedOfficerId);
        return Page();
    }

    public async Task<IActionResult> OnPostAssignAsync(int id, string officerId)
    {
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString();
        await incidents.AssignAsync(id, officerId, User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value, ip);
        return RedirectToPage(new { id });
    }

    public async Task<IActionResult> OnPostStatusAsync(int id, IncidentStatus next, string? comment)
    {
        var userId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString();
        await incidents.ChangeStatusAsync(id, next, comment, userId, User.Identity?.Name, ip);
        if (next == IncidentStatus.Resolved && !string.IsNullOrWhiteSpace(comment))
        {
            var incident = await db.IncidentReports.FindAsync(id);
            if (incident is not null)
            {
                incident.ResolutionNotes = comment;
                await db.SaveChangesAsync();
            }
        }
        return RedirectToPage(new { id });
    }
}
