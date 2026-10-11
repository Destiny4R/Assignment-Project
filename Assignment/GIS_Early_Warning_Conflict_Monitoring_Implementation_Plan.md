# Implementation Plan

## 1. Project Objective

Develop a web-based **GIS Early Warning and Real-Time Monitoring System for Farmer/Herder Conflict Resolution** that will:

1.  Automatically obtain a public user's GPS coordinates. 
2.  Send the coordinates to the ASP.NET Core application. 
3.  Store the location and report information in MySQL. 
4.  Display incoming locations on an administrative dashboard. 
5.  Push new locations to the dashboard in real time without page refresh. 
6.  Display locations on an interactive GIS map. 
7.  Allow administrators to view individual incident locations. 
8.  Categorize incidents according to risk level. 
9.  Detect geographical concentrations of incidents. 
10.  Generate early-warning alerts when predefined thresholds are reached. 
11.  Allow authorized officers to manage and resolve reported incidents. 
12.  Maintain historical records for future analysis. 

---

# 2. Proposed Technology Stack

| Layer          | Technology                               |
| -------------- | ---------------------------------------- |
| Framework      | ASP.NET Core                             |
| UI             | Razor Pages                              |
| Backend        | C# / ASP.NET Core                        |
| Database       | MySQL                                    |
| ORM            | Entity Framework Core                    |
| MySQL Provider | Pomelo.EntityFrameworkCore.MySql         |
| Authentication | ASP.NET Core Identity                    |
| Real-time      | ASP.NET Core SignalR                     |
| GIS Map        | Leaflet.js                               |
| Map Tiles      | OpenStreetMap                            |
| Client GPS     | Browser Geolocation API                  |
| Frontend       | HTML5 + Bootstrap 5 + JavaScript/jQuery  |
| Charts         | Chart.js                                 |
| Data tables    | DataTables                               |
| Spatial format | GeoJSON                                  |
| Logging        | Serilog                                  |
| Validation     | DataAnnotations / server-side validation |

---

# 3. High-Level Architecture

The system should follow this architecture:

```
```

```
                    PUBLIC USER
                        │
                        │
                  Open Web Page
                        │
                        ▼
                Browser GPS API
                        │
                        │ Latitude
                        │ Longitude
                        ▼
              ASP.NET CORE RAZOR
                   APPLICATION
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
       MySQL Database           SignalR Hub
            │                       │
            │                       ▼
            │               ADMIN DASHBOARD
            │                       │
            │                       ▼
            │                  LIVE GIS MAP
            │
            ▼
      Historical Records
            │
            ▼
     GIS / Risk Analysis
            │
            ▼
     EARLY WARNING ALERT
```

---

# 4. Recommended Project Structure

Because you are using Razor Pages, I recommend keeping the project organized around modules rather than putting everything into one folder.

```
```

```
FarmerHerderConflictSystem
│
├── Data
│   ├── ApplicationDbContext.cs
│   └── DbInitializer.cs
│
├── Models
│   ├── UserLocation.cs
│   ├── IncidentReport.cs
│   ├── ConflictAlert.cs
│   ├── IncidentEvidence.cs
│   ├── IncidentStatusHistory.cs
│   ├── RiskRule.cs
│   └── AdministrativeArea.cs
│
├── DTOs
│   ├── LocationDto.cs
│   ├── IncidentDto.cs
│   ├── LiveLocationDto.cs
│   └── AlertDto.cs
│
├── Services
│   ├── LocationService.cs
│   ├── IncidentService.cs
│   ├── RiskAssessmentService.cs
│   ├── AlertService.cs
│   ├── GisService.cs
│   └── NotificationService.cs
│
├── Hubs
│   └── MonitoringHub.cs
│
├── Pages
│   │
│   ├── Index.cshtml
│   │
│   ├── Report
│   │   ├── Index.cshtml
│   │   └── Index.cshtml.cs
│   │
│   ├── Dashboard
│   │   ├── Index.cshtml
│   │   └── Index.cshtml.cs
│   │
│   ├── Incidents
│   │   ├── Index.cshtml
│   │   ├── Details.cshtml
│   │   ├── Edit.cshtml
│   │   └── History.cshtml
│   │
│   ├── Map
│   │   ├── Index.cshtml
│   │   └── Index.cshtml.cs
│   │
│   └── Admin
│       ├── Users
│       ├── Alerts
│       ├── RiskRules
│       └── Settings
│
├── wwwroot
│   ├── css
│   ├── js
│   │   ├── gps.js
│   │   ├── live-map.js
│   │   └── monitoring.js
│   └── uploads
│
└── Program.cs
```

---

# 5. Phase 1 — Database Design

Start with the database because almost every module depends on it.

## Main entities

### UserLocation

Stores GPS information.

