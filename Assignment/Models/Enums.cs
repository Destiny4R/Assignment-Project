namespace Assignment.Models;

public enum RiskLevel
{
    Low = 0,
    Medium = 1,
    High = 2,
    Critical = 3
}

public enum IncidentStatus
{
    New = 0,
    Acknowledged = 1,
    Investigating = 2,
    ActionTaken = 3,
    Resolved = 4
}

public static class Roles
{
    public const string SuperAdmin = "SuperAdmin";
    public const string Admin = "Administrator";
    public const string MonitoringOfficer = "MonitoringOfficer";
    public const string ResponseOfficer = "ResponseOfficer";
    public const string Viewer = "Viewer";

    public static readonly string[] All = [SuperAdmin, Admin, MonitoringOfficer, ResponseOfficer, Viewer];
}
