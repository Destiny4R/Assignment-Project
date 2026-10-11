using System.ComponentModel.DataAnnotations;

namespace Assignment.Models;

public class AdministrativeArea
{
    public int Id { get; set; }

    [Required, MaxLength(150)]
    public string Name { get; set; } = string.Empty;

    [MaxLength(50)]
    public string AreaType { get; set; } = "LGA"; // State | LGA | Community

    public int? ParentId { get; set; }
    public AdministrativeArea? Parent { get; set; }

    public double? Latitude { get; set; }
    public double? Longitude { get; set; }

    /// <summary>Optional GeoJSON polygon for map boundary layer.</summary>
    public string? BoundaryGeoJson { get; set; }

    public bool IsActive { get; set; } = true;
}
