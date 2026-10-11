using System.ComponentModel.DataAnnotations;

namespace Assignment.Models;

/// <summary>Raw GPS fix submitted by a public user (Phase 1 / Phase 5).</summary>
public class UserLocation
{
    public int Id { get; set; }

    [MaxLength(64)]
    public string? SessionId { get; set; }

    [Range(-90, 90)]
    public double Latitude { get; set; }

    [Range(-180, 180)]
    public double Longitude { get; set; }

    /// <summary>GPS accuracy in metres (nullable — browser may omit).</summary>
    [Range(0, 100000)]
    public double? Accuracy { get; set; }

    public double? Altitude { get; set; }
    public double? Speed { get; set; }
    public double? Heading { get; set; }

    /// <summary>Client-side timestamp (browser clock).</summary>
    public DateTime CapturedAt { get; set; } = DateTime.UtcNow;

    /// <summary>Server-side receipt timestamp.</summary>
    public DateTime ReceivedAt { get; set; } = DateTime.UtcNow;

    public bool IsActive { get; set; } = true;

    [MaxLength(45)]
    public string? IpAddress { get; set; }

    public ICollection<IncidentReport> Incidents { get; set; } = new List<IncidentReport>();
}
