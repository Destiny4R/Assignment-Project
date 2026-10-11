using Assignment.Data;
using Assignment.DTOs;
using Assignment.Models;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Services;

public interface IAlertService
{
    Task<List<ConflictAlert>> CheckAndGenerateAsync(IncidentReport incident, CancellationToken ct = default);
    Task AcknowledgeAsync(int alertId, string? userId, string? ip, CancellationToken ct = default);
    Task<List<ConflictAlert>> GetActiveAsync(int take = 10, CancellationToken ct = default);
}

public class AlertService(ApplicationDbContext db, IGisService gis, IAuditService audit) : IAlertService
{
    public async Task<List<ConflictAlert>> CheckAndGenerateAsync(IncidentReport incident, CancellationToken ct = default)
    {
        var created = new List<ConflictAlert>();
        var rules = await db.RiskRules.Where(r => r.IsActive).ToListAsync(ct);
        foreach (var rule in rules)
        {
            var nearby = await gis.GetNearbyAsync(incident.Latitude, incident.Longitude, rule.RadiusKm, rule.TimeWindowHours, ct);
            // Avoid duplicate alerts: skip if an unacknowledged alert already covers this cluster.
            var recentCover = await db.ConflictAlerts
                .Where(a => !a.IsAcknowledged && a.CreatedAt >= DateTime.UtcNow.AddHours(-rule.TimeWindowHours))
                .ToListAsync(ct);
            if (recentCover.Any(a => gis.HaversineKm(a.Latitude, a.Longitude, incident.Latitude, incident.Longitude) <= a.RadiusKm))
                continue;

            if (nearby.Count >= rule.MinIncidentCount || incident.RiskLevel == RiskLevel.Critical)
            {
                var alert = new ConflictAlert
                {
                    Title = incident.RiskLevel == RiskLevel.Critical
                        ? "CRITICAL incident reported"
                        : "HIGH-RISK HOTSPOT DETECTED",
                    Message = incident.RiskLevel == RiskLevel.Critical
                        ? $"Critical {incident.IncidentType?.Name} ({incident.ReferenceNumber}) requires immediate response."
                        : $"Multiple incidents ({nearby.Count}) reported within {rule.RadiusKm}km in the last {rule.TimeWindowHours}h. Potential conflict hotspot.",
                    Latitude = incident.Latitude,
                    Longitude = incident.Longitude,
                    RadiusKm = rule.RadiusKm,
                    RiskLevel = incident.RiskLevel == RiskLevel.Critical ? RiskLevel.Critical : RiskLevel.High,
                    TriggerType = incident.RiskLevel == RiskLevel.Critical ? "Severity" : "Frequency",
                    IncidentCount = Math.Max(nearby.Count, 1),
                    CreatedAt = DateTime.UtcNow,
                    Status = "New"
                };
                db.ConflictAlerts.Add(alert);
                created.Add(alert);
            }
        }
        if (created.Count > 0) await db.SaveChangesAsync(ct);
        return created;
    }

    public async Task AcknowledgeAsync(int alertId, string? userId, string? ip, CancellationToken ct = default)
    {
        var alert = await db.ConflictAlerts.FindAsync([alertId], ct)
                    ?? throw new KeyNotFoundException("Alert not found.");
        alert.IsAcknowledged = true;
        alert.AcknowledgedAt = DateTime.UtcNow;
        alert.AcknowledgedById = userId;
        alert.Status = "Acknowledged";
        await db.SaveChangesAsync(ct);
        await audit.LogAsync(userId, "Officer acknowledged alert", "ConflictAlert", alertId.ToString(), ip,
            alert.Title, ct);
    }

    public Task<List<ConflictAlert>> GetActiveAsync(int take = 10, CancellationToken ct = default)
        => db.ConflictAlerts.OrderByDescending(a => a.CreatedAt).Take(take).ToListAsync(ct);
}

public interface IAuditService
{
    Task LogAsync(string? userId, string action, string? entity, string? entityId, string? ip, string? description, CancellationToken ct = default);
}

public class AuditService(ApplicationDbContext db) : IAuditService
{
    public async Task LogAsync(string? userId, string action, string? entity, string? entityId, string? ip, string? description, CancellationToken ct = default)
    {
        db.AuditLogs.Add(new AuditLog
        {
            UserId = userId,
            Action = action,
            Entity = entity,
            EntityId = entityId,
            IPAddress = ip,
            Description = description,
            Timestamp = DateTime.UtcNow
        });
        await db.SaveChangesAsync(ct);
    }
}

public interface INotificationService
{
    Task BroadcastIncidentAsync(LiveLocationDto dto, CancellationToken ct = default);
    Task BroadcastAlertAsync(AlertDto dto, CancellationToken ct = default);
}
