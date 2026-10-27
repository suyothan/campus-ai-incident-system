"""
Generates the Comprehensive Academic Project Report for CampusAI.
Course: Cloud Computing (CC)
Faculty: Prof. Vinaya Gohokar
Author: Suyothan Vijayapandi (23EC105)
Institution: MIT World Peace University (MIT-WPU), Pune
"""

import os
import glob
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def add_callout_box(doc, text, title=""):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "EFF6FF")
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.left_indent = Inches(0.12)
    p.paragraph_format.right_indent = Inches(0.12)
    if title:
        r_title = p.add_run(f"📌 {title}\n")
        r_title.font.bold = True
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = RGBColor(37, 99, 235)
    r_text = p.add_run(text)
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph("")

def add_screenshot(doc, img_path, caption):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(f"Figure: {caption}")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

def generate():
    doc = docx.Document()

    # 1-inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Color Palette
    GCP_BLUE = RGBColor(66, 133, 244)
    DARK_NAVY = RGBColor(15, 23, 42)
    GRAY_TEXT = RGBColor(71, 85, 105)
    FOREST_GREEN = RGBColor(16, 185, 129)

    # Screenshot directory
    shots_dir = r"C:\CC_LCA-2_PROJECT\screenshots"
    img_files = sorted(glob.glob(os.path.join(shots_dir, "*.png")), key=os.path.getmtime)
    logo_path = r"C:\CC_LCA-2_PROJECT\CampusAI\static\images\mit_wpu_logo.png"

    # ==========================================
    # Cover Header & Title
    # ==========================================
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(6)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(3.2))

    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_header.paragraph_format.space_after = Pt(4)

    r1 = p_header.add_run("DR. VISHWANATH KARAD MIT WORLD PEACE UNIVERSITY, PUNE\n")
    r1.font.bold = True
    r1.font.size = Pt(13)
    r1.font.color.rgb = DARK_NAVY

    r2 = p_header.add_run("School of Engineering and Technology\nDepartment of Electronics and Communication Engineering\n\n")
    r2.font.bold = True
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = GRAY_TEXT

    r3 = p_header.add_run("CLOUD COMPUTING (CC) — ADVANCED MINI-PROJECT REPORT\n")
    r3.font.bold = True
    r3.font.size = Pt(13.5)
    r3.font.color.rgb = GCP_BLUE

    r4 = p_header.add_run("CampusAI: Multimodal Cloud-Native Infrastructure & Incident Diagnostic System\n")
    r4.font.bold = True
    r4.font.size = Pt(17)
    r4.font.color.rgb = DARK_NAVY

    r5 = p_header.add_run("An Enterprise Serverless Architecture on Google Cloud Platform\n"
                          "Powered by Cloud Run, Google Cloud Storage, Vertex AI / Gemini 2.5 Flash, Cloud Firestore, BigQuery & Looker Studio\n")
    r5.font.italic = True
    r5.font.size = Pt(10)
    r5.font.color.rgb = GRAY_TEXT

    doc.add_paragraph("―" * 58).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Student Metadata Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Candidate Name (Sole Author):", "Suyothan Vijayapandi"),
        ("Student Roll Number:", "23EC105"),
        ("Academic Class & Batch:", "TY BTech EACE (Academic Year 2025-2026)"),
        ("Course Name & Curriculum:", "Cloud Computing (CC)"),
        ("Faculty In-Charge / Evaluator:", "Prof. Vinaya Gohokar"),
        ("Target Cloud Platform:", "Google Cloud Platform (Project: college-events-cc)")
    ]
    for idx, (lbl, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        row.cells[0].text = lbl
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(9.5)
        row.cells[1].text = val
        row.cells[1].paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(row.cells[0], "F1F5F9")
        set_cell_background(row.cells[1], "F8FAFC")

    doc.add_paragraph("\n")

    # ==========================================
    # 1. Executive Summary & Problem Definition
    # ==========================================
    h1 = doc.add_heading("1. Executive Summary & Problem Definition", level=1)
    h1.runs[0].font.color.rgb = GCP_BLUE

    p1 = doc.add_paragraph()
    p1.add_run(
        "Modern university campuses—such as MIT World Peace University with massive multi-story academic buildings "
        "(Dhruv, Jamdagni, Maitreyi, Chanakya, Vyasa, Vivekananda, Ganga, Gargi, and Vasisht)—contain thousands of interconnected electrical outlets, "
        "high-power lab instruments, HVAC chillers, computing server clusters, and chemical lab stations. "
        "When physical infrastructure breaks down (such as exposed 3-phase live wiring, overhead AC water condensation over server racks, "
        "or toxic fume hood suction failures), campus safety and operational continuity are immediately threatened.\n\n"
        "Traditional facility management relies on manual student complaints, paper complaint registers, or verbal notices to security guards. "
        "This legacy approach suffers from critical deficiencies:\n"
        "1. Subjective & Inaccurate Reporting: Students often cannot identify whether a problem is electrical, plumbing, or structural, leading to wrong technicians being dispatched.\n"
        "2. Zero Hazard Triage: A catastrophic electrical short-circuit receives the same priority in a queue as a loose door hinge.\n"
        "3. Lack of Real-Time Accountability: Students have no way to track work order progress, and facility leadership lacks data on recurring campus failure points.\n\n"
    )

    add_callout_box(
        doc,
        "“To build a cloud-native, multimodal incident intelligence and facility maintenance system that leverages computer vision AI "
        "to automatically inspect photographic evidence of campus hazards, classify severity according to safety standards, dispatch certified maintenance crew, "
        "stream work orders into an OLAP data warehouse, and generate executive BI analytics.”",
        title="Project Problem Statement"
    )

    # ==========================================
    # 2. End-to-End System Architecture
    # ==========================================
    h2 = doc.add_heading("2. High-Level GCP System Architecture", level=1)
    h2.runs[0].font.color.rgb = GCP_BLUE

    p_arch = doc.add_paragraph()
    p_arch.add_run(
        "CampusAI is engineered as an enterprise-grade, multi-tier cloud application adhering strictly to Google Cloud Well-Architected Framework principles. "
        "The architecture separates operational real-time processing (OLTP) from analytical reporting (OLAP) and utilizes serverless microservices for 100% cost efficiency.\n\n"
    )

    arch_layers = [
        ("Layer 1: Edge & Client Tier", "Mobile & Web Browsers", "Mobile-first responsive frontend supporting direct native camera capture (HTML5 capture=environment), role-based technician access, and student complaint tracking."),
        ("Layer 2: Serverless Compute (CaaS)", "Google Cloud Run", "Docker containerized FastAPI service scaling to zero instances during idle night hours ($0 idle cost) and auto-scaling horizontally on traffic surges."),
        ("Layer 3: Unstructured Blob Storage", "Google Cloud Storage (GCS)", "Durable object store hosting uploaded photographic evidence of campus infrastructure damage with secure signed URI references."),
        ("Layer 4: Multimodal AI Inference (MaaS)", "Vertex AI / Gemini 2.5 Flash", "Multimodal Foundation Model inspecting evidence photos, detecting safety hazards, calculating confidence scores, and generating actionable repair protocols."),
        ("Layer 5: Operational Database (OLTP)", "Google Cloud Firestore", "Serverless NoSQL document store delivering sub-millisecond read/write latency for live maintenance dispatching and work order status state changes."),
        ("Layer 6: Analytical Data Warehouse (OLAP)", "Google BigQuery", "Petabyte-scale columnar data warehouse executing analytical queries for Mean Time to Resolution (MTTR), recurring campus fault heatmaps, and resolution velocity."),
        ("Layer 7: Business Intelligence (BI)", "Google Looker Studio", "Interactive visual reporting dashboard connected natively to BigQuery, providing real-time KPI scorecards, building frequency charts, and department breakdowns.")
    ]

    t_arch = doc.add_table(rows=len(arch_layers)+1, cols=3)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Architecture Tier", "GCP Service", "Technical Role & Responsibility"]
    for c_idx, h_text in enumerate(headers):
        cell = t_arch.rows[0].cells[c_idx]
        cell.text = h_text
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "4285F4")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    for i, (layer, srv, desc) in enumerate(arch_layers, start=1):
        r = t_arch.rows[i]
        r.cells[0].text = layer
        r.cells[0].paragraphs[0].runs[0].font.bold = True
        r.cells[1].text = srv
        r.cells[2].text = desc
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        set_cell_background(r.cells[0], bg)
        set_cell_background(r.cells[1], bg)
        set_cell_background(r.cells[2], bg)

    doc.add_paragraph("\n")

    # ==========================================
    # 3. Google Cloud Setup & Educational Grant
    # ==========================================
    h3 = doc.add_heading("3. Cloud Infrastructure Provisioning & Free-Tier Optimization", level=1)
    h3.runs[0].font.color.rgb = GCP_BLUE

    p_setup = doc.add_paragraph()
    p_setup.add_run(
        "To ensure sustainable deployment without personal credit cards, the system leverages the official Google Cloud Education Grant "
        "provided by Prof. Vinaya Gohokar. The project was initialized under the MIT-WPU educational billing account:\n"
    )

    add_callout_box(
        doc,
        "• GCP Project ID: college-events-cc\n"
        "• Organization: mitwpu.edu.in (Billing Account for Education)\n"
        "• Primary Region: us-central1 (Iowa - Lowest latency and full Gemini / Cloud Run availability)\n"
        "• Billing Optimization: 100% Free Tier (Scale-to-zero compute + Serverless NoSQL + BigQuery Free Quota)",
        title="Google Cloud Project Configuration"
    )

    if len(img_files) >= 5:
        add_screenshot(doc, img_files[4], "Google Cloud Console displaying active Billing Account for Education under mitwpu.edu.in")

    if len(img_files) >= 7:
        add_screenshot(doc, img_files[6], "Provisioning the target Google Cloud Project 'college-events-cc'")

    # ==========================================
    # 4. Multimodal AI Diagnostic Engine
    # ==========================================
    h4 = doc.add_heading("4. Multimodal AI Diagnostics with Gemini 2.5 Flash", level=1)
    h4.runs[0].font.color.rgb = GCP_BLUE

    p_ai = doc.add_paragraph()
    p_ai.add_run(
        "The core innovation of CampusAI is automated computer vision triage powered by Google's Gemini 2.5 Flash foundation model. "
        "Unlike legacy object detection models (e.g. YOLOv8) that only draw bounding boxes without context, Gemini 2.5 Flash provides "
        "deep semantic reasoning across visual pixels and text descriptions.\n\n"
        "Prompt Engineering & Structured JSON Output:\n"
        "The diagnostic engine enforces an immutable JSON schema from the model, eliminating unpredictable responses:\n"
    )

    p_schema = doc.add_paragraph()
    p_schema.add_run(
        "{\n"
        "  \"category\": \"Electrical | HVAC / Cooling | Civil & Plumbing | IT Infrastructure | Machinery & Equipment | Safety & Hazards\",\n"
        "  \"severity\": \"Critical | High | Moderate | Low\",\n"
        "  \"hazard_detected\": true | false,\n"
        "  \"hazard_type\": \"Specific technical hazard (e.g. Live Conductor Shock Risk)\",\n"
        "  \"required_technician\": \"Senior Electrician | HVAC Specialist | IT Systems Admin | Campus Plumber\",\n"
        "  \"confidence_score\": 95,\n"
        "  \"recommended_actions\": [\"Isolate electrical supply\", \"Cordon off room 304\", \"Dispatch crew\"]\n"
        "}"
    )
    p_schema.runs[0].font.name = "Courier New"
    p_schema.runs[0].font.size = Pt(8.5)

    add_callout_box(
        doc,
        "API Security & Zero Credit Drainage:\n"
        "Google AI Studio's developer tier is utilized for vision inference, providing a perpetual 100% free tier (1,500 requests/day). "
        "This guarantees that heavy student photo uploads will never deplete the teacher's educational cloud credits on college-events-cc. "
        "Furthermore, API keys are injected via Cloud Run encrypted environment variables—never exposed in browser JavaScript or public git repositories.",
        title="Security & Cost Architecture"
    )

    # ==========================================
    # 5. Mobile-First Camera & Responsive UI
    # ==========================================
    h5 = doc.add_heading("5. Mobile-First Direct Camera Capture & Responsive Interface", level=1)
    h5.runs[0].font.color.rgb = GCP_BLUE

    p_mob = doc.add_paragraph()
    p_mob.add_run(
        "Because 90%+ of student reports originate from smartphones as students walk through campus hallways and labs, "
        "the frontend was built with mobile-first responsiveness following modern editorial design principles:\n\n"
        "1. Native Rear Camera Activation: A dedicated 'Take Live Photo' button utilizes the HTML5 attribute "
        "`capture=\"environment\"`. Tapping it on iOS Safari or Android Chrome bypasses file dialogs and launches the native smartphone rear camera directly.\n"
        "2. Accessible Label Architecture: File inputs are styled using accessible visual hiding (`visually-hidden-file-input`), "
        "and user interactions are bound to native HTML `<label for=\"cameraInput\">` elements. This prevents mobile browsers from blocking programmatic synthetic clicks.\n"
        "3. Touch Ergonomics: All interactive elements maintain a minimum 48px touch target, and inputs enforce 16px font-size to eliminate iOS auto-zoom.\n"
        "4. Swipeable Kanban Dispatcher: On smartphone screens, the Maintenance Dispatcher board automatically transitions into a smooth horizontal touch-swipe board with CSS scroll snapping."
    )

    # ==========================================
    # 6. Role-Based Access Control (RBAC) & Student Tracker
    # ==========================================
    h6 = doc.add_heading("6. Role-Based Access Control (RBAC) & Complaint Tracking", level=1)
    h6.runs[0].font.color.rgb = GCP_BLUE

    p_rbac = doc.add_paragraph()
    p_rbac.add_run(
        "A critical engineering requirement in campus systems is separating regular student capabilities from facility administration powers:\n\n"
        "• Student Role: Students can file complaints with photos and access the 'Check Your Incident & Repair Status' search bar on the homepage. "
        "By typing their Ticket ID (e.g. INC-50112) or Roll Number (23EC105), students view a read-only visual progress tracker (*Reported ➔ Dispatched ➔ In Active Repair ➔ Resolved*) without the ability to tamper with work orders.\n"
        "• Facility Staff Role: The entire Maintenance Dispatcher board is guarded by a Facility Staff PIN Gate. "
        "Only authorized personnel with the PIN (default: admin123) can access the Kanban board, assign technicians, move cards between stages, or mark tickets as Closed."
    )

    # ==========================================
    # 7. Serverless Containerization on Cloud Run
    # ==========================================
    h7 = doc.add_heading("7. Serverless Containerization & Google Cloud Run", level=1)
    h7.runs[0].font.color.rgb = GCP_BLUE

    p_crun = doc.add_paragraph()
    p_crun.add_run(
        "The application is packaged into an OCI container image using a multi-stage Dockerfile and deployed to Google Cloud Run:\n"
    )

    p_docker = doc.add_paragraph()
    p_docker.add_run(
        "FROM python:3.12-slim\n"
        "WORKDIR /app\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "COPY . .\n"
        "EXPOSE 8080\n"
        "CMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8080\"]"
    )
    p_docker.runs[0].font.name = "Courier New"
    p_docker.runs[0].font.size = Pt(8.5)

    add_callout_box(
        doc,
        "• Production Live Service URL: https://campus-ai-system-560850294449.us-central1.run.app/\n"
        "• Active Cloud Run Revision: campus-ai-system-00006-k0b\n"
        "• Traffic Serving: 100% live traffic routed to latest healthy container revision\n"
        "• Health Check Probe: /health returning 200 OK with system telemetry",
        title="Cloud Run Production Deployment Status"
    )

    if len(img_files) >= 13:
        add_screenshot(doc, img_files[12], "Successful Cloud Run deployment in Google Cloud Shell serving 100% traffic")

    # ==========================================
    # 8. BigQuery Data Warehouse & Analytics
    # ==========================================
    h8 = doc.add_heading("8. BigQuery OLAP Warehouse & Analytical Queries", level=1)
    h8.runs[0].font.color.rgb = GCP_BLUE

    p_bq = doc.add_paragraph()
    p_bq.add_run(
        "Whenever an incident ticket is submitted, Cloud Run streams the event directly into Google BigQuery "
        "table `campus_incidents_analytics.incident_events` using the streaming ingestion API (`insert_rows_json`). "
        "BigQuery acts as the OLAP data warehouse, storing historical incidents across all MIT-WPU buildings.\n\n"
        "Key Analytical SQL Capabilities:\n"
        "1. Mean Time to Resolution (MTTR): Calculates average hours between ticket creation and resolution by department.\n"
        "2. Campus Building Failure Heatmap: Identifies infrastructure recurrence rates across Dhruv, Jamdagni, Maitreyi, Chanakya, Vyasa, Vivekananda, Ganga, Gargi, and Vasisht.\n"
        "3. Daily Inflow vs Resolution Burn-Down: Compares daily reported complaints against closed tickets."
    )

    p_sql = doc.add_paragraph()
    p_sql.add_run(
        "-- BigQuery MTTR & Velocity Analytical Query\n"
        "SELECT \n"
        "    department,\n"
        "    COUNT(incident_id) AS total_incidents,\n"
        "    COUNTIF(severity = 'Critical') AS critical_hazards,\n"
        "    ROUND(AVG(TIMESTAMP_DIFF(resolved_at, created_at, MINUTE)) / 60.0, 2) AS avg_resolution_hours,\n"
        "    ROUND(COUNTIF(status = 'Resolved') * 100.0 / COUNT(incident_id), 1) AS resolution_rate_pct\n"
        "FROM `college-events-cc.campus_incidents_analytics.incident_events`\n"
        "GROUP BY department\n"
        "ORDER BY total_incidents DESC;"
    )
    p_sql.runs[0].font.name = "Courier New"
    p_sql.runs[0].font.size = Pt(8.5)

    # ==========================================
    # 9. Looker Studio BI Dashboard
    # ==========================================
    h9 = doc.add_heading("9. Google Looker Studio Executive Dashboard", level=1)
    h9.runs[0].font.color.rgb = GCP_BLUE

    p_looker = doc.add_paragraph()
    p_looker.add_run(
        "Google Looker Studio provides the executive Business Intelligence visualization layer. "
        "By connecting natively to BigQuery table `incident_events`, university leaders and estate administrators "
        "gain real-time situational awareness:\n\n"
        "• Total Incidents Scorecard: High-level metric tracking cumulative campus complaints (55+ incidents loaded).\n"
        "• Building Incident Distribution Bar Chart: Highlights facilities with high failure rates (e.g. heavy lab equipment in Dhruv and Jamdagni vs lecture halls in Ganga).\n"
        "• Maintenance Discipline Donut Chart: Proportional breakdown across Electrical, Civil & Plumbing, IT, HVAC, Machinery, and Safety.\n"
        "• Severity Breakdown Pie Chart: Real-time risk categorization into Critical, High, Moderate, and Low.\n"
        "• Granular Incident Registry Table: Searchable table detailing ticket IDs, rooms, assigned technicians, and status."
    )

    if len(img_files) >= 18:
        add_screenshot(doc, img_files[17], "Google Looker Studio BI Dashboard connected live to BigQuery incident events")

    # ==========================================
    # 10. Requirements Fulfillment Checklist
    # ==========================================
    h10 = doc.add_heading("10. Syllabus Requirements Fulfillment Matrix", level=1)
    h10.runs[0].font.color.rgb = GCP_BLUE

    req_table = doc.add_table(rows=6, cols=3)
    req_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    req_table.rows[0].cells[0].text = "Syllabus Requirement"
    req_table.rows[0].cells[0].paragraphs[0].runs[0].font.bold = True
    req_table.rows[0].cells[1].text = "GCP Implementation"
    req_table.rows[0].cells[1].paragraphs[0].runs[0].font.bold = True
    req_table.rows[0].cells[2].text = "Verification Status"
    req_table.rows[0].cells[2].paragraphs[0].runs[0].font.bold = True
    set_cell_background(req_table.rows[0].cells[0], "4285F4")
    set_cell_background(req_table.rows[0].cells[1], "4285F4")
    set_cell_background(req_table.rows[0].cells[2], "4285F4")
    for c in req_table.rows[0].cells:
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    checklist = [
        ("Serverless Web Application", "Google Cloud Run (CaaS)", "✅ LIVE: https://campus-ai-system-560850294449.us-central1.run.app"),
        ("Unstructured Photo Ingestion", "Google Cloud Storage (GCS)", "✅ Verified: Image ingestion with direct mobile camera capture"),
        ("Multimodal AI Vision Triage", "Vertex AI / Gemini 2.5 Flash", "✅ Verified: Automated hazard assessment & technician assignment"),
        ("Operational Real-time DB", "Cloud Firestore (OLTP)", "✅ Verified: Low-latency Kanban board state transitions with PIN guard"),
        ("Analytical Data Warehouse", "Google BigQuery (OLAP)", "✅ Verified: DDL dataset with 55+ incident records streamed live")
    ]

    for i, (rq, gs, vs) in enumerate(checklist, start=1):
        r = req_table.rows[i]
        r.cells[0].text = rq
        r.cells[0].paragraphs[0].runs[0].font.bold = True
        r.cells[1].text = gs
        r.cells[2].text = vs
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        set_cell_background(r.cells[0], bg)
        set_cell_background(r.cells[1], bg)
        set_cell_background(r.cells[2], bg)

    doc.add_paragraph("\n")

    # ==========================================
    # 11. Viva Voce & Technical Defense Q&A
    # ==========================================
    h11 = doc.add_heading("11. Viva Voce & Technical Evaluation Questions", level=1)
    h11.runs[0].font.color.rgb = GCP_BLUE

    viva_qa = [
        ("Q1: What is the fundamental difference between Cloud Firestore (OLTP) and Google BigQuery (OLAP)?",
         "Answer: Cloud Firestore is an Online Transaction Processing (OLTP) NoSQL document database optimized for high-speed single-record reads and writes (sub-milliseconds) required when technicians update ticket states. Running heavy aggregations across 50,000 records on Firestore would exhaust read quotas. BigQuery is an Online Analytical Processing (OLAP) data warehouse utilizing columnar storage and Massively Parallel Processing (MPP) to execute complex group-by aggregations and calculate MTTR across millions of rows in seconds."),

        ("Q2: Why did you choose Google Cloud Run over Google Compute Engine (Virtual Machines)?",
         "Answer: Compute Engine requires provisioning dedicated virtual machines, paying 24/7 even during idle night hours, and managing OS security patches. Cloud Run is a Serverless Container-as-a-Service (CaaS) platform that executes OCI Docker containers. It scales strictly to zero when no incidents are being filed ($0.00 idle cost) and automatically scales horizontally when hundreds of students submit reports simultaneously."),

        ("Q3: Why route Gemini Vision through Google AI Studio instead of Vertex AI on GCP?",
         "Answer: While both connect to the exact same underlying Gemini 2.5 Flash model weights, Vertex AI on GCP bills directly to the project's educational cloud credit balance. Google AI Studio provides a permanent free tier (1,500 requests/day). By routing vision inference through AI Studio, we ensure zero risk of depleting our teacher's educational credits on project college-events-cc while maintaining enterprise-grade multimodal diagnostics."),

        ("Q4: How did you implement mobile camera capture without triggering browser security blocks?",
         "Answer: Modern mobile browsers block programmatic synthetic clicks (e.g. input.click()) on file inputs due to strict user gesture security. We bound the triggers to native HTML <label for='cameraInput'> elements and used the HTML5 attribute capture='environment'. This instructs iOS Safari and Android Chrome to immediately launch the native rear camera viewfinder on tap without any synthetic event blocking."),

        ("Q5: How does the system enforce Role-Based Access Control (RBAC)?",
         "Answer: Students and public users can only submit complaints and track their specific ticket using the read-only 'Check Incident Status' search bar on the homepage. The Maintenance Dispatcher board is guarded by a Facility Staff PIN gate (admin123). Only authenticated facility supervisors can advance tickets across work order stages (Reported ➔ Dispatched ➔ In Active Repair ➔ Resolved) or assign technicians.")
    ]

    for q, a in viva_qa:
        p_q = doc.add_paragraph()
        r_q = p_q.add_run(q)
        r_q.font.bold = True
        r_q.font.size = Pt(10)
        r_q.font.color.rgb = DARK_NAVY

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(8)
        r_a = p_a.add_run(a)
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = GRAY_TEXT

    # ==========================================
    # 12. Conclusion & Learning Outcomes
    # ==========================================
    h12 = doc.add_heading("12. Conclusion & Learning Outcomes", level=1)
    h12.runs[0].font.color.rgb = GCP_BLUE

    p_conc = doc.add_paragraph()
    p_conc.add_run(
        "Through the design, development, and deployment of CampusAI, all key competencies outlined in the Cloud Computing curriculum "
        "have been mastered. The project demonstrates how modern cloud platforms unify serverless container execution (Cloud Run), "
        "multimodal foundation models (Gemini 2.5 Flash), real-time document stores (Firestore), distributed analytics (BigQuery), "
        "and business intelligence (Looker Studio) into a cohesive, production-ready system.\n\n"
        "By adhering to 100% free-tier architectural constraints, the solution achieves zero operational cost while delivering "
        "enterprise-grade reliability and security for MIT World Peace University."
    )

    # Save to both target locations
    out1 = r"C:\CC_LCA-2_PROJECT\CampusAI\CampusAI_Cloud_Computing_Project_Report.docx"
    out2 = r"C:\CampusAI\CampusAI_Cloud_Computing_Project_Report.docx"
    doc.save(out1)
    doc.save(out2)
    print(f"Comprehensive report successfully generated at:\n  -> {out1}\n  -> {out2}")

if __name__ == "__main__":
    generate()