```
```

```
UserLocation
-------------------------
Id
SessionId
Latitude
Longitude
Accuracy
Altitude
Speed
Heading
CapturedAt
ReceivedAt
IsActive
```

### IncidentReport

Stores the actual conflict report.

```
```

```
IncidentReport
-------------------------
Id
ReferenceNumber
UserLocationId
IncidentTypeId
Description
RiskLevel
Status
ReportedAt
UpdatedAt
ResolvedAt
AssignedOfficerId
```

### IncidentType

```
```

```
IncidentType
-------------------------
Id
Name
Description
IsActive
```

Examples:

-  Suspicious Activity 
-  Farmer/Herder Dispute 
-  Livestock Intrusion 
-  Threat 
-  Crop/Property Destruction 
-  Physical Conflict 
-  Other 

---

### ConflictAlert

```
```

```
ConflictAlert
-------------------------
Id
Title
Message
Latitude
Longitude
Radius
RiskLevel
TriggerType
IncidentCount
CreatedAt
IsAcknowledged
```

---

### IncidentStatusHistory

This allows you to track what happened to an incident.

```
```

```
IncidentStatusHistory
-------------------------
Id
IncidentReportId
OldStatus
NewStatus
Comment
ChangedBy
ChangedAt
```

---

# 6. Phase 2 — Authentication and Authorization

Create two broad categories of users.

### Public users

They do not need an account to submit a basic report.

### Authorized users

Examples:

```
```

```
Super Administrator
Administrator
Monitoring Officer
Response Officer
Viewer
```

Their permissions should control what they can do.

For example:

| Function             | Admin | Monitoring Officer | Response Officer |
| -------------------- | ----- | ------------------ | ---------------- |
| View dashboard       | ✓     | ✓                  | ✓                |
| View map             | ✓     | ✓                  | ✓                |
| View reports         | ✓     | ✓                  | ✓                |
| Change status        | ✓     | ✓                  | ✓                |
| Assign incident      | ✓     | ✓                  | ✓                |
| Manage users         | ✓     | -                  | -                |
| Configure risk rules | ✓     | -                  | -                |
| Delete records       | ✓     | -                  | -                |

---

# 7. Phase 3 — Public GPS Page

Create:

```
```

```
/Report
```

When the page loads:

```
```

```
Page Loaded
     ↓
Request Location Permission
     ↓
navigator.geolocation
     ↓
Get Position
     ↓
Latitude + Longitude
     ↓
Send to ASP.NET Core
```

The browser's Geolocation API provides:

```
```

```
latitude
longitude
accuracy
altitude
speed
heading
```

You should **not continuously track a person's location by default**.

For the project, use explicit user consent and a clearly visible indication that location is being shared.

---

# 8. Phase 4 — Send GPS Coordinates to ASP.NET Core

The public page sends something like:

```
```

```
Latitude: 7.xxxxx
Longitude: 8.xxxxx
Accuracy: 12m
Timestamp: ...
```

to your Razor Page handler.

For example conceptually:

```
```

```
POST /Report?handler=Location
```

The server then:

1.  Validates latitude. 
2.  Validates longitude. 
3.  Validates accuracy. 
4.  Records timestamp. 
5.  Creates a location record. 
6.  Optionally creates an incident. 
7.  Sends a SignalR notification. 

---

# 9. Phase 5 — Real-Time Communication

This is a critical part of your project.

Create:

```
```

```
Hubs/MonitoringHub.cs
```

The flow becomes:

```
```

```
PUBLIC PAGE
     │
     │ Submit Location
     ▼
ASP.NET CORE
     │
     ├── Save to MySQL
     │
     └── SignalR
          │
          ▼
     ADMIN DASHBOARD
          │
          ▼
      LIVE MAP
```

Therefore, when a public user submits:

```
```

```
Latitude: 7.7322
Longitude: 8.5391
```

the administrator's dashboard receives it immediately.

No manual refresh is required.

---

# 10. Phase 6 — Administrative Dashboard

Create:

```
```

```
/Dashboard
```

The dashboard should contain:

### Summary cards

```
```

```
Total Reports
Active Incidents
Today's Reports
Critical Alerts
Unresolved Incidents
```

### Incoming reports table

```
```

```
Reference | Type | Risk | Location | Time | Status | Action
```

### Live map

The map occupies a significant portion of the dashboard.

---

# 11. Phase 7 — GIS Map

Use **Leaflet.js**.

The map should initially show the relevant operating area.

When a new location arrives through SignalR:

```
```

```
SignalR Event
     ↓
Receive latitude/longitude
     ↓
Create Leaflet Marker
     ↓
Add marker to map
```

Example:

```
```

```
             LIVE GIS MAP

        🟢
             🟡

                   🔴
               
       🟢

                   🟠
```

