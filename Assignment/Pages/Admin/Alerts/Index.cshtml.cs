using Assignment.Data;
using Assignment.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Pages.Admin.Alerts;

[Authorize]
public class IndexModel(ApplicationDbContext db, IAlertService alerts) : PageModel
{
    public List<Models.ConflictAlert> Items { get; set; } = [];

    public async Task OnGetAsync()
        => Items = await db.ConflictAlerts.OrderByDescending(a => a.CreatedAt).Take(100).ToListAsync();

    public async Task<IActionResult> OnPostAckAsync(int id)
    {
        var userId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString();
        await alerts.AcknowledgeAsync(id, userId, ip);
        return RedirectToPage();
    }
}
