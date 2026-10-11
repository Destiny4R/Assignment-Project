using Assignment.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Pages.Admin.RiskRules;

[Authorize(Roles = "SuperAdmin,Administrator")]
public class IndexModel(ApplicationDbContext db) : PageModel
{
    public List<Models.RiskRule> Items { get; set; } = [];

    public async Task OnGetAsync()
        => Items = await db.RiskRules.OrderBy(r => r.Id).ToListAsync();
}
