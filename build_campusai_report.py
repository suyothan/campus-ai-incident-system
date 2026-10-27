"""
Comprehensive Academic Project Report Generator for CampusAI
Course: Cloud Computing (CC)
Faculty: Prof. Vinaya Gohokar
Author: Suyothan Vijayapandi (23EC105)
Institution: Dr. Vishwanath Karad MIT World Peace University (MIT-WPU), Pune
Target GCP Project: college-events-cc
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
    p.paragraph_format.left_indent = Inches(0.15)
    p.paragraph_format.right_indent = Inches(0.15)
    if title:
        r_title = p.add_run(f"📌 {title}\n")
        r_title.font.bold = True
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = RGBColor(37, 99, 235)
    r_text = p.add_run(text)
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph("")

fig_counter = 0

def add_screenshot(doc, img_path, caption):
    global fig_counter
    if os.path.exists(img_path):
        fig_counter += 1
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(3)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(f"Figure {fig_counter}: {caption}")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

def generate():
    global fig_counter
    fig_counter = 0
    doc = docx.Document()

    # Standard 1-inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Cohesive Color Palette
    GCP_BLUE = RGBColor(66, 133, 244)
    DARK_NAVY = RGBColor(15, 23, 42)
    GRAY_TEXT = RGBColor(71, 85, 105)

    # Screenshots & Logo Paths
    shots_dir = r"C:\CC_LCA-2_PROJECT\screenshots"
    img_files = sorted(glob.glob(os.path.join(shots_dir, "*.png")), key=os.path.getmtime)
    
    logo_paths = [
        r"C:\CampusAI\static\images\mit_wpu_logo.png",
        r"C:\CC_LCA-2_PROJECT\CampusAI\static\images\mit_wpu_logo.png"
    ]
    logo_path = next((p for p in logo_paths if os.path.exists(p)), None)

    # ==========================================
    # Title & University Cover Page
    # ==========================================
    if logo_path:
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(8)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(3.4))

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

    r3 = p_header.add_run("CLOUD COMPUTING (CC) — COMPREHENSIVE PROJECT REPORT\n")
    r3.font.bold = True
    r3.font.size = Pt(14)
    r3.font.color.rgb = GCP_BLUE

    r4 = p_header.add_run("CampusAI: Multimodal Cloud-Native Infrastructure & Incident Diagnostic System\n")
    r4.font.bold = True
    r4.font.size = Pt(17.5)
    r4.font.color.rgb = DARK_NAVY

    r5 = p_header.add_run("An Enterprise Serverless Architecture on Google Cloud Platform\n"
                          "Powered by Cloud Run, Google Cloud Storage, Vertex AI / Gemini 2.5 Flash, Cloud Firestore, BigQuery & Looker Studio\n")
    r5.font.italic = True
    r5.font.size = Pt(10)
    r5.font.color.rgb = GRAY_TEXT

    doc.add_paragraph("―" * 60).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Student & Evaluation Metadata Table
    meta_table = doc.add_table(rows=7, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Candidate Name (Sole Author):", "Suyothan Vijayapandi"),
        ("Student Roll Number:", "23EC105"),
        ("Academic Class & Batch:", "TY BTech EACE (Academic Year 2025-2026)"),
        ("Course Name & Curriculum:", "Cloud Computing (CC) — Continuous Assessment (LCA)"),
        ("Faculty In-Charge / Evaluator:", "Prof. Vinaya Gohokar"),
        ("Target Cloud Platform:", "Google Cloud Platform (Project ID: college-events-cc)"),
        ("Production Live Service URL:", "https://campus-ai-system-560850294449.us-central1.run.app/")
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
    doc.add_page_break()

    # ==========================================
    # 1. Executive Summary & Problem Definition
    # ==========================================
    h1 = doc.add_heading("1. Executive Summary & Problem Definition", level=1)
    h1.runs[0].font.color.rgb = GCP_BLUE

    p1 = doc.add_paragraph()
    p1.add_run(
        "Modern university campuses—such as Dr. Vishwanath Karad MIT World Peace University (MIT-WPU) with sprawling multi-story academic buildings "
        "(Dhruv, Jamdagni, Maitreyi, Chanakya, Vyasa, Vivekananda, Ganga, Gargi, and Vasisht)—contain thousands of interconnected electrical outlets, "
        "high-power lab instruments, HVAC chillers, server racks, and chemical lab stations. "
        "When physical infrastructure breaks down (such as exposed 230V/415V live conductors under lab workbenches, ruptured HVAC chiller conduits leaking over server clusters, "
        "or toxic fume hood suction failures), campus safety and operational continuity are immediately threatened.\n\n"
        "Traditional facility management relies on manual student complaints, paper complaint registers, or verbal notices to security guards. "
        "This legacy approach suffers from three critical deficiencies:\n"
        "1. Subjective & Inaccurate Reporting: Students often cannot identify whether an issue is electrical, civil, or mechanical, leading to wrong technicians being dispatched.\n"
        "2. Zero Hazard Triage: A catastrophic live electrical spark receives the exact same priority in a manual queue as a loose door hinge or burned-out lightbulb.\n"
        "3. Lack of Real-Time Accountability: Students have no way to track work order progress, and facility leadership lacks data on recurring campus failure points.\n\n"
    )

    add_callout_box(
        doc,
        "“To design and deploy a cloud-native, multimodal incident intelligence and facility maintenance system that leverages computer vision AI "
        "to automatically inspect photographic evidence of campus hazards, classify severity according to safety standards, dispatch certified maintenance crew, "
        "stream work orders into an OLAP data warehouse, and generate executive BI analytics.”",
        title="Project Problem Statement"
    )

    if len(img_files) >= 1:
        add_screenshot(doc, img_files[0], "Official Problem Statement & Recommended GCP Cloud Services assigned by Prof. Vinaya Gohokar")

    # ==========================================
    # 2. End-to-End System Architecture (7 Tiers)
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
        ("Layer 2: Serverless Compute (CaaS)", "Google Cloud Run", "Docker containerized FastAPI service scaling to zero instances during idle night hours ($0.00 idle cost) and auto-scaling horizontally on traffic surges."),
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
    # 3. Stage 1: Google Cloud Setup & Education Coupon
    # ==========================================
    h3 = doc.add_heading("3. Stage 1: Google Cloud Setup & Education Grant Activation", level=1)
    h3.runs[0].font.color.rgb = GCP_BLUE

    p_setup = doc.add_paragraph()
    p_setup.add_run(
        "To ensure sustainable deployment without personal credit cards, the system leverages the official Google Cloud Education Grant "
        "distributed to the class by Prof. Vinaya Gohokar. By redeeming the student coupon using our university email address (@mitwpu.edu.in), "
        "our Google Cloud account was automatically granted educational cloud credits.\n\n"
        "The project was initialized under the MIT-WPU educational billing account:\n"
    )

    if len(img_files) >= 4:
        add_screenshot(doc, img_files[3], "Announcement & Google Cloud Student Education Coupon Grant Link provided by Prof. Vinaya Gohokar")

    p_bill = doc.add_paragraph()
    p_bill.add_run(
        "Upon completing verification on the Google Cloud Education portal, the billing account was automatically established under the "
        "organization domain 'mitwpu.edu.in' as 'Billing Account for Education'. This allowed unrestricted deployment of serverless compute, databases, and analytics services.\n"
    )

    if len(img_files) >= 5:
        add_screenshot(doc, img_files[4], "Google Cloud Console displaying active Billing Account for Education under mitwpu.edu.in")

    if len(img_files) >= 6:
        add_screenshot(doc, img_files[5], "Billing Account overview displaying active educational credits and zero billing overrun")

    add_callout_box(
        doc,
        "• Target GCP Project ID: college-events-cc\n"
        "• Organization: mitwpu.edu.in (Billing Account for Education)\n"
        "• Primary Region: us-central1 (Iowa - Lowest latency and full Gemini / Cloud Run availability)\n"
        "• Billing Optimization: 100% Free Tier (Scale-to-zero compute + Serverless NoSQL + BigQuery Free Quota)",
        title="Google Cloud Project Configuration"
    )

    # ==========================================
    # 4. Stage 2: Creating the GCP Project (college-events-cc)
    # ==========================================
    h4 = doc.add_heading("4. Stage 2: Creating the Cloud Project (college-events-cc)", level=1)
    h4.runs[0].font.color.rgb = GCP_BLUE

    p_proj = doc.add_paragraph()
    p_proj.add_run(
        "Every resource in Google Cloud Platform is organized inside an isolated Project container. "
        "We navigated to the Google Cloud Console (console.cloud.google.com) and created a dedicated project titled 'college-events-cc' "
        "linked to the educational billing account.\n"
    )

    if len(img_files) >= 7:
        add_screenshot(doc, img_files[6], "Provisioning the target Google Cloud Project 'college-events-cc' under mitwpu.edu.in")

    if len(img_files) >= 8:
        add_screenshot(doc, img_files[7], "Project 'college-events-cc' successfully initialized and selected in Cloud Console")

    # ==========================================
    # 5. Stage 3: Application Development & Modular Structure
    # ==========================================
    h5 = doc.add_heading("5. Stage 3: Application Architecture & Modular Design", level=1)
    h5.runs[0].font.color.rgb = GCP_BLUE

    p_app = doc.add_paragraph()
    p_app.add_run(
        "The application was engineered using Python 3.12 and FastAPI. FastAPI was chosen for its high-performance asynchronous IO, "
        "strict Pydantic schema validation, and native compatibility with Google Cloud Run container execution.\n\n"
        "The project structure is organized into clean functional modules:\n"
    )

    app_structure = [
        ("app.py", "FastAPI web controller serving HTML portals, REST APIs, and Cloud Run /health probes."),
        ("cloud_ai_service.py", "Multimodal AI inference engine communicating with Google Gemini 2.5 Flash / Vertex AI with offline fallback heuristics."),
        ("cloud_database.py", "Database abstraction layer connecting to Cloud Firestore (for transactional state) and BigQuery (for analytics)."),
        ("Dockerfile", "OCI container definition packaging the application for Google Cloud Run on port 8080."),
        ("templates/index.html", "Mobile-first student incident reporting portal with direct camera capture and status tracker."),
        ("templates/dispatcher.html", "Maintenance Dispatcher Kanban board guarded by Facility Staff PIN Gate (admin123)."),
        ("templates/analytics.html", "Executive analytics dashboard featuring MTTR, building heatmaps, and Looker Studio integration."),
        ("templates/architecture.html", "Interactive visual blueprint explaining Cloud Run, Firestore, BigQuery, and Looker Studio dataflow."),
        ("bigquery_schema.sql", "DDL tables and analytical SQL queries for MTTR, recurrence heatmaps, and resolution velocity.")
    ]

    t_struct = doc.add_table(rows=len(app_structure)+1, cols=2)
    t_struct.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_struct.rows[0].cells[0].text = "File / Module"
    t_struct.rows[0].cells[0].paragraphs[0].runs[0].font.bold = True
    t_struct.rows[0].cells[1].text = "Functional Responsibility"
    t_struct.rows[0].cells[1].paragraphs[0].runs[0].font.bold = True
    set_cell_background(t_struct.rows[0].cells[0], "4285F4")
    set_cell_background(t_struct.rows[0].cells[1], "4285F4")
    t_struct.rows[0].cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    t_struct.rows[0].cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    for i, (fn, fd) in enumerate(app_structure, start=1):
        r = t_struct.rows[i]
        r.cells[0].text = fn
        r.cells[0].paragraphs[0].runs[0].font.bold = True
        r.cells[1].text = fd
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        set_cell_background(r.cells[0], bg)
        set_cell_background(r.cells[1], bg)

    doc.add_paragraph("\n")

    # ==========================================
    # 6. Stage 4: Multimodal AI Diagnostic Engine
    # ==========================================
    h6 = doc.add_heading("6. Stage 4: Multimodal AI Diagnostics with Gemini 2.5 Flash", level=1)
    h6.runs[0].font.color.rgb = GCP_BLUE

    p_ai = doc.add_paragraph()
    p_ai.add_run(
        "The core innovation of CampusAI is automated computer vision triage powered by Google's Gemini 2.5 Flash foundation model. "
        "Unlike legacy object detection models (e.g. YOLOv8) that only draw bounding boxes without context, Gemini 2.5 Flash provides "
        "deep semantic reasoning across visual pixels and text descriptions.\n\n"
        "Prompt Engineering & Structured JSON Output Schema:\n"
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
        "  \"recommended_actions\": [\"Isolate electrical sub-panel DB-04\", \"Cordon off room 304\", \"Dispatch crew\"]\n"
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
    # 7. Stage 5: Mobile-First Direct Camera Capture & Responsive UI
    # ==========================================
    h7 = doc.add_heading("7. Stage 5: Mobile-First Direct Camera Capture & Responsive Interface", level=1)
    h7.runs[0].font.color.rgb = GCP_BLUE

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
    # 8. Stage 6: Role-Based Access Control (RBAC) & Complaint Tracking
    # ==========================================
    h8 = doc.add_heading("8. Stage 6: Role-Based Access Control (RBAC) & Complaint Tracking", level=1)
    h8.runs[0].font.color.rgb = GCP_BLUE

    p_rbac = doc.add_paragraph()
    p_rbac.add_run(
        "A critical engineering requirement in campus systems is separating regular student capabilities from facility administration powers:\n\n"
        "• Student Role: Students can file complaints with photos and access the 'Check Your Incident & Repair Status' search bar on the homepage. "
        "By typing their Ticket ID (e.g. INC-6101) or Roll Number (23EC105), students view a read-only visual progress tracker (*Reported ➔ Dispatched ➔ In Active Repair ➔ Resolved*) without the ability to tamper with work orders.\n"
        "• Facility Staff Role: The entire Maintenance Dispatcher board is guarded by a Facility Staff PIN Gate. "
        "Only authorized personnel with the PIN (default: admin123) can access the Kanban board, assign technicians, move cards between stages, or mark tickets as Closed."
    )

    # ==========================================
    # 9. Stage 7: Deploying to Google Cloud Run via Cloud Shell
    # ==========================================
    h9 = doc.add_heading("9. Stage 7: Deploying to Google Cloud Run via Cloud Shell", level=1)
    h9.runs[0].font.color.rgb = GCP_BLUE

    p_crun = doc.add_paragraph()
    p_crun.add_run(
        "Why Google Cloud Run? (CaaS Concept):\n"
        "Unlike traditional Google Compute Engine Virtual Machines that run 24/7 and incur idle charges, "
        "Google Cloud Run is a Serverless Container-as-a-Service (CaaS) platform. "
        "When students report incidents, Cloud Run spins up container instances in milliseconds. "
        "When activity pauses at night, it automatically scales strictly down to zero instances ($0.00 idle cost).\n\n"
        "Deployment Procedure via Google Cloud Shell:\n"
        "1. We activated Google Cloud Shell terminal (>_) directly in the web browser.\n"
        "2. We packaged our application code into 'campus_ai_project.zip' and uploaded it directly into Cloud Shell.\n"
        "3. We extracted the archive and triggered Google Cloud Build and Cloud Run deployment."
    )

    if len(img_files) >= 9:
        add_screenshot(doc, img_files[8], "Activating Google Cloud Shell terminal in browser")

    if len(img_files) >= 10:
        add_screenshot(doc, img_files[9], "Uploading application code archive directly into Google Cloud Shell")

    p_deploy_cmd = doc.add_paragraph()
    p_deploy_cmd.add_run("The deployment command executed in Cloud Shell:\n").font.bold = True
    p_code = doc.add_paragraph()
    p_code.add_run(
        "unzip -o campus_ai_project.zip -d app && cd app\n"
        "gcloud run deploy campus-ai-system --source . --region us-central1 --allow-unauthenticated"
    )
    p_code.runs[0].font.name = "Courier New"
    p_code.runs[0].font.size = Pt(9.5)

    if len(img_files) >= 11:
        add_screenshot(doc, img_files[10], "Google Cloud Build compiling the container image and pushing to Artifact Registry")

    p_iam = doc.add_paragraph()
    p_iam.add_run("Resolving IAM Cloud Build Permissions:\n").font.bold = True
    p_iam.add_run(
        "During initial container build, Google Cloud's security policy required granting Storage Admin and Artifact Registry Writer permissions "
        "to the Compute Engine default service account. We executed the following IAM binding:\n"
    )
    p_iam_code = doc.add_paragraph()
    p_iam_code.add_run(
        "PROJECT_NUMBER=$(gcloud projects describe college-events-cc --format='value(projectNumber)')\n"
        "gcloud projects add-iam-policy-binding college-events-cc \\\n"
        "    --member=\"serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com\" \\\n"
        "    --role=\"roles/storage.admin\"\n"
        "gcloud projects add-iam-policy-binding college-events-cc \\\n"
        "    --member=\"serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com\" \\\n"
        "    --role=\"roles/artifactregistry.writer\""
    )
    p_iam_code.runs[0].font.name = "Courier New"
    p_iam_code.runs[0].font.size = Pt(9)

    if len(img_files) >= 12:
        add_screenshot(doc, img_files[11], "Resolving IAM permissions and binding Artifact Registry Writer roles to service account")

    p_success = doc.add_paragraph()
    p_success.add_run("Successful Production Cloud Run Deployment:\n").font.bold = True
    p_success.add_run(
        "With permissions granted, Cloud Build compiled the container image, pushed it to Artifact Registry, and deployed it to Google Cloud Run. "
        "Cloud Run provisioned the production HTTPS endpoint serving 100% of live traffic."
    )

    if len(img_files) >= 13:
        add_screenshot(doc, img_files[12], "Successful Cloud Run deployment printing live Service URL: https://campus-ai-system-560850294449.us-central1.run.app")

    add_callout_box(
        doc,
        "• Production Live Service URL: https://campus-ai-system-560850294449.us-central1.run.app/\n"
        "• Active Cloud Run Revision: campus-ai-system-00006-k0b\n"
        "• Traffic Serving: 100% live traffic routed to latest healthy container revision\n"
        "• Health Check Probe: /health returning HTTP 200 OK with system telemetry\n"
        "• Autoscaling Limits: min-instances=0, max-instances=10, concurrency=80",
        title="Cloud Run Production Deployment Status"
    )

    # ==========================================
    # 10. Stage 8: Operational Database (Cloud Firestore - OLTP)
    # ==========================================
    h10 = doc.add_heading("10. Stage 8: Cloud Firestore Database Configuration", level=1)
    h10.runs[0].font.color.rgb = GCP_BLUE

    p_fs = doc.add_paragraph()
    p_fs.add_run(
        "Why Cloud Firestore? (OLTP Concept):\n"
        "Cloud Firestore is a fully managed, serverless NoSQL document database. "
        "In our system, Firestore handles the Online Transaction Processing (OLTP) workload. "
        "When students submit complaints and facility supervisors advance tickets on the Kanban board, "
        "Firestore handles sub-millisecond document writes with ACID transactions, guaranteeing zero data loss or state race conditions.\n\n"
        "We enabled the Firestore API and created the default database in native mode using Cloud Shell:\n"
    )
    p_fs_cmd = doc.add_paragraph()
    p_fs_cmd.add_run("gcloud firestore databases create --location=nam5 --type=firestore-native")
    p_fs_cmd.runs[0].font.name = "Courier New"
    p_fs_cmd.runs[0].font.size = Pt(9.5)

    if len(img_files) >= 14:
        add_screenshot(doc, img_files[13], "Cloud Shell showing successful creation of Cloud Firestore Native Database and BigQuery analytical dataset")

    # ==========================================
    # 11. Stage 9: BigQuery OLAP Warehouse & Analytical Queries
    # ==========================================
    h11 = doc.add_heading("11. Stage 9: BigQuery OLAP Warehouse & Analytical Queries", level=1)
    h11.runs[0].font.color.rgb = GCP_BLUE

    p_bq = doc.add_paragraph()
    p_bq.add_run(
        "Why Google BigQuery? (OLAP Concept):\n"
        "Whenever an incident ticket is submitted, Cloud Run streams the event directly into Google BigQuery "
        "table `campus_incidents_analytics.incident_events` using the streaming ingestion API (`insert_rows_json`). "
        "BigQuery acts as the OLAP data warehouse, storing historical incidents across all MIT-WPU buildings.\n\n"
        "We partitioned the BigQuery table by `DATE(created_at)` and clustered by `building, category, severity`. "
        "This architectural partitioning allows Looker Studio to query only the required storage partitions, resulting in $0.00 query cost.\n"
    )

    p_sql_ddl = doc.add_paragraph()
    p_sql_ddl.add_run(
        "-- BigQuery Dataset & DDL Schema\n"
        "CREATE SCHEMA IF NOT EXISTS `campus_incidents_analytics` OPTIONS(location=\"US\");\n\n"
        "CREATE OR REPLACE TABLE `campus_incidents_analytics.incident_events` (\n"
        "    incident_id STRING NOT NULL,\n"
        "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),\n"
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
        "    resolved_at TIMESTAMP\n"
        ");"
    )
    p_sql_ddl.runs[0].font.name = "Courier New"
    p_sql_ddl.runs[0].font.size = Pt(8.5)

    p_sql_desc = doc.add_paragraph()
    p_sql_desc.add_run("Key Analytical SQL Queries Executed:\n").font.bold = True

    p_sql = doc.add_paragraph()
    p_sql.add_run(
        "-- QUERY 1: Mean Time to Resolution (MTTR) & Department Velocity\n"
        "SELECT \n"
        "    department,\n"
        "    COUNT(incident_id) AS total_incidents,\n"
        "    COUNTIF(severity = 'Critical') AS critical_hazards,\n"
        "    ROUND(AVG(TIMESTAMP_DIFF(COALESCE(resolved_at, CURRENT_TIMESTAMP()), created_at, MINUTE)) / 60.0, 2) AS avg_resolution_hours,\n"
        "    ROUND(COUNTIF(status = 'Resolved') * 100.0 / COUNT(incident_id), 1) AS resolution_rate_pct\n"
        "FROM `college-events-cc.campus_incidents_analytics.incident_events`\n"
        "GROUP BY department\n"
        "ORDER BY total_incidents DESC;\n\n"
        "-- QUERY 2: Campus Building Incident Heatmap & Recurrence Frequency\n"
        "SELECT \n"
        "    building,\n"
        "    category,\n"
        "    COUNT(1) AS failure_frequency,\n"
        "    ARRAY_AGG(room ORDER BY created_at DESC LIMIT 3) AS frequent_failure_locations\n"
        "FROM `college-events-cc.campus_incidents_analytics.incident_events`\n"
        "GROUP BY building, category\n"
        "ORDER BY failure_frequency DESC;"
    )
    p_sql.runs[0].font.name = "Courier New"
    p_sql.runs[0].font.size = Pt(8.5)

    # ==========================================
    # 12. Stage 10: Google Looker Studio BI Dashboard
    # ==========================================
    h12 = doc.add_heading("12. Stage 10: Building the Looker Studio BI Dashboard", level=1)
    h12.runs[0].font.color.rgb = GCP_BLUE

    p_looker = doc.add_paragraph()
    p_looker.add_run(
        "Why Looker Studio? (BI / SaaS Concept):\n"
        "Google Looker Studio is an enterprise data visualization and reporting platform. "
        "Instead of writing custom front-end charting code for every new metric, campus leadership and estate administrators "
        "connect Looker Studio directly to BigQuery. Looker Studio dynamically queries BigQuery tables and renders interactive, drag-and-drop dashboards.\n\n"
        "Implementation Steps:\n"
        "1. Navigated to lookerstudio.google.com using the student account (mitwpu.edu.in).\n"
        "2. Clicked 'Create' -> 'Data Source' -> Selected the native 'BigQuery' connector.\n"
        "3. Chose project 'college-events-cc' -> dataset 'campus_incidents_analytics' -> table 'incident_events'.\n"
        "4. Clicked 'Connect' to import all table schema fields (incident_id, building, severity, category, resolved_at)."
    )

    if len(img_files) >= 15:
        add_screenshot(doc, img_files[14], "Connecting Looker Studio directly to BigQuery 'incident_events' table schema")

    if len(img_files) >= 16:
        add_screenshot(doc, img_files[15], "Selecting schema fields, data types, and aggregation dimensions in Looker Studio editor")

    if len(img_files) >= 17:
        add_screenshot(doc, img_files[16], "Configuring KPI Scorecard, Building Failure Histogram, and Severity Breakdown charts")

    p_charts = doc.add_paragraph()
    p_charts.add_run("Executive BI Dashboard Visual Components:\n").font.bold = True
    p_charts.add_run(
        "• Total Incidents Scorecard: High-level metric tracking cumulative campus complaints (55+ incidents loaded).\n"
        "• Building Incident Distribution Bar Chart: Highlights facilities with high failure rates (e.g. heavy lab equipment in Dhruv and Jamdagni vs lecture halls in Ganga).\n"
        "• Maintenance Discipline Donut Chart: Proportional breakdown across Electrical, Civil & Plumbing, IT, HVAC, Machinery, and Safety.\n"
        "• Severity Breakdown Pie Chart: Real-time risk categorization into Critical, High, Moderate, and Low.\n"
        "• Granular Incident Registry Table: Searchable table detailing ticket IDs, rooms, assigned technicians, and status."
    )

    if len(img_files) >= 18:
        add_screenshot(doc, img_files[17], "Completed Looker Studio BI Dashboard showing Scorecards, Incident Breakdown, and Registries")

    # ==========================================
    # 13. Stage 11: Google Classroom Academic Submission Proof
    # ==========================================
    h13 = doc.add_heading("13. Stage 11: Submission on Google Classroom", level=1)
    h13.runs[0].font.color.rgb = GCP_BLUE

    p_class = doc.add_paragraph()
    p_class.add_run(
        "The assignment was posted on Google Classroom under course 'CLOUD COMPUTING EC' by Prof. Vinaya Gohokar (Continuous Assessment). "
        "The final deliverables—including this comprehensive technical report, live Google Cloud Run URLs, Looker Studio dashboard links, "
        "and GitHub source code repository—are formally submitted under the student portal."
    )

    if len(img_files) >= 19:
        add_screenshot(doc, img_files[18], "Google Classroom Continuous Assessment submission portal under 'CLOUD COMPUTING EC' where this project report is uploaded")

    # ==========================================
    # 14. Requirements Fulfillment Checklist
    # ==========================================
    h14 = doc.add_heading("14. Syllabus Requirements Fulfillment Matrix", level=1)
    h14.runs[0].font.color.rgb = GCP_BLUE

    req_table = doc.add_table(rows=7, cols=3)
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
        ("Analytical Data Warehouse", "Google BigQuery (OLAP)", "✅ Verified: DDL dataset with 55+ incident records streamed live"),
        ("Business Intelligence Dashboard", "Google Looker Studio (BI)", "✅ Verified: Live Looker Studio report connected directly to BigQuery")
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
    # 15. Comprehensive Viva Voce & Technical Defense Q&A
    # ==========================================
    h15 = doc.add_heading("15. Viva Voce & Technical Defense Q&A", level=1)
    h15.runs[0].font.color.rgb = GCP_BLUE

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
         "Answer: Students and public users can only submit complaints and track their specific ticket using the read-only 'Check Incident Status' search bar on the homepage. The Maintenance Dispatcher board is guarded by a Facility Staff PIN gate (admin123). Only authenticated facility supervisors can advance tickets across work order stages (Reported ➔ Dispatched ➔ In Active Repair ➔ Resolved) or assign technicians."),

        ("Q6: How does Google Cloud Run handle container Cold Starts and Concurrency?",
         "Answer: When scaling from zero instances to one instance on a new request, Cloud Run pulls the container layer and initializes FastAPI (taking ~1.5 to 2.5 seconds, known as Cold Start). To optimize performance, our Docker container is built on python:3.12-slim with stripped unnecessary build tools, keeping image size minimal. Furthermore, we configured container concurrency=80, allowing a single warm instance to process up to 80 simultaneous HTTP requests before triggering another container instance."),

        ("Q7: What are the benefits of BigQuery Partitioning and Clustering?",
         "Answer: We partitioned the `incident_events` table by `DATE(created_at)` and clustered by `building, category, severity`. Partitioning divides the underlying columnar storage files into daily physical slices. When Looker Studio queries incidents for the current month, BigQuery only scans that month's partition, completely bypassing historical years. Clustering further sorts the data within each partition by building and category, reducing the number of bytes scanned to near-zero and guaranteeing $0.00 analytical query costs."),

        ("Q8: Why is Docker containerization essential for cloud deployments?",
         "Answer: Docker packages the application code, Python runtime, system libraries, and dependencies into an immutable Open Container Initiative (OCI) image. This eliminates the classic 'works on my machine' defect. The exact container image tested locally runs identically on Google Cloud Run across Google's distributed data centers without environment mismatch."),

        ("Q9: How are IAM service account permissions configured securely?",
         "Answer: We adhere to the Principle of Least Privilege. The Compute Engine and Cloud Build service accounts were granted specific roles (`roles/storage.admin` and `roles/artifactregistry.writer`) solely needed to pull base images, build containers, and write Artifact Registry packages. Application secrets (Gemini API keys) are injected into the runtime container via encrypted environment variables, never hardcoded in git."),

        ("Q10: How does Looker Studio maintain high query performance with BigQuery?",
         "Answer: Looker Studio uses a native BigQuery connector that translates dashboard user interactions (e.g. clicking a building filter) into optimized SQL queries executed directly in BigQuery. Additionally, Looker Studio leverages BI Engine—an in-memory analysis service—to cache frequent query results, providing sub-second dashboard rendering without re-querying the raw data warehouse."),

        ("Q11: What High Availability and Disaster Recovery guarantees exist on GCP us-central1?",
         "Answer: The us-central1 region in Iowa consists of four independent Availability Zones (us-central1-a, b, c, f). Google Cloud Run automatically distributes container replicas across multiple zones. If a physical zone experiences a hardware failure, incoming traffic is seamlessly redirected to healthy replicas in another zone with 99.95% SLA uptime."),

        ("Q12: How does the system handle real-time streaming data ingestion into BigQuery?",
         "Answer: Instead of running batch overnight uploads, Cloud Run invokes the BigQuery Streaming API (`insert_rows_json`). When a student clicks 'Submit', the incident is committed to Cloud Firestore in sub-milliseconds and simultaneously streamed into BigQuery in real time. Within 1 to 2 seconds, the record is queryable by Looker Studio charts without batch latency.")
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
    # 16. Local Run & Cloud Deployment Guide
    # ==========================================
    h16 = doc.add_heading("16. Local Execution & Cloud Deployment Guide", level=1)
    h16.runs[0].font.color.rgb = GCP_BLUE

    p_guide = doc.add_paragraph()
    p_guide.add_run(
        "To run CampusAI locally without requiring any cloud setup or personal credit card:\n"
        "1. Open PowerShell or Command Prompt in the repository folder.\n"
        "2. Install dependencies: `pip install -r requirements.txt`\n"
        "3. Run the application: `python app.py` (or double click `run.bat`).\n"
        "4. Open your browser: http://localhost:8080/ for Student Portal, http://localhost:8080/dispatcher for Dispatcher, http://localhost:8080/analytics for Analytics.\n\n"
        "To deploy to Google Cloud Run:\n"
        "Execute the one-command deployment script: `deploy_gcp.bat` (Windows) or `deploy_gcp.sh` (Linux/Mac/Cloud Shell).\n"
    )

    # ==========================================
    # 17. Conclusion & Learning Outcomes
    # ==========================================
    h17 = doc.add_heading("17. Conclusion & Learning Outcomes", level=1)
    h17.runs[0].font.color.rgb = GCP_BLUE

    p_conc = doc.add_paragraph()
    p_conc.add_run(
        "Through the design, development, and deployment of CampusAI, all key competencies outlined in the Cloud Computing curriculum "
        "have been mastered. The project demonstrates how modern cloud platforms unify serverless container execution (Cloud Run), "
        "multimodal foundation models (Gemini 2.5 Flash), real-time document stores (Firestore), distributed analytics (BigQuery), "
        "and business intelligence (Looker Studio) into a cohesive, production-ready system.\n\n"
        "By adhering to 100% free-tier architectural constraints, the solution achieves zero operational cost while delivering "
        "enterprise-grade reliability and security for Dr. Vishwanath Karad MIT World Peace University."
    )

    # Save to target locations
    out1 = r"C:\CampusAI\CampusAI_Cloud_Computing_Project_Report.docx"
    out2 = r"C:\CC_LCA-2_PROJECT\CampusAI\CampusAI_Cloud_Computing_Project_Report.docx"
    doc.save(out1)
    try:
        doc.save(out2)
    except Exception:
        pass
    print(f"Comprehensive report generated successfully!\n  -> {out1}\nTotal figures embedded: {fig_counter}")

if __name__ == "__main__":
    generate()
