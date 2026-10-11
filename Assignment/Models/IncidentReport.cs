using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Assignment.Models;

public class IncidentReport
{
    public int Id { get; set; }

    [Required, MaxLength(20)]
    public string ReferenceNumber { get; set; } = string.Empty; // e.g. INC-00025

    public int UserLocationId { get; set; }
    public UserLocation? UserLocation { get; set; }

    public int IncidentTypeId { get; set; }
    public IncidentType? IncidentType { get; set; }

    [Required, MaxLength(2000)]
    public string Description { get; set; } = string.Empty;

    public RiskLevel RiskLevel { get; set; } = RiskLevel.Medium;

    /// <summary>Computed 0-100 score from RiskAssessmentService.</summary>
    [Range(0, 100)]
    public int RiskScore { get; set; }

    public IncidentStatus Status { get; set; } = IncidentStatus.New;

    public DateTime ReportedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? ResolvedAt { get; set; }

    /// <summary>Denormalised coords for fast GIS queries (copied from UserLocation).</summary>
    public double Latitude { get; set; }
    public double Longitude { get; set; }

    [MaxLength(150)]
    public string? ReporterName { get; set; }

    [MaxLength(50)]
    public string? ReporterContact { get; set; }

    [MaxLength(150)]
    public string? Community { get; set; }

    [MaxLength(150)]
    public string? Lga { get; set; }

    [MaxLength(450)]
    public string? AssignedOfficerId { get; set; }

    [ForeignKey(nameof(AssignedOfficerId))]
    public ApplicationUser? AssignedOfficer { get; set; }

    [MaxLength(2000)]
    public string? ResolutionNotes { get; set; }

    public ICollection<IncidentStatusHistory> StatusHistory { get; set; } = new List<IncidentStatusHistory>();
    public ICollection<IncidentEvidence> Evidence { get; set; } = new List<IncidentEvidence>();
}
