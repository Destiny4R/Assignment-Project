"""Generate .docx project report for Assignment (GIS Early Warning & Conflict Monitoring)."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

OUT = r"C:\Users\BDIC-004\Documents\Visual Studio 2026\Projects\AssignmentProject\GIS_Early_Warning_Conflict_Monitoring_Report.docx"

doc = Document()

# -- base styles
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

for i in range(1, 4):
    hs = doc.styles[f'Heading {i}']
    hs.font.name = 'Calibri'
    hs.font.color.rgb = RGBColor(0x1F, 0x3B, 0x63)
    if i == 1:
        hs.font.size = Pt(16)
    elif i == 2:
        hs.font.size = Pt(13)
    else:
        hs.font.size = Pt(11.5)

# narrow margins for more content per page
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

# footer with page number field
footer = doc.sections[0].footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run()
fld1 = OxmlElement('w:fldSimple')
fld1.set(qn('w:instr'), 'PAGE')
r = OxmlElement('w:r')
r2 = OxmlElement('w:t')
r2.text = '1'
r.append(r2)
fld1.append(r)
run._r.append(fld1)
fp.add_run('  |  GIS Early Warning & Conflict Monitoring — Project Report').font.size = Pt(8)
for r_ in fp.runs:
    r_.font.size = Pt(8)
    r_.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

def add_para(text, bold=False, italic=False, size=None, align=None, space_after=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if size: r.font.size = size
    if align: p.alignment = align
    if space_after is not None: p.paragraph_format.space_after = Pt(space_after)
    return p

def add_mixed(segments, align=None):
    """segments: list of (text, dict{bold,italic,size,code})"""
    p = doc.add_paragraph()
    if align: p.alignment = align
    for text, fmt in segments:
        r = p.add_run(text)
        if fmt.get('bold'): r.bold = True
        if fmt.get('italic'): r.italic = True
        if fmt.get('size'): r.font.size = Pt(fmt['size'])
        if fmt.get('code'):
            r.font.name = 'Consolas'
            r.font.size = Pt(9.5)
    return p

def add_bullet(text, bold_prefix=None, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.3 + level*0.25)
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
        p.add_run(text)
    else:
        p.add_run(text)
    return p

def add_code(code_text, title=None):
    if title:
        t = doc.add_paragraph()
        r = t.add_run(title)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x1F, 0x3B, 0x63)
        t.paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    pf = p.paragraph_format
    # shading
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), 'F2F2F2')
    pPr.append(shd)
    r = p.add_run(code_text)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.5)
    return p

def add_table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ''
        r = hdr[i].paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        shading = OxmlElement('w:shd')
        shading.set(qn('w:val'), 'clear')
        shading.set(qn('w:fill'), 'D9E2F3')
        hdr[i]._tc.get_or_add_tcPr().append(shading)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ''
            r = cells[i].paragraphs[0].add_run(str(val))
            r.font.size = Pt(9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def heading1(t): return doc.add_heading(t, level=1)
def heading2(t): return doc.add_heading(t, level=2)
def heading3(t): return doc.add_heading(t, level=3)

# ================= COVER =================
for _ in range(3):
    doc.add_paragraph()
add_para('GIS-Based Early Warning and Real-Time Conflict Monitoring System', bold=True, size=24, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
add_para('For Farmer–Herder Conflict (Benue State Focus)', size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
add_para('Project Development Report', bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
add_para('ASP.NET Core 8 · Razor Pages · Entity Framework Core 8 · MySQL (Pomelo) · ASP.NET Core Identity · SignalR · Leaflet.js / OpenStreetMap', size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
add_table(['Item', 'Detail'], [
    ['Solution', 'AssignmentProject.slnx → Assignment/Assignment.csproj (net8.0)'],
    ['Database', 'FarmerHerderConflictDb on MySQL localhost:3306 (Pomelo.EntityFrameworkCore.MySql 8.0.2)'],
    ['Seed admin', 'admin@test.com / Admin123! (SuperAdmin + Administrator)'],
    ['Run profiles', 'http://localhost:5278 · https://localhost:7006 · IIS Express http://localhost:32583'],
    ['Publish', 'FolderProfile → C:\\Users\\BDIC-004\\Desktop\\MyAssignment (Release, Any CPU)'],
    ['Date / Log evidence', '08 Oct 2026 — Logs/app-20261008.log (3,027 lines); migration 20261008171902_InitialCreate'],
])
add_para('This report was written from a careful study of the as-built codebase: Program.cs, appsettings.json, all Models/Data/DTOs/Services/Hubs, all Razor Pages and wwwroot/js, the EF Core migration, Serilog log, launch/publish profiles, and GIS_Early_Warning_Conflict_Monitoring_Implementation_Plan.md.', italic=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para(f'Report generated {datetime.date.today().isoformat()} from the working tree at C:\\Users\\BDIC-004\\Documents\\Visual Studio 2026\\Projects\\AssignmentProject.', size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ================= CONTENTS =================
heading1('Contents')
toc_items = [
    ('Abstract', '2'),
    ('1  Introduction', '2'),
    ('2  Requirements and Threat Model', '3'),
    ('3  System Design', '4'),
    ('4  Implementation', '6'),
    ('5  Testing and Evaluation', '9'),
    ('6  Deployment and Operating Policy', '10'),
    ('7  Security Considerations', '11'),
    ('8  Limitations and Future Work', '12'),
    ('9  Conclusion', '12'),
    ('References', '13'),
    ('Appendix A: Command Reference', '13'),
    ('Appendix B: Source Code Layout', '14'),
]
for title, pg in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(title)
    r.font.size = Pt(11)
    p.add_run(f'  .....  {pg}').font.size = Pt(11)
add_para('List of Tables: (1) Technology stack · (2) Roles & permissions · (3) Entities · (4) Seeded IncidentTypes · (5) Risk scoring illustration · (6) Functional test matrix · (7) Command reference.  List of key code excerpts: risk scoring, Haversine/bounding-box, alert de-duplication, reference-number generation, SignalR broadcast.', italic=True, size=9.5)

# ================= ABSTRACT =================
heading1('Abstract')
doc.add_paragraph(
    'This report documents the design, implementation, testing, deployment and secure operation of a GIS-based early warning and real-time conflict monitoring system for farmer–herder conflicts, built as an ASP.NET Core 8 Razor Pages web application backed by MySQL. '
    'The system provides three linked capabilities: (i) anonymous public incident/GPS-share reporting with browser geolocation and OpenStreetMap reverse-geocoding; (ii) an officer-only live monitoring loop (dashboard statistics, Leaflet live map, incident triage, GIS operations map with GeoJSON and hotspot detection); and (iii) a configurable early-warning engine that scores every incident (60% type severity + 40% spatio-temporal frequency) and raises de-duplicated ConflictAlerts when density or severity thresholds defined in RiskRules are crossed. Real-time push is delivered over an authorised SignalR hub (MonitoringHub, group “dashboard”), persistence over Entity Framework Core 8 (Pomelo MySQL provider), authentication over ASP.NET Core Identity with five roles, and observability over Serilog (console + rolling daily file) plus a persistent AuditLog and per-incident status history. '
    'The as-built data model centres on UserLocation → IncidentReport (with IncidentType, RiskScore/RiskLevel, denormalised lat/lon, officer assignment and resolution), ConflictAlert, RiskRule, AdministrativeArea (State/LGA hierarchy with optional GeoJSON), IncidentEvidence, IncidentStatusHistory and AuditLog on top of Identity tables. '
    'Evidence examined includes the Release folder-publish artefact, the 665-line InitialCreate migration, seed data (7 incident types, default 3-in-5 km-in-24 h rule, Benue/Makurdi/Guma/Logo areas), and a 3,027-line startup/migration log. No automated test project, Dockerfile or CI pipeline was found; verification to date is manual plus migration/log evidence. '
    'The report closes with deployment/operating procedures, a STRIDE-informed threat model and hardening guidance, and explicit limitations and future work (spatial indexes, PostGIS/NetTopologySuite, offline/SMS ingestion, evidence upload wiring, analytics).'
)

# ================= 1 INTRODUCTION =================
heading1('1  Introduction')
heading2('1.1  Background and problem')
doc.add_paragraph(
    'Farmer–herder competition over land, water and grazing routes in Nigeria — particularly in Benue State (Makurdi, Guma, Logo, the seeded default areas) — can escalate rapidly from disputes and livestock intrusion to crop destruction, threats and physical violence. Response is often delayed because reports arrive by word of mouth, locations are imprecise, and there is no shared live picture or automatic escalation when incidents cluster in space and time. The project therefore set out to build a low-friction reporting channel combined with a GIS operations picture and an automatic hotspot/severity detector.'
)
heading2('1.2  Objectives')
for b in [
    ('Public reporting without barriers: ', 'a mobile-friendly /Report page that captures consented GPS fixes, reverse-geocoded place names and incident details with no login, validated and rate-limited server-side.'),
    ('Live common operating picture: ', 'an officer dashboard (statistics, alert banner, live table, Leaflet map), an incidents worklist with DataTables filtering, and a GIS operations map served as GeoJSON with hotspot overlays — all updated in real time over SignalR.'),
    ('Configurable early warning: ', 'a RiskAssessmentService + AlertService pair driven by administrator-editable RiskRules (minimum count, radius, time window, High/Critical thresholds) rather than hard-coded constants.'),
    ('Accountability and audit: ', 'role-based access, per-incident status workflow with history, and a global audit log, all on a relational MySQL store with seeded taxonomy and geography.'),
]:
    add_bullet(b[1], bold_prefix=b[0])
heading2('1.3  Scope and stakeholders')
add_table(['Stakeholder / role', 'Needs / uses'],
    [
        ['Affected community member (anonymous)', 'Share location + report incident quickly on a phone; see confirmation reference (e.g. INC-00025), risk level and nearest area.'],
        ['MonitoringOfficer / ResponseOfficer', 'Watch dashboard + live map, triage incidents, assign officers, advance status, acknowledge alerts.'],
        ['Administrator / SuperAdmin', 'All officer powers plus user-role management and risk-threshold tuning (Admin/RiskRules, Admin/Users).'],
        ['Viewer', 'Read-only situational awareness (authorised pages, no management actions).'],
    ])
doc.add_paragraph('Out of scope in the as-built increment (see §8): predictive modelling, SMS/USSD ingestion, native mobile apps, and automated dispatch — the system stops at detection, visualisation and audited human workflow.')
heading2('1.4  Report structure and method')
doc.add_paragraph('The remainder of this report follows the requested contents: requirements and threat model (§2), system design (§3), implementation as-built (§4), testing and evaluation (§5), deployment and operating policy (§6), security considerations (§7), limitations and future work (§8), conclusion (§9), references, and appendices (commands, source layout). Every factual claim about the code cites its file and, where useful, line-anchored excerpts reproduced from the working tree. The normative design source GIS_Early_Warning_Conflict_Monitoring_Implementation_Plan.md is referenced as “Plan §n” where it constrains or matches the build.')

# ================= 2 REQUIREMENTS =================
heading1('2  Requirements and Threat Model')
heading2('2.1  Functional requirements (as-built)')
add_table(['ID', 'Requirement', 'Where realised'],
[
    ['FR-1', 'Anonymous consented GPS share + incident report with server validation', 'Pages/Report/Index (.cshtml/.cs), wwwroot/js/gps.js, DTOs/LocationShareDto, Services/LocationService'],
    ['FR-2', 'Incident taxonomy with severity weights', 'Models/IncidentType + ApplicationDbContext seed (7 types); IncidentService.CreateAsync validates type'],
    ['FR-3', 'Automatic risk score (0–100) + level (Low/Medium/High/Critical)', 'Services/RiskAssessmentService.EvaluateAsync; stored on IncidentReport.RiskScore/RiskLevel'],
    ['FR-4', 'Automatic hotspot/severity alerts with de-duplication', 'Services/AlertService.CheckAndGenerateAsync; Models/ConflictAlert'],
    ['FR-5', 'Live dashboard: stats, alerts, incoming reports, live map', 'Pages/Dashboard/Index + wwwroot/js/live-map.js + monitoring.js + SignalR'],
    ['FR-6', 'Incident worklist: search/filter (text, status, risk, type)', 'Pages/Incidents/Index (Take 200, DataTables 1.13.8)'],
    ['FR-7', 'Incident detail: map, assignment, status workflow + history', 'Pages/Incidents/Details (+Assign/Status handlers; IncidentStatusHistory)'],
    ['FR-8', 'GIS operations map with filters + GeoJSON + hotspots + focus links', 'Pages/Map/Index (handler GeoJson; GisService.ToGeoJson/DetectHotspotsAsync)'],
    ['FR-9', 'Alert acknowledgement workflow', 'Pages/Admin/Alerts/Index (handler Ack → AlertService.AcknowledgeAsync)'],
    ['FR-10', 'Configurable risk rules (no hard-coded scoring)', 'Pages/Admin/RiskRules/Index+Edit; Models/RiskRule'],
    ['FR-11', 'User administration (single-role assignment)', 'Pages/Admin/Users/Index (handler Role)'],
    ['FR-12', 'Auditability (global log + per-incident trail)', 'Models/AuditLog (AuditService) + IncidentStatusHistory on Details page'],
])
heading2('2.2  Non-functional requirements')
for b in [
    ('Usability: ', 'Bootstrap 5 layout, one-tap GPS share with consent gate and retry, Leaflet tiles from OpenStreetMap, toasts for live events.'),
    ('Performance: ', 'bounding-box pre-filter before Haversine; capped queries (Dashboard 30 recent / 10 alerts; Incidents 200; GeoJSON 500 incidents / 20 alerts); distributed memory cache + 2 h session.'),
    ('Reliability: ', 'auto-migrate + seed on startup (Program.cs); Serilog console + daily rolling file Logs/app-.log; global exception handler + HSTS in non-development.'),
    ('Portability: ', 'net8.0, Pomelo MySQL 8.0.2 with ServerVersion.AutoDetect and 8.0.36 fallback; folder publish (Release/Any CPU).'),
    ('Maintainability: ', 'scoped services behind interfaces (IGisService, IRiskAssessmentService, ILocationService, IIncidentService, IAlertService, IAuditService, INotificationService); DataAnnotations validation; nullable + implicit usings enabled.'),
]:
    add_bullet(b[1], bold_prefix=b[0])
heading2('2.3  Actors, trust boundaries and assumptions')
doc.add_paragraph('Trust boundaries: (B1) browser ↔ server (untrusted GPS clocks/coordinates, untrusted input — hence server-side validation, rate limiting and consent flag); (B2) public zone (/Report, /Account/Login) ↔ authorised zone (/Dashboard, /Incidents, /Map, /Admin, MonitoringHub) enforced by AuthorizeFolder conventions + [Authorize]/role attributes; (B3) application ↔ MySQL (credentials in configuration) and ↔ third-party tile/geocode services (OSM tile CDN, Nominatim reverse-geocode). Assumptions: officers’ devices and the hosting network are notionally trusted but credentials can leak (hence least-privilege roles); GPS accuracy is advisory; browser clocks may skew (server stamps ReceivedAt independently).')
add_table(['Role (Models/Enums.cs)', 'Powers (Plan §6, enforced in _Layout + page attributes)'],
[
    ['SuperAdmin', 'Full control incl. user/role management and risk-rule editing.'],
    ['Administrator', 'Full control incl. user/role management and risk-rule editing.'],
    ['MonitoringOfficer', 'View dashboard/map/incidents/alerts; acknowledge alerts; update status (no user/rule admin).'],
    ['ResponseOfficer', 'As MonitoringOfficer (field response focus).'],
    ['Viewer', 'Read-only authorised views.'],
])
heading2('2.4  Threat model (STRIDE, informal)')
add_table(['Threat', 'Example against this system', 'Mitigation as-built / residual (→ §7)'],
[
    ['Spoofing', 'Fake GPS/incident flood; credential theft; session hijack', 'Identity + cookie auth; authorised hub; rate limit 10/min/location; audit; RESIDUAL: 6-char passwords, no lockout/2FA, empty default DB password'],
    ['Tampering', 'Altered coordinates, handler parameters, GeoJSON filters', 'Range validation (-90..90/-180..180), antiforgery tokens on forms + RequestVerificationToken header on fetch; RESIDUAL: authorisation is coarse (any officer can ack)'],
    ['Repudiation', '“I didn’t change that status”', 'AuditLog (user, action, entity, IP, timestamp) + IncidentStatusHistory (old→new, who, when, comment)'],
    ['Information disclosure', 'Incident/reporter PII on live map; connection string in appsettings', 'AuthoriseFolder + hub [Authorize]; RESIDUAL: reporter names/contacts broadcast in DTOs — minimise; move secrets to user-secrets/vault'],
    ['Denial of service', 'Report-flood; heavy GeoJSON scans', 'Per-session/IP rate limit + query caps + bounding-box prefilter; RESIDUAL: in-memory limiter is single-node; add distributed throttling + CDN caching'],
    ['Elevation of privilege', 'Viewer→Admin; CSRF role change', 'Role attributes on RiskRules/Users pages; nav hidden by role; antiforgery; single-role replace; RESIDUAL: add fine-grained policies + tests'],
])
doc.add_paragraph('Abuse cases explicitly handled: consent must be true (LocationShareDto); unconsented or out-of-range fixes throw; duplicate alerts within the same rule window/radius are suppressed; critical-severity incidents can alert even below the density threshold so a single grave event is never silently clustered away.')

# ================= 3 SYSTEM DESIGN =================
heading1('3  System Design')
heading2('3.1  Architectural overview')
doc.add_paragraph(
    'Three-tier Razor Pages monolith (Plan §§9, 12): Browser (HTML5 + Bootstrap 5 + jQuery/DataTables, Leaflet 1.9.4, SignalR JS 8.0.0, Geolocation API) → ASP.NET Core 8 server (Razor Pages handlers, scoped domain services, SignalR MonitoringHub, Identity, EF Core 8, Serilog) → MySQL 8 (FarmerHerderConflictDb via Pomelo). Third-party runtime dependencies are OpenStreetMap tiles and Nominatim reverse-geocoding (client-side fetch). No separate Web API project: data operations are page handlers (POST /Report?handler=Submit, GET /Map?handler=GeoJson, POST handlers for Assign/Status/Ack/Role) plus the hub at /monitoringHub (Program.cs:94–95 maps only MapRazorPages + MapHub).'
)
add_code('Browser (/Report, /Dashboard, /Map)\n  │  fetch POST ?handler=Submit / GET ?handler=GeoJson / SignalR\n  ▼\nASP.NET Core 8 (Razor Pages + Services + MonitoringHub + Identity)\n  │  EF Core 8 + Pomelo MySQL          │  SignalR group "dashboard"\n  ▼                                     ▼\nMySQL: FarmerHerderConflictDb     Officer browsers (live tables/maps/toasts)\n  ▲\n  OSM tiles + Nominatim (client-side)', title='Figure 3-1 — Deployment/logical data flow (textual).')
heading2('3.2  Data design (ER summary)')
doc.add_paragraph('ApplicationDbContext : IdentityDbContext<ApplicationUser> exposes 9 domain DbSets plus Identity sets. The incident core is UserLocation 1—* IncidentReport (FK UserLocationId, Restrict) with IncidentType *—1 IncidentReport (FK IncidentTypeId, Restrict); IncidentReport 1—* IncidentStatusHistory / IncidentEvidence (Cascade); optional assignment IncidentReport.AssignedOfficerId → ApplicationUser; ConflictAlert, RiskRule, AdministrativeArea (self-parent), AuditLog and UserLocation stand alone except the incident link. Key constraints: unique index IncidentReport.ReferenceNumber (INC-00005 format), composite {Latitude,Longitude} + single-column ReportedAt/Status indexes, UserLocation.ReceivedAt, ConflictAlert.(CreatedAt, IsAcknowledged). Coordinates are doubles with a denormalised lat/lon copy on IncidentReport for fast GIS scans without a join.')
add_table(['Entity (file)', 'Key attributes', 'Notes'],
[
    ['ApplicationUser (Models/ApplicationUser.cs)', 'IdentityUser + FullName(150), IsActive=true, CreatedAt', 'Seed: admin@test.com / Admin123!, EmailConfirmed, SuperAdmin+Administrator'],
    ['UserLocation (Models/UserLocation.cs)', 'SessionId(64), Lat/Lon, Accuracy/Alt/Speed/Heading, CapturedAt (browser), ReceivedAt (server), IsActive, IpAddress(45)', 'Raw GPS fix; rate-limit key is sessionId ?? IP'],
    ['IncidentType (Models/IncidentType.cs)', 'Name, Description, DefaultRiskLevel, SeverityWeight 0–100, IsActive', 'Seed 7 rows — see Table 4'],
    ['IncidentReport (Models/IncidentReport.cs)', 'ReferenceNumber UQ, UserLocationId, IncidentTypeId, Description 2000, RiskLevel/Score, Status, ReportedAt/UpdatedAt/ResolvedAt, Lat/Lon, Reporter*, Community/Lga, AssignedOfficerId, ResolutionNotes', 'Status enum New→Acknowledged→Investigating→ActionTaken→Resolved'],
    ['ConflictAlert (Models/ConflictAlert.cs)', 'Title/Message, Lat/Lon, RadiusKm=5, RiskLevel, TriggerType Frequency|Proximity|Severity|Manual, IncidentCount, CreatedAt, IsAcknowledged/AckBy/At, Status string', 'Latest-10 active list; dedupe window = rule TimeWindowHours'],
    ['RiskRule (Models/RiskRule.cs)', 'Name, Description, MinIncidentCount=3, RadiusKm=5, TimeWindowHours=24, High≥50, Critical≥75, IsActive', 'Seed “Default hotspot rule”; scoring never hard-coded (UI note)'],
    ['AdministrativeArea (Models/AdministrativeArea.cs)', 'Name, AreaType State|LGA|Community, ParentId self-FK, Lat/Lon, BoundaryGeoJson, IsActive', 'Seed Benue State + Makurdi/Guma/Logo; default centre 7.7322, 8.5391'],
    ['IncidentEvidence (Models/IncidentEvidence.cs)', 'IncidentId (Cascade), FilePath, FileType, UploadedAt/By', 'Modelled; no upload UI wired as-built'],
    ['IncidentStatusHistory (Models/IncidentStatusHistory.cs)', 'IncidentId (Cascade), Old/New status, Comment, ChangedBy Id/Name, ChangedAt', 'Rendered on Details page'],
    ['AuditLog (Models/AuditLog.cs)', 'UserId, Action, Entity, EntityId, IPAddress, Timestamp, Description', 'Written by AuditService on status/assign/ack/rule changes'],
])
add_table(['#', 'IncidentType (seed)', 'Default level', 'Weight'],
[
    ['1', 'Suspicious Activity', 'Low', '20'],
    ['2', 'Farmer/Herder Dispute', 'Medium', '40'],
    ['3', 'Livestock Intrusion', 'Medium', '35'],
    ['4', 'Threat', 'High', '60'],
    ['5', 'Crop/Property Destruction', 'High', '65'],
    ['6', 'Physical Conflict', 'Critical', '90'],
    ['7', 'Other', 'Low', '15'],
])
heading2('3.3  Request / realtime flows')
for b in [
    ('Public report (Plan §9 flow): ', 'gps.js requires consent → getCurrentPosition (high accuracy, 15 s timeout) → optional Nominatim reverse-geocode → POST /Report?handler=Submit (JSON + antiforgery header) → LocationService.SaveAsync → nearest-area lookup (FindNearestAreaAsync + client NearestPlace) → IncidentService.CreateAsync (default “Other” type for pure GPS shares) → RiskAssessmentService.EvaluateAsync → AlertService.CheckAndGenerateAsync → NotificationService broadcasts ReceiveIncident (+ ReceiveAlert per alert) → JSON {referenceNumber, riskLevel, riskScore, alerts, nearestPlace, nearestArea}.'),
    ('Live monitoring: ', 'officer loads /Dashboard (seeded 30 recent + 10 alerts into initLiveMap centre [7.7322, 8.5391] zoom 10) → monitoring.js opens /monitoringHub, invokes JoinDashboard → group “dashboard” receives ReceiveIncident (addLiveMarker + prepend row + toast) and ReceiveAlert (red banner + View-on-map link). Hub itself only has Join/Leave; all fan-out is server-side via IHubContext.'),
    ('Triage: ', '/Incidents list (Take 200 + DataTables) → /Incidents/Details/{id} (detail + 320 px map zoom 14 + assign form + status form + history) → ChangeStatusAsync/AssignAsync write history + audit → officer returns to /Map?focus=lat,lon or acknowledges on /Admin/Alerts.'),
    ('GIS ops: ', '/Map filter form (risk/status/from/to/hotspots) → GET ?handler=GeoJson → GisService filters (≤500 incidents, ≤20 alerts) + DetectHotspotsAsync → ToGeoJson FeatureCollection {kind: incident|alert|hotspot} → live-map.js draws circleMarkers/circles (radiusKm×1000 m) with risk colours (Critical red, High orange, Medium gold, Low green).'),
]:
    add_bullet(b[1], bold_prefix=b[0])
heading2('3.4  Early-warning design (risk + hotspot + alert)')
doc.add_paragraph('Risk scoring is deliberately explainable and configurable. For each incident the active RiskRule supplies MinIncidentCount (density normaliser), RadiusKm/TimeWindowHours (spatio-temporal window) and High/Critical thresholds; only the Medium floor (25) is hard-coded, matching Plan bands 0–24 Low / 25–49 Medium / 50–74 High / 75–100 Critical. Frequency = min(100, nearby×100/threshold); Score = round(0.6×severityWeight + 0.4×frequency), clamped 0–100. Example: Physical Conflict (90) with 1 neighbour under a threshold-3 rule → freq 33 → score round(54+13.2)=67 → High; with 3 neighbours → freq 100 → score 94 → Critical. Hotspot detection is a greedy clustering pass over recent unresolved incidents (each unassigned incident seeds a neighbourhood; neighbourhoods ≥ MinIncidentCount become HotspotResults with centroid means and max-score level). Alerting iterates all active rules, skips incidents already covered by an unacknowledged alert in the same window/radius, and raises “HIGH-RISK HOTSPOT DETECTED” (Frequency) or “CRITICAL incident reported” (Severity) with IncidentCount = max(nearby,1). Full excerpts are reproduced in §4.4–4.6.')
heading2('3.5  Authorisation design')
doc.add_paragraph('Defence in depth is by convention + attribute + UI: Program.cs AuthorizeFolder on /Dashboard, /Incidents, /Map, /Admin (leaving /Report public by design); [Authorize] on Dashboard/Incidents/Map/Alerts pages, [Authorize(Roles="SuperAdmin,Administrator")] on RiskRules + Users pages, [Authorize] on MonitoringHub; _Layout hides Risk rules/Users links unless SuperAdmin/Administrator. LoginPath /Account/Login, AccessDeniedPath /Account/AccessDenied. Password policy is deliberately light (digit + length 6, no upper/symbol requirement) with RequireConfirmedAccount=false and lockoutOnFailure=false — flagged as hardening targets in §7.')

# ================= 4 IMPLEMENTATION =================
heading1('4  Implementation')
heading2('4.1  Technology stack (as-built, not planned)')
add_table(['Layer', 'Choice (evidence)'],
[
    ['Runtime / UI', 'ASP.NET Core 8, net8.0, Nullable + ImplicitUsings (Assignment.csproj:1–19; Program.cs:42–48,94)'],
    ['ORM / DB', 'EF Core 8.0.8 + EF Design 8.0.8 + Pomelo.EntityFrameworkCore.MySql 8.0.2; UseMySql + AutoDetect w/ 8.0.36 fallback (Program.cs:22–23)'],
    ['Auth', 'Microsoft.AspNetCore.Identity.EntityFrameworkCore 8.0.8; cookie LoginPath/AccessDeniedPath (Program.cs:25–48)'],
    ['Realtime', 'SignalR server (AddSignalR, MapHub /monitoringHub) + @microsoft/signalr 8.0.0 CDN (client)'],
    ['GIS / GPS', 'Leaflet 1.9.4 CDN + OSM tiles; browser Geolocation API; Nominatim reverse-geocode (gps.js)'],
    ['Tables / charts deps', 'Bootstrap 5 + jQuery + DataTables 1.13.8 CDN; Chart.js listed in Plan but no chart wired as-built'],
    ['Logging', 'Serilog.AspNetCore 8.0.1; UseSerilog(ReadFrom.Configuration); console + Logs/app-.log daily rolling'],
    ['State', 'AddDistributedMemoryCache + Session (IdleTimeout 2 h); UseSession (Program.cs:19–20,92)'],
])
heading2('4.2  Solution structure and pipeline')
doc.add_paragraph('Single-project solution (AssignmentProject.slnx → Assignment/Assignment.csproj). Request pipeline in Program.cs: Serilog → exception handler/HSTS (non-dev) → HTTPS → static files → routing → session → authentication → authorization → Razor Pages + hub. Startup also runs Database.MigrateAsync() then DbInitializer.SeedAsync() inside a try/catch that logs “Database migration/seed failed” without crashing the host. All domain services are registered Scoped behind interfaces (Program.cs:52–58): IGisService, IRiskAssessmentService, ILocationService, IIncidentService, IAlertService, IAuditService, INotificationService.')
heading2('4.3  Data layer: DbContext, migration, seeds')
doc.add_paragraph('ApplicationDbContext (Data/ApplicationDbContext.cs:7–91) declares the 9 DbSets, the ReferenceNumber unique index, spatial/reporting indexes, Restrict delete behaviour on the two incident parents (to preserve history), Cascade on evidence/history children, the AdministrativeArea self-FK, and HasData seeds (7 types, default rule, 4 areas). Migration 20261008171902_InitialCreate (665 lines, MySQL utf8mb4) creates AspNet* Identity tables (with FullName/IsActive/CreatedAt extension), AuditLogs, ConflictAlerts, IncidentTypes, RiskRules, UserLocations, IncidentReports, IncidentEvidence and IncidentStatusHistories — the schema §3.2 summarises. DbInitializer (Data/DbInitializer.cs:8–33) idempotently creates the 5 roles and the admin@test.com account (Admin123!, EmailConfirmed, SuperAdmin+Administrator) if absent.')
heading2('4.4  Early-warning engine')
add_code('public int CalculateScore(int severityWeight, int nearbyCount, int ruleThreshold)\n{\n  var freq = ruleThreshold <= 0 ? 0\n    : Math.Min(100, nearbyCount * 100 / Math.Max(1, ruleThreshold));\n  var score = (int)Math.Round(severityWeight * 0.6 + freq * 0.4);\n  return Math.Clamp(score, 0, 100);\n}\npublic RiskLevel Classify(int score, int high, int critical)\n{\n  if (score >= critical) return RiskLevel.Critical;\n  if (score >= high) return RiskLevel.High;\n  if (score >= 25) return RiskLevel.Medium;\n  return RiskLevel.Low;\n}\n// EvaluateAsync: load first active rule (or defaults), weight = type?.SeverityWeight ?? 30,\n// nearby = await gis.GetNearbyAsync(lat, lon, rule.RadiusKm, rule.TimeWindowHours), count excludes self.',
title='Excerpt 4-A — Services/RiskAssessmentService.cs:21–46 (60/40 severity/frequency blend).')
add_table(['Scenario (threshold 3, High 50, Critical 75)', 'freq', 'Score', 'Level'],
[
    ['Threat (60), 0 neighbours', '0', '36', 'Medium'],
    ['Threat (60), 2 neighbours', '66', '62', 'High'],
    ['Physical Conflict (90), 1 neighbour', '33', '67', 'High'],
    ['Physical Conflict (90), 3 neighbours', '100', '94', 'Critical'],
    ['Other (15), 0 neighbours', '0', '9', 'Low'],
])
heading2('4.5  GIS service')
add_code('const double EarthKm = 6371.0;\nstatic double ToRad(double d) => d * Math.PI / 180.0;\nHaversineKm = 2 * EarthKm * Asin(Sqrt(Sin²(dLat/2) + Cos(lat1)*Cos(lat2)*Sin²(dLon/2)));\n// GetNearbyAsync: since = UtcNow − hoursBack; latDelta = r/111;\n// lonDelta = r / (111 * Max(0.2, Cos(ToRad(lat))));\n// candidates = incidents in [ReportedAt ≥ since] × bounding box → precise Haversine filter.\n// DetectHotspotsAsync: greedy unassigned-seed clustering; centroid = Avg(lat/lon);\n// level from max score vs rule thresholds. ToGeoJson: FeatureCollection, Point [lon,lat].',
title='Excerpt 4-B — Services/GisService.cs:20–151 (bounding-box + Haversine; greedy hotspots; GeoJSON).')
doc.add_paragraph('The bounding-box pre-filter avoids a full-table Haversine scan without requiring MySQL spatial extensions; the longitude guard Max(0.2, cos φ) prevents division blow-up near the poles. FindNearestAreaAsync is a linear scan over active areas with coordinates — adequate for 4 seed areas, flagged for indexing in §8. ToGeoJson emits kind-tagged Point features so one Leaflet loader serves incidents, alerts and hotspots.')
heading2('4.6  Alerting, incidents, locations, notifications')
add_code('foreach (var rule in activeRules) {\n  var nearby = await gis.GetNearbyAsync(lat, lon, rule.RadiusKm, rule.TimeWindowHours);\n  var covered = await db.ConflictAlerts.Where(a => !a.IsAcknowledged\n    && a.CreatedAt >= UtcNow.AddHours(-rule.TimeWindowHours)).ToListAsync();\n  if (covered.Any(a => gis.HaversineKm(a.Lat, a.Lon, lat, lon) <= a.RadiusKm)) continue;\n  if (nearby.Count >= rule.MinIncidentCount || incident.RiskLevel == RiskLevel.Critical) {\n    db.ConflictAlerts.Add(new ConflictAlert {\n      Title = Critical ? "CRITICAL incident reported" : "HIGH-RISK HOTSPOT DETECTED",\n      TriggerType = Critical ? "Severity" : "Frequency",\n      RiskLevel = Critical ? Critical : High, IncidentCount = Math.Max(nearby.Count, 1), … });\n  }\n}\n// AcknowledgeAsync sets IsAcknowledged/AcknowledgedAt/AcknowledgedById + Status="Acknowledged" + audit.',
title='Excerpt 4-C — Services/AlertService.cs:15–73 (per-rule density check with overlap suppression).')
add_code('NextReferenceNumber() => $"INC-{(Max(Id)+1):D5}"; // e.g. INC-00025\n// CreateAsync: validate IncidentType → copy lat/lon from UserLocation → trim strings →\n// Status=New → risk.EvaluateAsync → save → history {Old="-", New="New"}.\n// ChangeStatusAsync: Status/UpdatedAt/ResolvedAt + history + audit. AssignAsync: officer + audit.\n// GetStatsAsync: Total / Active(!Resolved) / Today(UTC) / Critical(!Resolved) / Unresolved.',
title='Excerpt 4-D — Services/IncidentService.cs:19–111 (identity, lifecycle, dashboard aggregates).')
add_code('// LocationService: static Dictionary<key=sessionId??ip??"anon", hits> pruned to 1 min; ≥10/min ⇒ 429.\n// SaveAsync stamps CapturedAt (browser) vs ReceivedAt (server) separately; Validate: lat ±90, lon ±180, acc 0–100000.\n// NotificationService: hub.Clients.Group("dashboard").SendAsync("ReceiveIncident"/"ReceiveAlert", dto).\n// Hub: [Authorize] MonitoringHub { JoinDashboard() → Groups.AddToGroupAsync("dashboard"); LeaveDashboard() → Remove… }',
title='Excerpt 4-E — Services/LocationService.cs, NotificationService.cs, Hubs/MonitoringHub.cs.')
heading2('4.7  Presentation layer (Razor Pages + JavaScript)')
doc.add_paragraph('Public surface is intentionally tiny: / (hero with “Report an incident” + “Officer dashboard” CTAs and three capability cards), /Report (consent checkbox, Share/Retry buttons, live lat/lon/accuracy/place readout, gps.js only — no type/description fields on the GPS-share form; richer IncidentSubmitDto exists for API-style posts), /Account/Login (email/password/remember-me, default ReturnUrl ~/Dashboard, UI hint of the seed credential) /Logout (POST sign-out → /Index) /AccessDenied, /Privacy and /Error (stock templates, request-id tracing). Authorised surface: /Dashboard (● LIVE badge, 5 stat cards bound to #statTotal/#statActive/Today/#statCritical/Unresolved, #alertBanner, 420 px #dashMap, active-alerts + 30-row incoming-reports tables, inline JSON seed into initLiveMap + connectMonitoring), /Incidents (GET filter q/status/risk/typeId, 200-row table enhanced by DataTables), /Incidents/Details/{id} (risk/status badges, “View location on GIS map” focus link, detail list, 320 px map at zoom 14, assign + status/comment forms, status-history list), /Map (risk/status/from/to/hotspots filter, 600 px #opsMap, fetch GeoJSON then focusOn when ?focus=lat,lon present), /Admin/Alerts (ack buttons + map links), /Admin/RiskRules (read-only list + Edit form for all thresholds with audit “Administrator changed risk configuration”), /Admin/Users (per-row single-role replace from Roles.All). Shared _Layout brands “Conflict Monitor”, gates nav by authentication and admin role, and loads Bootstrap/site.css/jQuery/site.js with per-page Scripts sections for Leaflet/SignalR CDNs.')
add_code('// gps.js: consent-gated getCurrentPosition({enableHighAccuracy:true, timeout:15000, maximumAge:0})\n// → Nominatim GET reverse?format=jsonv2&lat&lon&zoom=14 → POST ?handler=Submit JSON\n//    {latitude,longitude,accuracy,altitude,speed,heading,capturedAt,consent:true,nearestPlace}\n//    + RequestVerificationToken header; renders {referenceNumber, riskLevel, riskScore, nearestPlace}.\n// live-map.js: riskColor {Critical red, High orange, Medium gold, Low green};\n//   initLiveMap(id, seed, {center:[7.7322,8.5391], zoom:10}) on OSM tiles; markerFor popups link\n//   /Incidents/Details/{id}; loadGeoJson draws hotspot L.circle(r×1000) + alert/incident circleMarkers.\n// monitoring.js: HubConnectionBuilder.withUrl("/monitoringHub").withAutomaticReconnect()\n//   .on("ReceiveIncident" → addLiveMarker + row prepend + toast; "ReceiveAlert" → banner)\n//   .start().then(invoke("JoinDashboard")); toast auto-dismiss 4.5 s.',
title='Excerpt 4-F — wwwroot/js/gps.js (117 lines), live-map.js (69), monitoring.js (51).')
heading2('4.8  DTOs, validation and mapping')
doc.add_paragraph('DTOs/Dtos.cs defines LocationDto (ranges), IncidentSubmitDto : LocationDto (type + description 3–2000 chars + reporter/community/LGA/contact lengths), LocationShareDto : LocationDto (Consent must be true, NearestPlace ≤500), and read models LiveLocationDto/AlertDto/HotspotResult for SignalR/GeoJSON. Enforcement is layered: DataAnnotations on DTOs + entities, explicit LocationService.Validate throwing ArgumentException on out-of-range fixes, rate-limit gate before persistence, and antiforgery on both Razor forms and the JSON handler. Incident coordinates are copied from the persisted UserLocation so the report and the fix cannot diverge.')

# ================= 5 TESTING =================
heading1('5  Testing and Evaluation')
heading2('5.1  What evidence exists')
doc.add_paragraph('No automated test project, test framework reference, Dockerfile, CI workflow or README was found (solution contains only the main web project; only project documentation is the Implementation Plan plus inline comments). Verification to date therefore rests on: (a) successful EF Core migration + seed recorded in Logs/app-20261008.log (3,027 lines: initial connection errors on an empty server, then CREATE DATABASE FarmerHerderConflictDb, __EFMigrationsHistory, Applying 20261008171902_InitialCreate, CREATE TABLE … for all domain + Identity tables); (b) a prior Release folder-publish (bin/Release/net8.0, obj/Release/net8.0/PubTmp/Out); (c) manual end-to-end walks implied by the wired UI (report → dashboard/map/incident/alert/admin loops). This section records the manual matrix that should be (re-)executed and its expected results against the as-built code.')
heading2('5.2  Functional test matrix (manual, repeatable)')
add_table(['#', 'Case (steps)', 'Expected (as-built)'],
[
    ['T-1', 'Anonymous POST /Report?handler=Submit with consent + valid GPS', '200 {referenceNumber INC-#####, riskLevel/Score, nearestArea}; row in UserLocations + IncidentReports; SignalR ReceiveIncident; alert only if rule hit'],
    ['T-2', 'Submit without consent / lat=200 / lon=200', '400/validation failure; nothing persisted (Validate throws; Consent required)'],
    ['T-3', '11 shares in 60 s same session/IP', '11th → 429 rate-limited (IsRateLimited ≥10/min)'],
    ['T-4', 'Unauthenticated GET /Dashboard, /Map, /Incidents, /Admin/*, hub JoinDashboard', 'Redirect /Account/Login?ReturnUrl=… (pages); hub join rejected ([Authorize])'],
    ['T-5', 'Login admin@test.com / Admin123! → ~/Dashboard', 'Cookie issued; nav shows officer links + admin links; log “Officer … logged in”'],
    ['T-6', 'Viewer attempts /Admin/Users, /Admin/RiskRules/Edit', '403 → /Account/AccessDenied (role attribute)'],
    ['T-7', 'Report 3 incidents ≤5 km ≤24 h (default rule)', '3rd triggers HIGH-RISK HOTSPOT alert (Frequency, High, count≥3); banner + live-map circle; /Admin/Alerts row'],
    ['T-8', 'Single Physical Conflict (weight 90) alone', 'Score ≈54+ → High or Critical path; CRITICAL alert (Severity) even though count < 3'],
    ['T-9', 'Second cluster inside unacknowledged alert radius+window', 'Suppressed (overlap check) — no duplicate alert row'],
    ['T-10', 'Acknowledge alert; assign officer; advance New→…→Resolved', 'Alert IsAcknowledged + Status Acknowledged; incident history + audit rows; ResolvedAt set; stats decrement'],
    ['T-11', 'GET /Map?handler=GeoJson with risk/status/date/hotspot filters', 'FeatureCollection with kind-tagged Points; hotspot circles radiusKm×1000; ?focus=lat,lon centres at zoom 15'],
    ['T-12', 'Admin edits RiskRule (e.g. Min 3→5)', 'Persisted + UpdatedAt; audit “Administrator changed risk configuration”; subsequent scoring uses new values'],
    ['T-13', 'Restart with empty MySQL', 'Auto-migrate + seed (roles, admin, 7 types, rule, 4 areas) then serve; failure logged not fatal'],
])
heading2('5.3  Evaluation against requirements')
doc.add_paragraph('Against FR-1–FR-12 the build is functionally complete for the happy paths: public reporting, scoring, alerting with dedupe, live picture, triage, GIS export, acknowledgement, configurability and audit are all wired end to end. Non-functional posture is adequate for pilot load (capped queries, pre-filtered scans, 2 h session, daily log rotation) but unmeasured: no load, soak, GPS-accuracy-distribution or map-tile-offline tests were recorded. Risk-model calibration is the principal evaluation gap — the 60/40 blend and rule defaults (3 / 5 km / 24 h / 50 / 75) are plausible but unevidenced; §8 recommends back-testing against dated historical incidents and sensitivity analysis before operational thresholds are frozen.')
heading2('5.4  Defects and gaps observed')
for b in [
    'No automated tests means regressions in scoring, Haversine edge cases (antimeridian, poles) and handler authorisation would go undetected — add xUnit + WebApplicationFactory coverage (§8).',
    'Report GPS-share path always uses the “Other” type, so severity input is coarse for pure shares; consider exposing IncidentType + description on /Report or merging with IncidentSubmitDto.',
    'IncidentEvidence is modelled but no upload UI/handler exists; file-type/size/AV policy is therefore untested.',
    'In-memory rate limiter does not span farm nodes and resets on restart; move to IDistributedCache-backed throttling.',
]    :
    add_bullet(b)

# ================= 6 DEPLOYMENT =================
heading1('6  Deployment and Operating Policy')
heading2('6.1  Prerequisites')
add_table(['Need', 'As-built value / action'],
[
    ['Runtime', '.NET 8 ASP.NET Core runtime (app targets net8.0)'],
    ['Database', 'MySQL 8 (≈8.0.36 fallback); create empty schema or let MigrateAsync create FarmerHerderConflictDb'],
    ['Config', 'ConnectionStrings:DefaultConnection (appsettings.json currently server=localhost;3306;user=root;password=; — Program fallback uses password=root)'],
    ['Seed admin', 'SeedAdmin Email admin@test.com / Password Admin123! — rotate immediately (see §7)'],
    ['Ports', 'Development: http 5278, https 7006 (https profile), IIS Express 32583/44314; production behind reverse proxy + TLS'],
    ['Third-party at runtime', 'Internet egress to OSM tiles + Nominatim (client-side); CDN access to Leaflet/SignalR/DataTables unless vendored'],
])
heading2('6.2  Configure → migrate → run (standard path)')
add_code('dotnet restore\n'
         'dotnet tool install --global dotnet-ef   # once per machine\n'
         'dotnet ef database update --project Assignment/Assignment.csproj\n'
         'dotnet run --project Assignment/Assignment.csproj --launch-profile https\n'
         '# then open https://localhost:7006  (or http://localhost:5278)\n'
         '# login: admin@test.com / Admin123!',
title='Routine 6-A — Restore, migrate, run locally.')
doc.add_paragraph('On first boot the app self-migrates and seeds (roles, admin, taxonomy, rule, areas) and writes Serilog output to console plus Logs/app-<date>.log. The examined log shows exactly this sequence succeeding after initial empty-server connection errors — the expected cold-start signature, not a defect. DetailedErrors=true applies in Development only.')
heading2('6.3  Publish (folder profile)')
doc.add_paragraph('Properties/PublishProfiles/FolderProfile.pubxml publishes Release/Any CPU via FileSystem to C:\\Users\\BDIC-004\\Desktop\\MyAssignment (DeleteExistingFiles=false, ExcludeApp_Data=false, LaunchSiteAfterPublish=true; last publish 2026-10-08T17:59:47 per .pubxml.user; artefacts present under bin/Release/net8.0 and obj/Release/net8.0/PubTmp/Out). Operating policy: publish Release, copy the folder to the host, set ASPNETCORE_ENVIRONMENT=Production, override the connection string + SeedAdmin via environment variables (never ship appsettings secrets), front with IIS/Nginx + TLS, and schedule MySQL dumps plus Logs/ retention. Health check on boot = login as admin and confirm Dashboard stats + /Map GeoJSON return features.')
heading2('6.4  Day-to-day operating policy')
add_table(['Routine', 'Procedure (as-built UI)'],
[
    ['Monitoring shift', 'Keep /Dashboard open (● LIVE); triage ReceiveIncident toasts → open Details → assign officer → advance status with comment; acknowledge alerts only after field verification'],
    ['Alert hygiene', '/Admin/Alerts shows latest 10; acknowledged alerts suppress duplicates in their window/radius — do not ack speculatively or new clusters will be masked'],
    ['Threshold tuning', '/Admin/RiskRules/Edit (SuperAdmin/Administrator only); change one variable at a time; record rationale; audited automatically'],
    ['User lifecycle', '/Admin/Users single-role replace; disable leavers via IsActive; review AuditLogs + status histories weekly'],
    ['Data stewardship', 'Verify Community/LGA spellings (used for grouping); treat browser CapturedAt as advisory, ReceivedAt as authoritative; back up MySQL before rule/seed changes'],
    ['Incident discipline', 'OWASP-style: rotate seed password, enforce HTTPS/HSTS, restrict DB user to least privilege, retain logs ≥90 days'],
])

# ================= 7 SECURITY =================
heading1('7  Security Considerations')
heading2('7.1  Strengths in the build')
for b in [
    'Closed-by-default authorised zone (AuthorizeFolder ×4 + page/hub attributes) with public surface limited to reporting + login by design.',
    'Server never trusts the browser for location: independent ReceivedAt, range validation, consent enforcement, and rate limiting precede persistence.',
    'Antiforgery on Razor forms and on the JSON handler (RequestVerificationToken header from __RequestVerificationToken).',
    'Least-privilege role ladder (5 roles) with admin-only rule/user management, hidden admin nav, and single-role replacement.',
    'Dual audit trail (AuditLog + IncidentStatusHistory with actor, IP, timestamps, comments) and structured Serilog operational log.',
    'Secure-by-default pipeline (HTTPS redirection, HSTS + exception handler outside Development) and parameterised EF Core queries (no string-concatenated SQL).',
]:
    add_bullet(b)
heading2('7.2  Weaknesses and required hardening (ranked)')
add_table(['#', 'Finding', 'Risk', 'Fix'],
[
    ['S-1', 'Seed credential admin@test.com / Admin123! in appsettings.json + UI hint; empty prod DB password; fallback password=root in code', 'High — first-guess takeover', 'Rotate on first boot; move to user-secrets/env/vault; delete UI hint; fail closed if no strong secret'],
    ['S-2', 'Weak password policy (6 chars, digit only) + lockoutOnFailure=false + no 2FA', 'High — brute force', 'Require ≥12 chars/complexity, enable lockout + 2FA for admins, alert on repeated failures'],
    ['S-3', 'Reporter PII (name/contact) stored + broadcast to all dashboard clients', 'Medium — privacy over-collection', 'Minimise DTOs, mask contacts by role, add retention/purge + privacy notice at consent'],
    ['S-4', 'Coarse authorisation (any officer can ack/assign/status); no resource-based checks', 'Medium — misuse', 'Add policies (e.g. only ResponseOfficer/above may ack; assignment limited to team/LGA); test with matrix T-4/T-6'],
    ['S-5', 'In-memory rate limiter; no distributed throttle; no upload policy', 'Medium — flood/abuse', 'Back with IDistributedCache; add CAPTCHA/proof-of-work for anonymous posts; define evidence AV/size/type rules when wiring uploads'],
    ['S-6', 'Client dependency on OSM/Nominatim + CDNs without SRI/fallback', 'Low-Med — tracking/outage', 'Vendor or pin + SRI hashes; handle tile/geocode failure gracefully; document data-sharing with Nominatim'],
])
heading2('7.3  Transport, secrets and logging hygiene')
doc.add_paragraph('Enforce TLS 1.2+ end to end (reverse proxy → Kestrel), HSTS preload in production, and HttpOnly+Secure+SameSite cookies (Identity defaults — verify). Never commit real connection strings or SeedAdmin passwords; the current empty-password connection string must be treated as a local-dev placeholder only. Keep Serilog at Information with Warning for Microsoft.AspNetCore (as configured); ensure no reporter PII, passwords or connection strings are logged; ship Logs/ to a secured sink with ≥90-day retention and restrict file ACLs. MySQL accounts should be least-privilege (no SUPER/FILE), with encrypted backups tested by restore.')

# ================= 8 LIMITATIONS =================
heading1('8  Limitations and Future Work')
heading2('8.1  Limitations (acknowledged)')
for b in [
    'No automated tests, CI or containers — quality rests on manual passes; regressions likely as rules/pages grow.',
    'Naive geospatial stack: double lat/lon + application-side Haversine with (lat,lon)/(ReportedAt)/(Status) B-tree indexes only — no spatial index, no PostGIS/NetTopologySuite; hotspot clustering is O(n²) greedy over capped sets.',
    'Single-node assumptions: in-memory rate limiter, session and SignalR backplane are local (breaks under multi-instance scale-out).',
    'Coarse reporting input (GPS-share path fixed to “Other”) and no evidence-upload UI despite the IncidentEvidence model.',
    'Linear nearest-area scan, hardcoded medium floor (25) and uncalibrated defaults; no back-test against historical ground truth.',
    'External availability coupling: offline officers get no map tiles, no queuing, no SMS/USSD fallback.',
    'Accessibility/i18n gaps: English-only, no low-bandwidth mode, limited ARIA/keyboard treatment on live regions.',
]:
    add_bullet(b)
heading2('8.2  Future work (prioritised)')
add_table(['Priority', 'Work item', 'Why / acceptance'],
[
    ['P0', 'Test + CI: xUnit (scoring, Haversine incl. poles/antimeridian, dedupe), WebApplicationFactory handler/authz tests, GitHub Actions + publish gate', 'No red builds; authz matrix T-4/T-6 green on every PR'],
    ['P0', 'Secrets + auth hardening (S-1/S-2): vault/env secrets, strong policy, lockout + 2FA, remove hint', 'Seed creds unusable after first boot; brute-force lockout verified'],
    ['P1', 'Spatial upgrade: MySQL SPATIAL index or PostGIS + NetTopologySuite; DB-side ST_Distance queries; pagination on GeoJSON', 'Hotspot/nearby p95 < 500 ms at 100k incidents'],
    ['P1', 'Reporting fidelity: expose IncidentType + description + photo evidence on /Report with AV/size/type policy; wire IncidentEvidence end to end', 'Evidence attaches and renders on Details'],
    ['P1', 'Scale-out: Redis backplane + distributed throttle + sticky-free SignalR; CDN/vendor maps JS with SRI', 'Two-instance deploy passes flood test T-3'],
    ['P2', 'Calibration: back-test rules on dated historical data; ROC/sensitivity report; per-LGA adaptive thresholds', 'Documented precision/recall for alert thresholds'],
    ['P2', 'Resilience: offline tile pack, outbox/SMS gateway, queue-based ingestion with dedupe keys', 'Reports accepted with zero connectivity, synced later'],
    ['P3', 'Analytics: Chart.js/DataTables trend views, LGA league tables, export (CSV/GeoJSON), boundary GeoJSON admin editor', 'Monthly situation report in one click'],
])

# ================= 9 CONCLUSION =================
heading1('9  Conclusion')
doc.add_paragraph(
    'The as-built system meets its core promise: a public user can share consented GPS in seconds, and within the same minute an authorised officer sees a scored, mapped, auditable incident — with automatic escalation when incidents cluster or a single grave report arrives. The implementation is faithful to its plan (Razor Pages + Identity + MySQL + SignalR + Leaflet), the domain model is coherent and seeded for immediate pilot use in Benue State, and the early-warning mathematics are transparent and administrator-tunable rather than buried in code. Operational readiness is demonstrated by successful migration/seed logs and a working folder-publish path. The honest caveats are concentrated, not scattered: trust the build for a controlled pilot, but before wider or higher-stakes operation, close the P0 items — automated tests + CI, secret/auth hardening, and threshold calibration — then invest in the spatial, resilience and analytics increments of §8. Done in that order, the project provides a sound, extensible foundation for data-driven farmer–herder conflict prevention.'
)

# ================= REFERENCES =================
heading1('References')
refs = [
    'Microsoft. ASP.NET Core 8 — Razor Pages, Identity, SignalR, Entity Framework Core documentation. https://learn.microsoft.com/aspnet/core (accessed Oct 2026).',
    'Pomelo Foundation. Pomelo.EntityFrameworkCore.MySql 8.0.2 documentation (MySQL provider, ServerVersion.AutoDetect). https://github.com/PomeloFoundation/Pomelo.EntityFrameworkCore.MySql.',
    'Serilog. Serilog.AspNetCore 8.0.1 — structured logging with console + file sinks. https://serilog.net.',
    'Leaflet 1.9.4 + OpenStreetMap tile usage policy; Nominatim reverse-geocoding usage policy (client-side GET https://nominatim.openstreetmap.org/reverse). https://leafletjs.com, https://operations.osmfoundation.org/policies/.',
    'Microsoft SignalR JavaScript client @microsoft/signalr 8.0.0; jQuery; DataTables 1.13.8; Bootstrap 5.',
    'Project sources examined: Assignment/Program.cs; appsettings.json; Data/ApplicationDbContext.cs, DbInitializer.cs, Migrations/20261008171902_InitialCreate; Models/*.cs; DTOs/Dtos.cs; Services/*.cs; Hubs/MonitoringHub.cs; Pages/**; wwwroot/js/gps.js, live-map.js, monitoring.js; Logs/app-20261008.log; Properties/launchSettings.json + PublishProfiles/FolderProfile.pubxml; GIS_Early_Warning_Conflict_Monitoring_Implementation_Plan.md.',
    'OWASP Top 10 (2021) and Application Security Verification Standard — basis for §7 hardening (auth, session, logging, secrets). https://owasp.org.',
]
for i, r_ in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(f'[{i}]  ')
    run.bold = True
    run.font.size = Pt(10)
    run2 = p.add_run(r_)
    run2.font.size = Pt(10)

# ================= APPENDIX A =================
heading1('Appendix A: Command Reference')
doc.add_paragraph('All commands run from the solution root C:\\Users\\BDIC-004\\Documents\\Visual Studio 2026\\Projects\\AssignmentProject unless stated. PowerShell 5.1 syntax (the repo shell); use workdir instead of cd in automation.')
add_table(['Purpose', 'Command'],
[
    ['Restore packages', 'dotnet restore'],
    ['Run (HTTPS profile)', 'dotnet run --project Assignment\\Assignment.csproj --launch-profile https   # https://localhost:7006'],
    ['Run (HTTP profile)', 'dotnet run --project Assignment\\Assignment.csproj --launch-profile http    # http://localhost:5278'],
    ['EF tool (once)', 'dotnet tool install --global dotnet-ef'],
    ['Add migration', 'dotnet ef migrations add <Name> --project Assignment\\Assignment.csproj'],
    ['Apply migrations', 'dotnet ef database update --project Assignment\\Assignment.csproj'],
    ['Inspect migration SQL', 'dotnet ef migrations script --project Assignment\\Assignment.csproj --output migration.sql'],
    ['Publish (mirrors FolderProfile)', 'dotnet publish Assignment\\Assignment.csproj -c Release -o C:\\Users\\BDIC-004\\Desktop\\MyAssignment'],
    ['Watch run (dev)', 'dotnet watch run --project Assignment\\Assignment.csproj'],
    ['Tail Serilog log', 'Get-Content Assignment\\Logs\\app-20261008.log -Tail 50 -Wait'],
    ['MySQL: create DB', 'CREATE DATABASE FarmerHerderConflictDb CHARACTER SET utf8mb4;'],
    ['MySQL: quick counts', 'SELECT COUNT(*) FROM IncidentReports; SELECT COUNT(*) FROM ConflictAlerts WHERE IsAcknowledged=0;'],
    ['MySQL: backup', 'mysqldump -u root -p FarmerHerderConflictDb > farmerherder_%DATE%.sql'],
    ['Smoke: GeoJSON', 'Invoke-RestMethod "https://localhost:7006/Map?handler=GeoJson&showHotspots=true" | ConvertTo-Json -Depth 4'],
    ['Smoke: hub negotiate', 'Invoke-WebRequest "https://localhost:7006/monitoringHub/negotiate?negotiateVersion=1" -Method Post'],
])
add_code('# appsettings.json — connection + logging + seed (dev placeholder; override in production)\n{\n  "ConnectionStrings": { "DefaultConnection": "server=localhost;port=3306;database=FarmerHerderConflictDb;user=root;password=;" },\n  "Serilog": { "MinimumLevel": "Information",\n    "WriteTo": [{ "Name": "Console" },\n      { "Name": "File", "Args": { "path": "Logs/app-.log", "rollingInterval": "Day" } }] },\n  "SeedAdmin": { "Email": "admin@test.com", "Password": "Admin123!" }\n}',
title='Config 6-B — Assignment/appsettings.json (verbatim structure).')

# ================= APPENDIX B =================
heading1('Appendix B: Source Code Layout')
doc.add_paragraph('Filtered tree (excludes bin/, obj/, .vs/, wwwroot/lib/). Line counts for JS are exact; migration/log sizes evidence scale.')
add_code('AssignmentProject/\n├─ AssignmentProject.slnx                      # solution → Assignment/Assignment.csproj\n└─ Assignment/\n   ├─ Program.cs                                # pipeline, Identity, AuthZ folders, DI, Migrate+Seed, MapRazorPages+MapHub\n   ├─ appsettings.json / appsettings.Development.json\n   ├─ Assignment.csproj (.user)                 # net8.0; Identity.EF 8.0.8; EFCore.Design 8.0.8; Pomelo.MySql 8.0.2; Serilog 8.0.1\n   ├─ GIS_Early_Warning_Conflict_Monitoring_Implementation_Plan.md  # normative design doc\n   ├─ Data/ApplicationDbContext.cs             # 9 DbSets + indexes + HasData (7 types, 1 rule, 4 areas)\n   ├─ Data/DbInitializer.cs                    # roles ×5 + admin@test.com seed\n   ├─ Data/Migrations/20261008171902_InitialCreate*.cs  # 665-line schema (utf8mb4)\n   ├─ DTOs/Dtos.cs                             # Location/Submit/Share + LiveLocation/Alert/Hotspot DTOs\n   ├─ Hubs/MonitoringHub.cs                    # [Authorize]; Join/LeaveDashboard → group "dashboard"\n   ├─ Models/                                 # ApplicationUser, UserLocation, IncidentType, IncidentReport,\n   │                                          # ConflictAlert, RiskRule, AdministrativeArea, IncidentEvidence,\n   │                                          # IncidentStatusHistory, AuditLog, Enums (RiskLevel/Status/Roles)\n   ├─ Services/GisService.cs                  # Haversine, bounding-box GetNearby, hotspots, nearest area, GeoJSON\n   ├─ Services/RiskAssessmentService.cs        # 60/40 score + Classify + EvaluateAsync\n   ├─ Services/AlertService.cs                # CheckAndGenerate + Acknowledge + AuditService\n   ├─ Services/IncidentService.cs             # INC-#####, Create, Stats, ChangeStatus, Assign\n   ├─ Services/LocationService.cs             # 10/min limit, Save, Validate\n   ├─ Services/NotificationService.cs         # BroadcastIncident/Alert → group "dashboard"\n   ├─ Pages/Index|Privacy|Error               # public + diagnostics (RequestId tracing)\n   ├─ Pages/Account/Login|Logout|AccessDenied  # cookie auth (ReturnUrl ~/Dashboard)\n   ├─ Pages/Report/Index                      # PUBLIC GPS-share (gps.js; POST ?handler=Submit)\n   ├─ Pages/Dashboard/Index                   # stats + banner + 420px map + tables (live-map+monitoring.js)\n   ├─ Pages/Incidents/Index|Details           # 200-row filter + detail/assign/status/history\n   ├─ Pages/Map/Index                         # ops map + GET ?handler=GeoJson + ?focus=lat,lon\n   ├─ Pages/Admin/Alerts|RiskRules|Users       # ack; rule edit (admin-only); single-role replace (admin-only)\n   ├─ Pages/Shared/_Layout.cshtml             # brand, role-gated nav, Bootstrap/jQuery/Scripts sections\n   ├─ wwwroot/js/gps.js (117)                 # consent → geolocate → Nominatim → POST Submit\n   ├─ wwwroot/js/live-map.js (69)             # Leaflet init/markers/GeoJSON/focus (centre 7.7322,8.5391)\n   ├─ wwwroot/js/monitoring.js (51)           # SignalR join + ReceiveIncident/ReceiveAlert + toasts\n   ├─ wwwroot/js/site.js + css/site.css        # stock template (no app logic)\n   ├─ Logs/app-20261008.log (3,027 lines)     # cold-start errors → CREATE DATABASE → migration → tables\n   └─ Properties/launchSettings.json + PublishProfiles/FolderProfile.pubxml(.user)',
title='Layout B-1 — As-built source tree (abridged).')
doc.add_paragraph('End of report.',).runs[0].italic = True

doc.save(OUT)
print(f'Saved to {OUT}')
