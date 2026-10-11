using Assignment.Models;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Data;

public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<UserLocation> UserLocations => Set<UserLocation>();
    public DbSet<IncidentType> IncidentTypes => Set<IncidentType>();
    public DbSet<IncidentReport> IncidentReports => Set<IncidentReport>();
    public DbSet<ConflictAlert> ConflictAlerts => Set<ConflictAlert>();
    public DbSet<IncidentEvidence> IncidentEvidence => Set<IncidentEvidence>();
    public DbSet<IncidentStatusHistory> IncidentStatusHistories => Set<IncidentStatusHistory>();
    public DbSet<RiskRule> RiskRules => Set<RiskRule>();
    public DbSet<AdministrativeArea> AdministrativeAreas => Set<AdministrativeArea>();
    public DbSet<AuditLog> AuditLogs => Set<AuditLog>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        builder.Entity<IncidentReport>(e =>
        {
            e.HasIndex(x => x.ReferenceNumber).IsUnique();
            e.HasIndex(x => new { x.Latitude, x.Longitude });
            e.HasIndex(x => x.ReportedAt);
            e.HasIndex(x => x.Status);
            e.Property(x => x.ReferenceNumber).HasMaxLength(20).IsRequired();
            e.HasOne(x => x.UserLocation).WithMany(l => l.Incidents)
                .HasForeignKey(x => x.UserLocationId).OnDelete(DeleteBehavior.Restrict);
            e.HasOne(x => x.IncidentType).WithMany(t => t.Incidents)
                .HasForeignKey(x => x.IncidentTypeId).OnDelete(DeleteBehavior.Restrict);
        });

        builder.Entity<UserLocation>(e =>
        {
            e.HasIndex(x => x.ReceivedAt);
        });

        builder.Entity<ConflictAlert>(e =>
        {
            e.HasIndex(x => x.CreatedAt);
            e.HasIndex(x => x.IsAcknowledged);
        });

        builder.Entity<AdministrativeArea>(e =>
        {
            e.HasOne(x => x.Parent).WithMany()
                .HasForeignKey(x => x.ParentId).OnDelete(DeleteBehavior.Restrict);
        });

        // Seed incident types (Plan §9 / §13)
        builder.Entity<IncidentType>().HasData(
            new IncidentType { Id = 1, Name = "Suspicious Activity", Description = "Unusual movement or gathering that may precede conflict.", DefaultRiskLevel = RiskLevel.Low, SeverityWeight = 20, IsActive = true },
            new IncidentType { Id = 2, Name = "Farmer/Herder Dispute", Description = "Verbal or land-use disagreement between farmers and herders.", DefaultRiskLevel = RiskLevel.Medium, SeverityWeight = 40, IsActive = true },
            new IncidentType { Id = 3, Name = "Livestock Intrusion", Description = "Cattle grazing on farmland / crop intrusion.", DefaultRiskLevel = RiskLevel.Medium, SeverityWeight = 35, IsActive = true },
            new IncidentType { Id = 4, Name = "Threat", Description = "Reported threat of attack or reprisal.", DefaultRiskLevel = RiskLevel.High, SeverityWeight = 60, IsActive = true },
            new IncidentType { Id = 5, Name = "Crop/Property Destruction", Description = "Destruction of crops, property or livestock.", DefaultRiskLevel = RiskLevel.High, SeverityWeight = 65, IsActive = true },
            new IncidentType { Id = 6, Name = "Physical Conflict", Description = "Active violent confrontation in progress.", DefaultRiskLevel = RiskLevel.Critical, SeverityWeight = 90, IsActive = true },
            new IncidentType { Id = 7, Name = "Other", Description = "Any other security-relevant report.", DefaultRiskLevel = RiskLevel.Low, SeverityWeight = 15, IsActive = true }
        );

        // Seed default risk rule (Plan §14 configurable scoring)
        builder.Entity<RiskRule>().HasData(
            new RiskRule
            {
                Id = 1,
                Name = "Default hotspot rule",
                Description = "3+ incidents within 5km in 24h triggers hotspot evaluation.",
                MinIncidentCount = 3,
                RadiusKm = 5,
                TimeWindowHours = 24,
                HighRiskThreshold = 50,
                CriticalRiskThreshold = 75,
                IsActive = true
            }
        );

        // Seed Benue-state context areas (operating area default ~ Makurdi 7.7322, 8.5391)
        builder.Entity<AdministrativeArea>().HasData(
            new AdministrativeArea { Id = 1, Name = "Benue State", AreaType = "State", Latitude = 7.7322, Longitude = 8.5391, IsActive = true },
            new AdministrativeArea { Id = 2, Name = "Makurdi", AreaType = "LGA", ParentId = 1, Latitude = 7.7322, Longitude = 8.5391, IsActive = true },
            new AdministrativeArea { Id = 3, Name = "Guma", AreaType = "LGA", ParentId = 1, Latitude = 7.78, Longitude = 8.65, IsActive = true },
            new AdministrativeArea { Id = 4, Name = "Logo", AreaType = "LGA", ParentId = 1, Latitude = 7.55, Longitude = 9.05, IsActive = true }
        );
    }
}
