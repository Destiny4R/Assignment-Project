using System.ComponentModel.DataAnnotations;

namespace Assignment.Models;

public class AuditLog
{
    public int Id { get; set; }

    [MaxLength(450)]
    public string? UserId { get; set; }

    [Required, MaxLength(150)]
    public string Action { get; set; } = string.Empty;

    [MaxLength(100)]
    public string? Entity { get; set; }

    [MaxLength(100)]
    public string? EntityId { get; set; }

    [MaxLength(45)]
    public string? IPAddress { get; set; }

    public DateTime Timestamp { get; set; } = DateTime.UtcNow;

    [MaxLength(2000)]
    public string? Description { get; set; }
}
