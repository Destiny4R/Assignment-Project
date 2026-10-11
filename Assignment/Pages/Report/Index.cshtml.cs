using Assignment.Data;
using Assignment.DTOs;
using Assignment.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Pages.Report;

public class IndexModel(
    ApplicationDbContext db,
    ILocationService locations,
    IIncidentService incidents,
    IAlertService alerts,
    INotificationService notify,
    IGisService gis,
    ILogger<IndexModel> logger) : PageModel
{
    public void OnGet()
    {
    }

    /// <summary>
    /// Consent-only location share: POST /Report?handler=Submit.
    /// Body: { latitude, longitude, accuracy, altitude, speed, heading, capturedAt, consent: true, nearestPlace? }.
    /// No incident-type/description form fields — a default report is created server-side.
    /// </summary>
    public async Task<IActionResult> OnPostSubmitAsync([FromBody] LocationShareDto dto)
    {
        if (dto is null) return BadRequest("Empty report.");
        if (!dto.Consent) return BadRequest("Location consent is required.");
        if (!ModelState.IsValid) return BadRequest("Invalid location payload.");
        if (dto.Latitude is < -90 or > 90 || dto.Longitude is < -180 or > 180)
            return BadRequest("Latitude must be -90..90, longitude -180..180.");

        var session = HttpContext.Session?.Id;
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString();
        if (locations.IsRateLimited(session, ip)) return StatusCode(429, "Too many reports. Please wait a minute.");

        try
        {
            var location = await locations.SaveAsync(dto, ip);

            // Nearest known location by name: seeded admin areas (authoritative)
            // + client reverse-geocoded display name (OSM Nominatim) when available.
            var nearestArea = await gis.FindNearestAreaAsync(dto.Latitude, dto.Longitude);
            var clientPlace = dto.NearestPlace?.Trim();
            if (clientPlace?.Length > 500) clientPlace = clientPlace[..500];
            var label = !string.IsNullOrWhiteSpace(clientPlace)
                ? clientPlace
                : nearestArea is not null
                    ? $"{nearestArea.Name} ({nearestArea.AreaType}, ~{nearestArea.DistanceKm:F1} km)"
                    : $"{dto.Latitude:F5}, {dto.Longitude:F5}";

            var defaultType = await db.IncidentTypes
                                  .Where(t => t.IsActive && t.Name == "Other")
                                  .FirstOrDefaultAsync()
                              ?? await db.IncidentTypes.Where(t => t.IsActive).OrderBy(t => t.Id).FirstOrDefaultAsync()
                              ?? throw new InvalidOperationException("No active incident types configured.");

            var submit = new IncidentSubmitDto
            {
                Latitude = dto.Latitude,
                Longitude = dto.Longitude,
                Accuracy = dto.Accuracy,
                Altitude = dto.Altitude,
                Speed = dto.Speed,
                Heading = dto.Heading,
                CapturedAt = dto.CapturedAt,
                SessionId = dto.SessionId,
                IncidentTypeId = defaultType.Id,
                Description = $"Location shared by public user near {label}.",
                Community = clientPlace?.Length > 150 ? clientPlace[..150] : clientPlace ?? nearestArea?.Name,
                Lga = nearestArea?.AreaType == "LGA" ? nearestArea.Name : null
            };

            var incident = await incidents.CreateAsync(submit, location);
            var generated = await alerts.CheckAndGenerateAsync(incident);

            await notify.BroadcastIncidentAsync(new LiveLocationDto
            {
                Id = incident.Id,
                ReferenceNumber = incident.ReferenceNumber,
                Latitude = incident.Latitude,
                Longitude = incident.Longitude,
                RiskLevel = incident.RiskLevel.ToString(),
                RiskScore = incident.RiskScore,
                Status = incident.Status.ToString(),
                IncidentType = incident.IncidentType?.Name ?? "",
                ReportedAt = incident.ReportedAt
            });
            foreach (var a in generated)
            {
                await notify.BroadcastAlertAsync(new AlertDto
                {
                    Id = a.Id, Title = a.Title, Message = a.Message,
                    Latitude = a.Latitude, Longitude = a.Longitude,
                    RadiusKm = a.RadiusKm, RiskLevel = a.RiskLevel.ToString(),
                    IncidentCount = a.IncidentCount, CreatedAt = a.CreatedAt
                });
            }

            logger.LogInformation("Location share {Ref} at {Lat},{Lon} near {Place}.",
                incident.ReferenceNumber, incident.Latitude, incident.Longitude, label);
            return new JsonResult(new
            {
                referenceNumber = incident.ReferenceNumber,
                riskLevel = incident.RiskLevel.ToString(),
                riskScore = incident.RiskScore,
                alerts = generated.Count,
                nearestPlace = label,
                nearestArea = nearestArea?.Name
            });
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
    }
}
