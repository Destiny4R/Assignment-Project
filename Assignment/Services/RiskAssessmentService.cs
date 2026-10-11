using Assignment.Data;
using Assignment.Models;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Services;

public interface IRiskAssessmentService
{
    int CalculateScore(int severityWeight, int nearbyCount, int ruleThreshold);
    RiskLevel Classify(int score, int highThreshold, int criticalThreshold);
    Task<(int Score, RiskLevel Level)> EvaluateAsync(IncidentReport incident, CancellationToken ct = default);
}

public class RiskAssessmentService(ApplicationDbContext db, IGisService gis) : IRiskAssessmentService
{
    /// <summary>
    /// score = clamp(severity*0.6 + frequencyComponent*0.4), where frequencyComponent
    /// scales nearbyCount relative to the configured rule threshold.
    /// Thresholds themselves come from RiskRule (configurable, not hard-coded).
    /// </summary>
    public int CalculateScore(int severityWeight, int nearbyCount, int ruleThreshold)
    {
        var freq = ruleThreshold <= 0 ? 0 : Math.Min(100, nearbyCount * 100 / Math.Max(1, ruleThreshold));
        var score = (int)Math.Round(severityWeight * 0.6 + freq * 0.4);
        return Math.Clamp(score, 0, 100);
    }

    public RiskLevel Classify(int score, int highThreshold, int criticalThreshold)
    {
        if (score >= criticalThreshold) return RiskLevel.Critical;
        if (score >= highThreshold) return RiskLevel.High;
        if (score >= 25) return RiskLevel.Medium;
        return RiskLevel.Low;
    }

    public async Task<(int Score, RiskLevel Level)> EvaluateAsync(IncidentReport incident, CancellationToken ct = default)
    {
        var rule = await db.RiskRules.FirstOrDefaultAsync(r => r.IsActive, ct)
                   ?? new RiskRule { MinIncidentCount = 3, RadiusKm = 5, TimeWindowHours = 24, HighRiskThreshold = 50, CriticalRiskThreshold = 75 };
        var typeWeight = incident.IncidentType?.SeverityWeight ?? 30;
        var nearby = await gis.GetNearbyAsync(incident.Latitude, incident.Longitude, rule.RadiusKm, rule.TimeWindowHours, ct);
        // Exclude self if already persisted.
        var count = nearby.Count(n => n.Id != incident.Id);
        var score = CalculateScore(typeWeight, count, rule.MinIncidentCount);
        return (score, Classify(score, rule.HighRiskThreshold, rule.CriticalRiskThreshold));
    }
}
