using Assignment.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Pages.Admin.Users;

[Authorize(Roles = "SuperAdmin,Administrator")]
public class IndexModel(UserManager<ApplicationUser> users) : PageModel
{
    public List<(ApplicationUser User, IList<string> Roles)> Items { get; set; } = [];
    public SelectList RoleOptions => new(Roles.All);

    public async Task OnGetAsync()
    {
        var list = await users.Users.OrderBy(u => u.Email).Take(200).ToListAsync();
        foreach (var u in list)
            Items.Add((u, await users.GetRolesAsync(u)));
    }

    public async Task<IActionResult> OnPostRoleAsync(string userId, string role)
    {
        var user = await users.FindByIdAsync(userId);
        if (user is null || !Roles.All.Contains(role)) return RedirectToPage();
        var current = await users.GetRolesAsync(user);
        await users.RemoveFromRolesAsync(user, current);
        await users.AddToRoleAsync(user, role);
        return RedirectToPage();
    }
}
