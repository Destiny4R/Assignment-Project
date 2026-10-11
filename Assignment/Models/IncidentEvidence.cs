using System.ComponentModel.DataAnnotations;

namespace Assignment.Models;

public class IncidentEvidence
{
    public int Id { get; set; }

    public int IncidentReportId { get; set; }
    public IncidentReport? IncidentReport { get; set; }

    [Required, MaxLength(500)]
    public string FilePath { get; set; } = string.Empty;

    [MaxLength(100)]
    public string? FileType { get; set; }

    public DateTime UploadedAt { get; set; } = DateTime.UtcNow;

    [MaxLength(450)]
    public string? UploadedById { get; set; }
}
