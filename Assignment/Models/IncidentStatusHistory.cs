using System.ComponentModel.DataAnnotations;

namespace Assignment.Models;

public class IncidentStatusHistory
{
    public int Id { get; set; }

    public int IncidentReportId { get; set; }
    public IncidentReport? IncidentReport { get; set; }

    [Required, MaxLength(50)]
    public string OldStatus { get; set; } = string.Empty;

    [Required, MaxLength(50)]
    public string NewStatus { get; set; } = string.Empty;

    [MaxLength(1000)]
    public string? Comment { get; set; }

    [MaxLength(450)]
    public string? ChangedById { get; set; }

    [MaxLength(150)]
    public string? ChangedByName { get; set; }

    public DateTime ChangedAt { get; set; } = DateTime.UtcNow;
}
