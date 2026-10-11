using Assignment.Data;
using Assignment.DTOs;
using Assignment.Models;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Services;

public interface IGisService
{
    double HaversineKm(double lat1, double lon1, double lat2, double lon2);
    bool IsWithinRadius(double centerLat, double centerLon, double lat, double lon, double radiusKm);
    Task<List<IncidentReport>> GetNearbyAsync(double lat, double lon, double radiusKm, int hoursBack, CancellationToken ct = default);
    Task<List<HotspotResult>> DetectHotspotsAsync(CancellationToken ct = default);
    Task<NearestArea?> FindNearestAreaAsync(double lat, double lon, CancellationToken ct = default);
    object ToGeoJson(IEnumerable<IncidentReport> incidents, IEnumerable<ConflictAlert>? alerts = null, IEnumerable<HotspotResult>? hotspots = null);
}

public record NearestArea(string Name, string AreaType, double DistanceKm);

public class GisService(ApplicationDbContext db) : IGisService
{
    private const double EarthKm = 6371.0;

    public double HaversineKm(double lat1, double lon1, double lat2, double lon2)
    {
        var dLat = ToRad(lat2 - lat1);
        var dLon = ToRad(lon2 - lon1);
        var a = Math.Sin(dLat / 2) * Math.Sin(dLat / 2) +
                Math.Cos(ToRad(lat1)) * Math.Cos(ToRad(lat2)) *
                Math.Sin(dLon / 2) * Math.Sin(dLon / 2);
        return 2 * EarthKm * Math.Asin(Math.Sqrt(a));
    }

    public bool IsWithinRadius(double centerLat, double centerLon, double lat, double lon, double radiusKm)
        => HaversineKm(centerLat, centerLon, lat, lon) <= radiusKm;

    public async Task<List<IncidentReport>> GetNearbyAsync(double lat, double lon, double radiusKm, int hoursBack, CancellationToken ct = default)
    {
        var since = DateTime.UtcNow.AddHours(-hoursBack);
        // Coarse bounding-box prefilter (~111km per degree) then precise Haversine.
        var latDelta = radiusKm / 111.0;
        var lonDelta = radiusKm / (111.0 * Math.Max(0.2, Math.Cos(ToRad(lat))));
        var candidates = await db.IncidentReports
            .Where(i => i.ReportedAt >= since &&
                        i.Latitude >= lat - latDelta && i.Latitude <= lat + latDelta &&
                        i.Longitude >= lon - lonDelta && i.Longitude <= lon + lonDelta)
            .ToListAsync(ct);
        return candidates.Where(i => HaversineKm(lat, lon, i.Latitude, i.Longitude) <= radiusKm).ToList();
    }

    /// <summary>Naive clustering: for each unassigned incident, gather neighbours
    /// within the active rule radius/time window; emit clusters meeting MinIncidentCount.</summary>
    public async Task<List<HotspotResult>> DetectHotspotsAsync(CancellationToken ct = default)
    {
        var rule = await db.RiskRules.Where(r => r.IsActive).FirstOrDefaultAsync(ct)
                   ?? new RiskRule { MinIncidentCount = 3, RadiusKm = 5, TimeWindowHours = 24, HighRiskThreshold = 50, CriticalRiskThreshold = 75 };
        var since = DateTime.UtcNow.AddHours(-rule.TimeWindowHours);
        var recent = await db.IncidentReports
            .Where(i => i.ReportedAt >= since && i.Status != IncidentStatus.Resolved)
            .ToListAsync(ct);

        var hotspots = new List<HotspotResult>();
        var assigned = new HashSet<int>();
        foreach (var seed in recent)
        {
            if (assigned.Contains(seed.Id)) continue;
            var cluster = recent
                .Where(i => HaversineKm(seed.Latitude, seed.Longitude, i.Latitude, i.Longitude) <= rule.RadiusKm)
                .ToList();
            if (cluster.Count >= rule.MinIncidentCount)
            {
                var avgLat = cluster.Average(i => i.Latitude);
                var avgLon = cluster.Average(i => i.Longitude);
                var maxScore = cluster.Max(i => i.RiskScore);
                var level = maxScore >= rule.CriticalRiskThreshold ? RiskLevel.Critical
                    : maxScore >= rule.HighRiskThreshold ? RiskLevel.High
                    : RiskLevel.Medium;
                hotspots.Add(new HotspotResult
                {
                    CenterLatitude = avgLat,
                    CenterLongitude = avgLon,
                    IncidentCount = cluster.Count,
                    RadiusKm = rule.RadiusKm,
                    RiskLevel = level.ToString(),
                    IncidentIds = cluster.Select(i => i.Id).ToList()
                });
                foreach (var i in cluster) assigned.Add(i.Id);
            }
        }
        return hotspots;
    }

    /// <summary>Nearest seeded administrative area ("known location by name").</summary>
    public async Task<NearestArea?> FindNearestAreaAsync(double lat, double lon, CancellationToken ct = default)
    {
        var areas = await db.AdministrativeAreas
            .Where(a => a.IsActive && a.Latitude.HasValue && a.Longitude.HasValue)
            .ToListAsync(ct);
        NearestArea? best = null;
        foreach (var a in areas)
        {
            var d = HaversineKm(lat, lon, a.Latitude!.Value, a.Longitude!.Value);
            if (best is null || d < best.DistanceKm)
                best = new NearestArea(a.Name, a.AreaType, d);
        }
        return best;
    }

    public object ToGeoJson(IEnumerable<IncidentReport> incidents, IEnumerable<ConflictAlert>? alerts = null, IEnumerable<HotspotResult>? hotspots = null)
    {
        var features = new List<object>();
        foreach (var i in incidents)
        {
            features.Add(new
            {
                type = "Feature",
                geometry = new { type = "Point", coordinates = new[] { i.Longitude, i.Latitude } },
                properties = new
                {
                    kind = "incident",
                    id = i.Id,
                    reference = i.ReferenceNumber,
                    risk = i.RiskLevel.ToString(),
                    score = i.RiskScore,
                    status = i.Status.ToString(),
                    type = i.IncidentType?.Name,
                    reportedAt = i.ReportedAt
                }
            });
        }
        if (alerts is not null)
            foreach (var a in alerts)
                features.Add(new
                {
                    type = "Feature",
                    geometry = new { type = "Point", coordinates = new[] { a.Longitude, a.Latitude } },
                    properties = new { kind = "alert", id = a.Id, title = a.Title, risk = a.RiskLevel.ToString(), count = a.IncidentCount, radiusKm = a.RadiusKm }
                });
        if (hotspots is not null)
            foreach (var h in hotspots)
                features.Add(new
                {
                    type = "Feature",
                    geometry = new { type = "Point", coordinates = new[] { h.CenterLongitude, h.CenterLatitude } },
                    properties = new { kind = "hotspot", count = h.IncidentCount, risk = h.RiskLevel, radiusKm = h.RadiusKm }
                });
        return new { type = "FeatureCollection", features };
    }

    private static double ToRad(double d) => d * Math.PI / 180.0;
}
