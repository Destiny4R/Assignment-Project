using Assignment.Data;
using Assignment.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Assignment.Pages.Admin.RiskRules;

[Authorize(Roles = "SuperAdmin,Administrator")]
public class EditModel(ApplicationDbContext db, IAuditService audit) : PageModel
{
    [BindProperty]
    public Models.RiskRule Item { get; set; } = default!;

    public async Task<IActionResult> OnGetAsync(int id)
    {
        var rule = await db.RiskRules.FindAsync(id);
        if (rule is null) return NotFound();
        Item = rule;
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid) return Page();
        var rule = await db.RiskRules.FindAsync(Item.Id);
        if (rule is null) return NotFound();
        rule.Name = Item.Name;
        rule.Description = Item.Description;
        rule.MinIncidentCount = Item.MinIncidentCount;
        rule.RadiusKm = Item.RadiusKm;
        rule.TimeWindowHours = Item.TimeWindowHours;
        rule.HighRiskThreshold = Item.HighRiskThreshold;
        rule.CriticalRiskThreshold = Item.CriticalRiskThreshold;
        rule.IsActive = Item.IsActive;
        rule.UpdatedAt = DateTime.UtcNow;
        await db.SaveChangesAsync();
        var userId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
        await audit.LogAsync(userId, "Administrator changed risk configuration", "RiskRule", rule.Id.ToString(),
            HttpContext.Connection.RemoteIpAddress?.ToString(), rule.Name);
        return RedirectToPage("Index");
    }
}
