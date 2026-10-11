using Assignment.Data;
using Assignment.DTOs;
using Assignment.Models;
using Microsoft.EntityFrameworkCore;

namespace Assignment.Services;

public interface ILocationService
{
    Task<UserLocation> SaveAsync(LocationDto dto, string? ip, CancellationToken ct = default);
    bool IsRateLimited(string? sessionId, string? ip);
}

public class LocationService(ApplicationDbContext db) : ILocationService
{
    // Very light in-memory rate limit: max 10 submissions / minute per session-or-IP.
    private static readonly Dictionary<string, List<DateTime>> _hits = new();
    private static readonly object _lock = new();

    public bool IsRateLimited(string? sessionId, string? ip)
    {
        var key = sessionId ?? ip ?? "anon";
        lock (_lock)
        {
            var now = DateTime.UtcNow;
            if (!_hits.TryGetValue(key, out var list))
            {
                list = [];
                _hits[key] = list;
            }
            list.RemoveAll(t => t < now.AddMinutes(-1));
            if (list.Count >= 10) return true;
            list.Add(now);
            return false;
        }
    }

    public async Task<UserLocation> SaveAsync(LocationDto dto, string? ip, CancellationToken ct = default)
    {
        Validate(dto);
        var loc = new UserLocation
        {
            SessionId = dto.SessionId,
            Latitude = dto.Latitude,
            Longitude = dto.Longitude,
            Accuracy = dto.Accuracy,
            Altitude = dto.Altitude,
            Speed = dto.Speed,
            Heading = dto.Heading,
            CapturedAt = dto.CapturedAt ?? DateTime.UtcNow,
            ReceivedAt = DateTime.UtcNow,
            IpAddress = ip,
            IsActive = true
        };
        db.UserLocations.Add(loc);
        await db.SaveChangesAsync(ct);
        return loc;
    }

    private static void Validate(LocationDto dto)
    {
        // Never trust browser coordinates (Plan §20).
        if (dto.Latitude is < -90 or > 90) throw new ArgumentException("Latitude must be -90 to +90.");
        if (dto.Longitude is < -180 or > 180) throw new ArgumentException("Longitude must be -180 to +180.");
        if (dto.Accuracy is < 0 or > 100000) throw new ArgumentException("Invalid accuracy value.");
    }
}
