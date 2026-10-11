using Assignment.Data;
using Assignment.Hubs;
using Assignment.Models;
using Assignment.Services;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((ctx, cfg) => cfg.ReadFrom.Configuration(ctx.Configuration));

var conn = builder.Configuration.GetConnectionString("DefaultConnection")
           ?? "server=localhost;port=3306;database=FarmerHerderConflictDb;user=root;password=root;";
ServerVersion serverVersion;
try { serverVersion = ServerVersion.AutoDetect(conn); }
catch { serverVersion = new MySqlServerVersion(new Version(8, 0, 36)); }

builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(o => { o.IdleTimeout = TimeSpan.FromHours(2); });

builder.Services.AddDbContext<ApplicationDbContext>(o =>
    o.UseMySql(conn, serverVersion));

builder.Services.AddIdentity<ApplicationUser, IdentityRole>(o =>
    {
        o.SignIn.RequireConfirmedAccount = false;
        o.Password.RequireDigit = true;
        o.Password.RequiredLength = 6;
        o.Password.RequireNonAlphanumeric = false;
        o.Password.RequireUppercase = false;
    })
    .AddEntityFrameworkStores<ApplicationDbContext>()
    .AddDefaultTokenProviders();

builder.Services.ConfigureApplicationCookie(o =>
{
    o.LoginPath = "/Account/Login";
    o.AccessDeniedPath = "/Account/AccessDenied";
});

builder.Services.AddRazorPages(o =>
{
    o.Conventions.AuthorizeFolder("/Dashboard");
    o.Conventions.AuthorizeFolder("/Incidents");
    o.Conventions.AuthorizeFolder("/Map");
    o.Conventions.AuthorizeFolder("/Admin");
});
builder.Services.AddSignalR();

// Domain services (Plan §10 early-warning engine + GIS)
builder.Services.AddScoped<IGisService, GisService>();
builder.Services.AddScoped<IRiskAssessmentService, RiskAssessmentService>();
builder.Services.AddScoped<ILocationService, LocationService>();
builder.Services.AddScoped<IIncidentService, IncidentService>();
builder.Services.AddScoped<IAlertService, AlertService>();
builder.Services.AddScoped<IAuditService, AuditService>();
builder.Services.AddScoped<INotificationService, NotificationService>();

var app = builder.Build();

// Auto-migrate + seed roles/admin (dev convenience; use `dotnet ef migrations` for schema changes)
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var db = services.GetRequiredService<ApplicationDbContext>();
        await db.Database.MigrateAsync();
        var users = services.GetRequiredService<UserManager<ApplicationUser>>();
        var roles = services.GetRequiredService<RoleManager<IdentityRole>>();
        await DbInitializer.SeedAsync(db, users, roles);
    }
    catch (Exception ex)
    {
        var logger = services.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "Database migration/seed failed. Check MySQL connection string.");
    }
}

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();
app.UseSession();

app.MapRazorPages();
app.MapHub<MonitoringHub>("/monitoringHub");

app.Run();
