"""
Generates academic project report for CampusAI Project in .docx format.
Author: Suyothan Vijayapandi (23EC105)
Faculty: Prof. Vinaya Gohokar
Institution: MIT-WPU Pune
"""
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Page Margins (1 inch all around)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Color Constants (ElevenLabs Editorial & GCP Palette)
COLOR_PRIMARY = RGBColor(12, 10, 9)       # Warm Near-Black
COLOR_MUTED = RGBColor(87, 83, 78)        # Charcoal Muted
COLOR_ACCENT = RGBColor(66, 133, 244)     # Google Cloud Blue
COLOR_DARK_BLUE = RGBColor(26, 60, 110)   # MIT-WPU Navy

# Helper: Style Run
def style_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color=COLOR_PRIMARY):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color

# Helper: Heading
def add_custom_heading(doc, text, level=1):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    size = 18 if level == 1 else (14 if level == 2 else 12)
    color = COLOR_PRIMARY if level == 1 else COLOR_DARK_BLUE
    run = h.add_run(text)
    style_run(run, font_name="Arial", size_pt=size, bold=True, color=color)
    return h

# Helper: Paragraph
def add_p(doc, text="", space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        r = p.add_run(text)
        style_run(r, font_name="Times New Roman", size_pt=11.5)
    return p

# -------------------------------------------------------------
# TITLE & COVER
# -------------------------------------------------------------
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_before = Pt(20)
title_p.paragraph_format.space_after = Pt(8)
r_title = title_p.add_run("CAMPUSAI: MULTIMODAL CLOUD-NATIVE INFRASTRUCTURE & INCIDENT DIAGNOSTIC SYSTEM")
style_run(r_title, font_name="Arial", size_pt=20, bold=True, color=COLOR_DARK_BLUE)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_p.paragraph_format.space_after = Pt(24)
r_sub = sub_p.add_run("A 6-Tier Serverless Cloud Architecture on Google Cloud Platform (GCP)")
style_run(r_sub, font_name="Arial", size_pt=13, italic=True, color=COLOR_MUTED)

# Metadata Table
meta_tbl = doc.add_table(rows=5, cols=2)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Course / Subject:", "Cloud Computing (CC) Laboratory Continuous Assessment"),
    ("Submitted By:", "Suyothan Vijayapandi (Roll No: 23EC105)"),
    ("Academic Department:", "School of Electronics & Communication Engineering (ECE)"),
    ("Institution:", "Dr. Vishwanath Karad MIT World Peace University (MIT-WPU), Pune"),
    ("Faculty In-Charge:", "Prof. Vinaya Gohokar")
]
for row_idx, (k, v) in enumerate(meta_data):
    cell_k = meta_tbl.cell(row_idx, 0)
    cell_v = meta_tbl.cell(row_idx, 1)
    cell_k.width = Inches(2.2)
    cell_v.width = Inches(4.3)
    
    p_k = cell_k.paragraphs[0]
    p_k.paragraph_format.space_after = Pt(3)
    r_k = p_k.add_run(k)
    style_run(r_k, font_name="Arial", size_pt=10.5, bold=True, color=COLOR_PRIMARY)
    
    p_v = cell_v.paragraphs[0]
    p_v.paragraph_format.space_after = Pt(3)
    r_v = p_v.add_run(v)
    style_run(r_v, font_name="Times New Roman", size_pt=10.5, color=COLOR_PRIMARY)

doc.add_page_break()

# -------------------------------------------------------------
# 1. ABSTRACT
# -------------------------------------------------------------
add_custom_heading(doc, "1. Executive Summary & Abstract", level=1)
add_p(doc, 
    "Campus facility management in expansive academic institutions often suffers from slow manual triage, inaccurate fault reporting, and lack of real-time hazard severity assessment. When students or staff notice hazardous anomalies—such as exposed 230V wiring under computer workbenches, ruptured HVAC chiller conduits, or laboratory equipment failures—verbal or paper complaints frequently face multi-day latency before licensed technicians are dispatched."
)
add_p(doc, 
    "CampusAI addresses this institutional challenge by engineering a fully serverless, cloud-native multimodal diagnostic engine deployed on Google Cloud Platform (GCP). The application allows students at Dr. Vishwanath Karad MIT World Peace University (MIT-WPU) to capture photographic evidence across campus complexes (Dhruv, Jamdagni, Maitreyi, Chanakya, Vyasa, Vivekananda, Ganga, Gargi, and Vasisht). The ingested image is evaluated in sub-second latency by Google Gemini 2.5 Flash / Vertex AI Multimodal Computer Vision to classify the failure, assign OSHA-compliant severity ratings, recommend repair protocols, and stream live dispatch records to on-call technicians."
)