Clicking a marker displays:

```
```

```
Incident: INC-00025
Risk: High
Reported: 17:34
Accuracy: 8m
Status: Active

[View Incident]
```

---

# 12. Phase 8 — "View Location"

This directly addresses your original requirement.

The incident table contains:

```
```

```
[View Location]
```

When clicked:

```
```

```
Incident
   ↓
Retrieve Latitude/Longitude
   ↓
Open GIS Map
   ↓
Center map
   ↓
Zoom to location
   ↓
Display marker
```

You can also show a popup:

```
```

```
┌───────────────────────────────┐
│ INCIDENT INC-00025             │
│                               │
│ Risk: HIGH                    │
│ Status: Active                │
│ Reported: 17:34               │
│                               │
│ [Open Incident]               │
└───────────────────────────────┘
```

---

# 13. Phase 9 — Incident Classification

Create predefined categories.

```
```

```
Incident Type
│
├── Suspicious Activity
├── Farmer/Herder Dispute
├── Livestock Intrusion
├── Threat
├── Property/Crop Destruction
├── Physical Confrontation
└── Other
```

Then introduce:

```
```

```
Risk Level
│
├── Low
├── Medium
├── High
└── Critical
```

---

# 14. Phase 10 — Early-Warning Engine

This is the most important difference between a **GIS monitoring system** and an **early-warning system**.

Create a `RiskAssessmentService`.

It evaluates:

```
```

```
Incident frequency
       +
Geographical proximity
       +
Incident severity
       +
Time period
       +
Historical incidents
       ↓
   Risk Score
       ↓
Risk Classification
```

For example:

```
```

```
0 – 24     LOW
25 – 49    MEDIUM
50 – 74    HIGH
75 – 100   CRITICAL
```

The actual scoring values should be configurable rather than hard-coded.

---

# 15. Phase 11 — Geographic Hotspot Detection

Suppose the system receives:

```
```

```
Report 1 → Location A
Report 2 → 1 km away
Report 3 → 2 km away
Report 4 → 1.5 km away
Report 5 → 2.3 km away
```

within a short period.

The system can determine:

```
```

```
Several incidents
       ↓
Same geographical area
       ↓
High incident concentration
       ↓
Potential conflict hotspot
       ↓
Generate warning
```

The dashboard could display:

> 🔴 **HIGH-RISK HOTSPOT DETECTED**
>
> Multiple incidents have been reported within the defined monitoring radius.

---

# 16. Phase 12 — Alert Management

Alerts should be visible on the dashboard.

```
```

```
┌───────────────────────────────────────┐
│ 🔴 CRITICAL ALERT                    │
│                                       │
│ Multiple high-risk incidents detected│
│ within the configured monitoring area│
│                                       │
│ [View on Map] [Acknowledge]           │
└───────────────────────────────────────┘
```

Alert statuses:

```
```

```
New
 ↓
Acknowledged
 ↓
Investigating
 ↓
Action Taken
 ↓
Resolved
```

---

# 17. Phase 13 — Incident Resolution

The system should not stop after generating an alert.

An authorized officer can open an incident:

```
```

```
INC-00025

Incident Type:
Farmer/Herder Dispute

Location:
[GIS MAP]

Risk:
HIGH

Status:
ACTIVE

Reported:
08/10/2026 17:34

Description:
...

Assigned Officer:
Officer A

Actions:
[Assign]
[Change Status]
[Add Comment]
[Resolve]
```

This creates the **conflict resolution** component of the project.

---

# 18. Phase 14 — Historical GIS Analysis

The system should retain historical incidents.

Administrators can select:

```
```

```
From: 01/01/2026
To:   31/12/2026

LGA:
[Select]

Incident:
[All]

Risk:
[All]
```

Then display:

```
```

```
Historical Incidents
        ↓
GIS Map
        ↓
Clusters / Hotspots
        ↓
Charts
```

Useful analytics:

-  Number of incidents per LGA 
-  Number of incidents per month 
-  Incident types 
-  Risk distribution 
-  Response time 
-  Resolved vs unresolved 
-  Conflict hotspots 
-  Incident frequency 

---

# 19. Phase 15 — Dashboard Map Layers

Eventually your map can contain multiple layers:

```
```

```
GIS MAP
│
├── Incoming Reports
├── Active Incidents
├── Historical Incidents
├── Conflict Hotspots
├── Administrative Boundaries
├── Communities
└── Risk Zones
```

This is where the project becomes a proper GIS application rather than simply a map showing GPS points.

---

# 20. Phase 16 — Security and Privacy

This should be treated as a major requirement.

Because the system handles people's locations:

### Public users

