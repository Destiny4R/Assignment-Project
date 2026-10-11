using System.ComponentModel.DataAnnotations;

namespace Assignment.Models;

/// <summary>Configurable early-warning thresholds (never hard-code scoring).</summary>
public class RiskRule
{
    public int Id { get; set; }

    [Required, MaxLength(150)]
    public string Name { get; set; } = string.Empty;

    [MaxLength(1000)]
    public string? Description { get; set; }

    /// <summary>Incidents within RadiusKm + TimeWindowHours to trigger.</summary>
    [Range(1, 1000)]
    public int MinIncidentCount { get; set; } = 3;

    [Range(0.1, 500)]
    public double RadiusKm { get; set; } = 5;

    [Range(1, 720)]
    public int TimeWindowHours { get; set; } = 24;

    [Range(0, 100)]
    public int HighRiskThreshold { get; set; } = 50;

    [Range(0, 100)]
    public int CriticalRiskThreshold { get; set; } = 75;

    public bool IsActive { get; set; } = true;

    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}
