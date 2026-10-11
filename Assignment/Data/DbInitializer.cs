using Assignment.Models;
using Microsoft.AspNetCore.Identity;

namespace Assignment.Data;

public static class DbInitializer
{
    public static async Task SeedAsync(
        ApplicationDbContext db,
        UserManager<ApplicationUser> users,
        RoleManager<IdentityRole> roles)
    {
        foreach (var role in Roles.All)
        {
            if (!await roles.RoleExistsAsync(role))
                await roles.CreateAsync(new IdentityRole(role));
        }

        const string adminEmail = "admin@test.com";
        var admin = await users.FindByEmailAsync(adminEmail);
        if (admin is null)
        {
            admin = new ApplicationUser
            {
                UserName = adminEmail,
                Email = adminEmail,
                EmailConfirmed = true,
                FullName = "System Administrator"
            };
            await users.CreateAsync(admin, "Admin123!");
            await users.AddToRolesAsync(admin, [Roles.SuperAdmin, Roles.Admin]);
        }
    }
}
