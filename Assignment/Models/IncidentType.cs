using System.ComponentModel.DataAnnotations;

namespace Assignment.Models;

public class IncidentType
{
    public int Id { get; set; }

    [Required, MaxLength(100)]
    public string Name { get; set; } = string.Empty;

    [MaxLength(500)]
    public string? Description { get; set; }

    public RiskLevel DefaultRiskLevel { get; set; } = RiskLevel.Medium;

    /// <summary>Weight 0-100 used by the early-warning engine.</summary>
    [Range(0, 100)]
    public int SeverityWeight { get; set; } = 30;

    public bool IsActive { get; set; } = true;

    public ICollection<IncidentReport> Incidents { get; set; } = new List<IncidentReport>();
}