-  Do not expose other users' locations. 
-  Do not expose the dashboard. 
-  Validate all submitted coordinates. 
-  Rate-limit submissions. 
-  Avoid collecting unnecessary personal information. 
-  Clearly inform users when their location is being shared. 

### Administrators

-  Require authentication. 
-  Use authorization policies/roles. 
-  Audit important actions. 
-  Protect uploaded evidence. 
-  Validate uploaded files. 
-  Protect SignalR access. 

### Database

Never trust coordinates sent from the browser.

For example:

```
```

```
Latitude must be:
-90 to +90

Longitude must be:
-180 to +180
```

---

# 21. Phase 17 — Audit Logging

Record important administrative activities.

```
```

```
AuditLog
--------------------
Id
UserId
Action
Entity
EntityId
IPAddress
Timestamp
Description
```

Examples:

```
```

```
Officer assigned incident
Admin changed risk level
Officer acknowledged alert
Incident marked resolved
Administrator changed risk configuration
```

---

# 22. Phase 18 — Testing

Testing should be done in stages.

### GPS testing

Test:

-  GPS permission granted 
-  Permission denied 
-  GPS unavailable 
-  Low accuracy 
-  Invalid coordinates 
-  Mobile browser 
-  Desktop browser 

### Real-time testing

Open:

```
```

```
Browser 1 → Public Page
Browser 2 → Admin Dashboard
```

Submit a location from Browser 1.

Browser 2 should immediately show:

```
```

```
New incident received
       ↓
New table record
       ↓
New map marker
       ↓
Dashboard notification
```

### GIS testing

Test:

-  Marker placement 
-  Zoom 
-  Popup 
-  View location 
-  Multiple markers 
-  Historical locations 
-  Hotspots 

---

# 23. Implementation Order

I recommend implementing the project in this exact order:

```
```

```
PHASE 1
Project setup
       ↓
PHASE 2
MySQL + EF Core
       ↓
PHASE 3
Database models
       ↓
PHASE 4
Authentication/Authorization
       ↓
PHASE 5
Public GPS page
       ↓
PHASE 6
Save GPS coordinates
       ↓
PHASE 7
SignalR
       ↓
PHASE 8
Admin dashboard
       ↓
PHASE 9
Leaflet GIS map
       ↓
PHASE 10
Real-time map markers
       ↓
PHASE 11
Incident reporting
       ↓
PHASE 12
Risk assessment
       ↓
PHASE 13
Early-warning engine
       ↓
PHASE 14
Hotspot detection
       ↓
PHASE 15
Incident management
       ↓
PHASE 16
Conflict resolution
       ↓
PHASE 17
Historical GIS analytics
       ↓
PHASE 18
Notifications
       ↓
PHASE 19
Security/audit
       ↓
PHASE 20
Testing + deployment
```

---

# 24. Minimum Viable Version

To avoid making the project unnecessarily large, I would make the **first working version** only these components:

### Public

```
```

```
/Report
```

-  Request GPS permission 
-  Get coordinates 
-  Select incident type 
-  Enter description 
-  Submit 

### Dashboard

```
```

```
/Dashboard
```

-  Total reports 
-  Incoming reports 
-  Live SignalR updates 
-  Interactive map 
-  View location 
-  Incident details 

### Early Warning

-  Risk classification 
-  Incident clustering 
-  Basic hotspot detection 
-  Alert generation 

### Resolution

-  Assign officer 
-  Change status 
-  Add resolution notes 
-  Close incident 

Then add advanced GIS analytics after the core system is working.

---

# 25. Final System Flow

The completed system should ultimately operate like this:

```
```

```
                  PUBLIC USER
                       │
                       ▼
              Opens Reporting Page
                       │
                       ▼
               GPS Permission
                       │
                       ▼
              Obtain Coordinates
                       │
                       ▼
              Submit Incident
                       │
                       ▼
              ASP.NET CORE API
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
         MySQL DB            SignalR
             │                   │
             │                   ▼
             │             ADMIN DASHBOARD
             │                   │
             │                   ▼
             │                LIVE MAP
             │                   │
             ▼                   ▼
      Historical Data      Real-Time Marker
             │
             ▼
       GIS/Risk Analysis
             │
             ▼
       HOTSPOT DETECTION
             │
             ▼
       EARLY WARNING ALERT
             │
             ▼
       OFFICER RESPONSE
             │
             ▼
       INCIDENT RESOLUTION
             │
             ▼
       HISTORICAL RECORD
```

### Recommended project title

I would slightly refine your title to:

> **Design and Development of a GIS-Based Early Warning and Real-Time Framework for Farmer-Herder Conflict Monitoring and Resolution**

This title better reflects what you are actually implementing: **GPS collection, GIS visualization, real-time monitoring, early-warning analysis, and conflict resolution**, using **ASP.NET Core Razor Pages and MySQL**.