# -------------------------------------------------------------
# 2. GOOGLE CLOUD ARCHITECTURE
# -------------------------------------------------------------
add_custom_heading(doc, "2. Cloud-Native 6-Service System Architecture", level=1)
add_p(doc, 
    "CampusAI leverages six complementary Google Cloud Platform services to form a decoupled, enterprise-grade architecture with zero idle compute costs (scale-to-zero model):"
)

services = [
    ("Google Cloud Run (Compute Tier)", "Hosts the containerized FastAPI asynchronous backend. Scales automatically from 0 to 1,000+ instances during campus disaster spikes, guaranteeing low latency and 100% free tier idle execution."),
    ("Google Cloud Storage (Object Store)", "Provides durable, geographically distributed bucket storage for raw image evidence uploaded by students, with pre-signed secure access."),
    ("Google Vertex AI / Gemini 2.5 Flash (AI Tier)", "Executes multimodal visual reasoning over images and user descriptions, returning structured technical JSON with OSHA hazard flags, root cause diagnosis, and required technician skill levels."),
    ("Cloud Firestore (OLTP Database)", "Serverless NoSQL document database maintaining live incident tickets, dispatch state transitions (Reported -> Dispatched -> In Repair -> Resolved), and technician assignments."),
    ("Google BigQuery (OLAP Data Warehouse)", "Petabyte-scale analytics engine calculating institutional maintenance velocity, Mean Time to Resolution (MTTR), and hazard density across campus buildings."),
    ("Google Looker Studio (BI Reporting)", "Interactive executive business intelligence dashboard directly connected to BigQuery tables, offering live data filtering for campus administration.")
]

svc_tbl = doc.add_table(rows=len(services)+1, cols=2)
svc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_0 = svc_tbl.cell(0, 0)
hdr_1 = svc_tbl.cell(0, 1)
hdr_0.paragraphs[0].add_run("Google Cloud Service").font.bold = True
hdr_1.paragraphs[0].add_run("Role in CampusAI Architecture").font.bold = True
hdr_0.width = Inches(2.2)
hdr_1.width = Inches(4.3)

for idx, (svc_name, svc_desc) in enumerate(services):
    c0 = svc_tbl.cell(idx+1, 0)
    c1 = svc_tbl.cell(idx+1, 1)
    c0.width = Inches(2.2)
    c1.width = Inches(4.3)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run(svc_name)
    style_run(r0, font_name="Arial", size_pt=9.5, bold=True)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run(svc_desc)
    style_run(r1, font_name="Times New Roman", size_pt=9.5)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# -------------------------------------------------------------
# 3. MULTIMODAL AI & GEMINI VISION IMPLEMENTATION
# -------------------------------------------------------------
add_custom_heading(doc, "3. Multimodal Computer Vision Diagnostic Pipeline", level=1)
add_p(doc, 
    "The core innovation of CampusAI is automated multimodal facility inspection. When an incident photo (JPG, PNG, or WebP) is submitted, the backend streams the image payload encoded as base64 to Google's generative language API using gemini-2.5-flash."
)
add_p(doc, 
    "The system enforces strict structured JSON outputs from the LLM, populating the following operational fields:"
)

points = [
    "Category Classification: Electrical, Civil & Plumbing, IT Infrastructure, Lab Equipment, or Sanitation.",
    "OSHA Severity Rating: Critical (Priority 1), High (Priority 2), Moderate (Priority 3), or Low (Priority 4).",
    "Hazard Flagging: Detects shock risks, structural water ingress, toxic fume generation, or slip hazards.",
    "Technical Diagnosis: Precise electrical, civil, or mechanical engineering observations.",
    "Protocol & Protocol Instructions: Specific containment protocols (e.g. 'De-energize sub-panel DB-04, replace with 4mm² flame-retardant cable').",
    "Estimated Repair Duration: Quantitative hours required to complete resolution for workload balancing."
]
for pt in points:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(pt)
    style_run(r, font_name="Times New Roman", size_pt=11)

# -------------------------------------------------------------
# 4. BIGQUERY ANALYTICS & DATA WAREHOUSING
# -------------------------------------------------------------
add_custom_heading(doc, "4. BigQuery Schema & Analytical Aggregations", level=1)
add_p(doc, 
    "To support executive analytics and administrative oversight, incident documents are partitioned into Google BigQuery under dataset `campus_ai_analytics` and table `incidents`. Below is the Data Definition Language (DDL) schema deployed:"
)

