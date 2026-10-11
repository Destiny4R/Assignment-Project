using System.ComponentModel.DataAnnotations;

namespace Assignment.DTOs;

public class LocationDto
{
    [Range(-90, 90)]
    public double Latitude { get; set; }

    [Range(-180, 180)]
    public double Longitude { get; set; }

    [Range(0, 100000)]
    public double? Accuracy { get; set; }
    public double? Altitude { get; set; }
    public double? Speed { get; set; }
    public double? Heading { get; set; }
    public DateTime? CapturedAt { get; set; }
    public string? SessionId { get; set; }
}

public class IncidentSubmitDto : LocationDto
{
    [Range(1, int.MaxValue)]
    public int IncidentTypeId { get; set; }

    [Required, MaxLength(2000), MinLength(3)]
    public string Description { get; set; } = string.Empty;

    [MaxLength(150)]
    public string? ReporterName { get; set; }

    [MaxLength(50)]
    public string? ReporterContact { get; set; }

    [MaxLength(150)]
    public string? Community { get; set; }

    [MaxLength(150)]
    public string? Lga { get; set; }
}

public class LocationShareDto : LocationDto
{
    /// <summary>Explicit consent — must be true, otherwise rejected.</summary>
    public bool Consent { get; set; }

    /// <summary>Nearest place display name resolved client-side (OSM reverse geocode). Optional.</summary>
    [MaxLength(500)]
    public string? NearestPlace { get; set; }
}

public class LiveLocationDto
{
    public int Id { get; set; }
    public string ReferenceNumber { get; set; } = string.Empty;
    public double Latitude { get; set; }
    public double Longitude { get; set; }
    public string RiskLevel { get; set; } = "Medium";
    public int RiskScore { get; set; }
    public string Status { get; set; } = "New";
    public string IncidentType { get; set; } = string.Empty;
    public DateTime ReportedAt { get; set; }
}

public class AlertDto
{
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public double Latitude { get; set; }
    public double Longitude { get; set; }
    public double RadiusKm { get; set; }
    public string RiskLevel { get; set; } = "High";
    public int IncidentCount { get; set; }
    public DateTime CreatedAt { get; set; }
}

public class HotspotResult
{
    public double CenterLatitude { get; set; }
    public double CenterLongitude { get; set; }
    public int IncidentCount { get; set; }
    public double RadiusKm { get; set; }
    public string RiskLevel { get; set; } = "High";
    public List<int> IncidentIds { get; set; } = [];
}
