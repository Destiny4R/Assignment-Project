using Assignment.Data;
using Assignment.DTOs;
using Assignment.Models;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Services;

public interface IIncidentService
{
    Task<IncidentReport> CreateAsync(IncidentSubmitDto dto, UserLocation location, CancellationToken ct = default);
    Task<DashboardStats> GetStatsAsync(CancellationToken ct = default);
    Task ChangeStatusAsync(int id, IncidentStatus next, string? comment, string? userId, string? userName, string? ip, CancellationToken ct = default);
    Task AssignAsync(int id, string officerId, string? actorId, string? ip, CancellationToken ct = default);
    string NextReferenceNumber();
}

public record DashboardStats(int Total, int Active, int Today, int Critical, int Unresolved);

public class IncidentService(ApplicationDbContext db, IRiskAssessmentService risk, IAuditService audit) : IIncidentService
{
    public string NextReferenceNumber()
    {
        var max = db.IncidentReports.Any() ? db.IncidentReports.Max(i => i.Id) : 0;
        return $"INC-{(max + 1):D5}";
    }

    public async Task<IncidentReport> CreateAsync(IncidentSubmitDto dto, UserLocation location, CancellationToken ct = default)
    {
        var type = await db.IncidentTypes.FindAsync([dto.IncidentTypeId], ct)
                   ?? throw new ArgumentException("Unknown incident type.");
        var incident = new IncidentReport
        {
            ReferenceNumber = NextReferenceNumber(),
            UserLocationId = location.Id,
            IncidentTypeId = type.Id,
            IncidentType = type,
            Description = dto.Description.Trim(),
            Latitude = location.Latitude,
            Longitude = location.Longitude,
            ReporterName = dto.ReporterName?.Trim(),
            ReporterContact = dto.ReporterContact?.Trim(),
            Community = dto.Community?.Trim(),
            Lga = dto.Lga?.Trim(),
            Status = IncidentStatus.New,
            ReportedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };
        var (score, level) = await risk.EvaluateAsync(incident, ct);
        incident.RiskScore = score;
        incident.RiskLevel = level;

        db.IncidentReports.Add(incident);
        await db.SaveChangesAsync(ct);

        db.IncidentStatusHistories.Add(new IncidentStatusHistory
        {
            IncidentReportId = incident.Id,
            OldStatus = "-",
            NewStatus = IncidentStatus.New.ToString(),
            Comment = "Report submitted by public user.",
            ChangedAt = DateTime.UtcNow
        });
        await db.SaveChangesAsync(ct);
        return incident;
    }

    public async Task<DashboardStats> GetStatsAsync(CancellationToken ct = default)
    {
        var today = DateTime.UtcNow.Date;
        var total = await db.IncidentReports.CountAsync(ct);
        var active = await db.IncidentReports.CountAsync(i => i.Status != IncidentStatus.Resolved, ct);
        var todays = await db.IncidentReports.CountAsync(i => i.ReportedAt >= today, ct);
        var critical = await db.IncidentReports.CountAsync(i => i.RiskLevel == RiskLevel.Critical && i.Status != IncidentStatus.Resolved, ct);
        return new DashboardStats(total, active, todays, critical, active);
    }

    public async Task ChangeStatusAsync(int id, IncidentStatus next, string? comment, string? userId, string? userName, string? ip, CancellationToken ct = default)
    {
        var incident = await db.IncidentReports.FindAsync([id], ct)
                       ?? throw new KeyNotFoundException("Incident not found.");
        var old = incident.Status;
        incident.Status = next;
        incident.UpdatedAt = DateTime.UtcNow;
        if (next == IncidentStatus.Resolved) incident.ResolvedAt = DateTime.UtcNow;

        db.IncidentStatusHistories.Add(new IncidentStatusHistory
        {
            IncidentReportId = id,
            OldStatus = old.ToString(),
            NewStatus = next.ToString(),
            Comment = comment,
            ChangedById = userId,
            ChangedByName = userName,
            ChangedAt = DateTime.UtcNow
        });
        await db.SaveChangesAsync(ct);
        await audit.LogAsync(userId, $"Status {old}->{next}", "IncidentReport", id.ToString(), ip,
            $"{incident.ReferenceNumber}: {comment}", ct);
    }

    public async Task AssignAsync(int id, string officerId, string? actorId, string? ip, CancellationToken ct = default)
    {
        var incident = await db.IncidentReports.FindAsync([id], ct)
                       ?? throw new KeyNotFoundException("Incident not found.");
        incident.AssignedOfficerId = officerId;
        incident.UpdatedAt = DateTime.UtcNow;
        await db.SaveChangesAsync(ct);
        await audit.LogAsync(actorId, "Officer assigned incident", "IncidentReport", id.ToString(), ip,
            $"{incident.ReferenceNumber} assigned to {officerId}", ct);
    }
}
