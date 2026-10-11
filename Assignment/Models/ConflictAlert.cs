using System.ComponentModel.DataAnnotations;

namespace Assignment.Models;

public class ConflictAlert
{
    public int Id { get; set; }

    [Required, MaxLength(200)]
    public string Title { get; set; } = string.Empty;

    [Required, MaxLength(2000)]
    public string Message { get; set; } = string.Empty;

    public double Latitude { get; set; }
    public double Longitude { get; set; }

    /// <summary>Monitoring radius in kilometres.</summary>
    public double RadiusKm { get; set; } = 5;

    public RiskLevel RiskLevel { get; set; } = RiskLevel.High;

    [MaxLength(50)]
    public string TriggerType { get; set; } = "Frequency"; // Frequency | Proximity | Severity | Manual

    public int IncidentCount { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public bool IsAcknowledged { get; set; }

    public DateTime? AcknowledgedAt { get; set; }

    [MaxLength(450)]
    public string? AcknowledgedById { get; set; }

    [MaxLength(50)]
    public string Status { get; set; } = "New"; // New -> Acknowledged -> Investigating -> ActionTaken -> Resolved
}