sql_snippet = (
    "CREATE TABLE IF NOT EXISTS `college-events-cc.campus_ai_analytics.incidents` (\n"
    "    incident_id STRING NOT NULL,\n"
    "    timestamp TIMESTAMP NOT NULL,\n"
    "    student_name STRING,\n"
    "    roll_no STRING,\n"
    "    department STRING,\n"
    "    building STRING,\n"
    "    room STRING,\n"
    "    title STRING,\n"
    "    category STRING,\n"
    "    severity STRING,\n"
    "    hazard_detected BOOLEAN,\n"
    "    hazard_type STRING,\n"
    "    status STRING,\n"
    "    assigned_technician STRING,\n"
    "    confidence_score INT64,\n"
    "    repair_hours FLOAT64,\n"
    "    resolved_at TIMESTAMP\n"
    ")\n"
    "PARTITION BY DATE(timestamp)\n"
    "CLUSTER BY building, category, severity;"
)
p_code = doc.add_paragraph()
p_code.paragraph_format.space_before = Pt(4)
p_code.paragraph_format.space_after = Pt(6)
p_code.paragraph_format.left_indent = Inches(0.4)
r_code = p_code.add_run(sql_snippet)
style_run(r_code, font_name="Courier New", size_pt=9.5, color=COLOR_PRIMARY)

add_p(doc, 
    "BigQuery allows campus facility managers to run sub-second queries calculating Mean Time to Resolution (MTTR):"
)

mttr_sql = (
    "SELECT building, category, \n"
    "       COUNT(*) as total_faults,\n"
    "       ROUND(AVG(TIMESTAMP_DIFF(resolved_at, timestamp, MINUTE) / 60.0), 2) as avg_mttr_hours\n"
    "FROM `college-events-cc.campus_ai_analytics.incidents`\n"
    "WHERE status = 'Resolved'\n"
    "GROUP BY building, category\n"
    "ORDER BY avg_mttr_hours DESC;"
)
p_code2 = doc.add_paragraph()
p_code2.paragraph_format.space_before = Pt(4)
p_code2.paragraph_format.space_after = Pt(8)
p_code2.paragraph_format.left_indent = Inches(0.4)
r_code2 = p_code2.add_run(mttr_sql)
style_run(r_code2, font_name="Courier New", size_pt=9.5, color=COLOR_PRIMARY)

# -------------------------------------------------------------
# 5. UI/UX DESIGN SYSTEM (ELEVENLABS SPECIFICATION)
# -------------------------------------------------------------
add_custom_heading(doc, "5. Design System: ElevenLabs Editorial Standards", level=1)
add_p(doc, 
    "In accordance with modern web engineering standards, the user interface was designed using the official ElevenLabs Design System (extracted via `npx getdesign add elevenlabs`)."
)
add_p(doc, 
    "Key characteristics implemented include:"
)
design_pts = [
    "Default Light Canvas (#f6f6f5): Clean off-white editorial surface paired with warm near-black ink (#0c0a09) and pure white floating cards (#ffffff).",
    "Editorial Display Typography: High-elegance EB Garamond display serif at weight 400 with negative tracking (-0.025em), paired with clean Inter body font.",
    "Atmospheric Pastel Blooms: Subtle radial gradient ambient orbs (mint #86efac, lavender #c4b5fd, peach #fdba74) providing visual depth without loud saturated neon colors.",
    "Signature Pill Components: Tactile pill buttons (border-radius: 9999px) with dark primary ink and outline secondaries.",
    "MIT-WPU Institutional Branding: Official high-resolution university dome logo integrated into the top navigation bar at 52px height."
]
for d in design_pts:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(d)
    style_run(r, font_name="Times New Roman", size_pt=11)

# -------------------------------------------------------------
# 6. REPOSITORY & DEPLOYMENT INSTRUCTIONS
# -------------------------------------------------------------
add_custom_heading(doc, "6. Public Verification & Deployment Links", level=1)
add_p(doc, 
    "The source code and cloud configuration scripts have been published as an open-source repository on GitHub:"
)

links = [
    ("GitHub Repository:", "https://github.com/suyothan/campus-ai-incident-system"),
    ("GCP Cloud Run Service:", "campus-ai-system (Deployed via Cloud Shell)"),
    ("Target GCP Project:", "college-events-cc (Region: us-central1)"),
    ("Multimodal AI Model:", "Google Gemini 2.5 Flash (models/gemini-2.5-flash)")
]
for k, v in links:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    r_k = p.add_run(k + " ")
    style_run(r_k, font_name="Arial", size_pt=10.5, bold=True)
    r_v = p.add_run(v)
    style_run(r_v, font_name="Courier New", size_pt=10, color=COLOR_ACCENT)

# -------------------------------------------------------------
# 7. CONCLUSION
# -------------------------------------------------------------
add_custom_heading(doc, "7. Educational Outcome & Conclusion", level=1)
add_p(doc, 
    "CampusAI successfully demonstrates how serverless containerization (Cloud Run), multimodal artificial intelligence (Gemini 2.5), operational document stores (Firestore), and analytical data warehouses (BigQuery) can be united into a cost-effective, zero-maintenance university management solution. By eliminating traditional server provisioning and relying entirely on event-driven cloud primitives, the entire campus facility diagnostic pipeline operates reliably within the Google Cloud Free Tier."
)

output_path = r"c:\CC_LCA-2_PROJECT\CampusAI\CampusAI_Cloud_Computing_Project_Report.docx"
doc.save(output_path)
print("Report successfully generated at:", output_path)
