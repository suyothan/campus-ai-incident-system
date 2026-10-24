# CampusAI: Multimodal Cloud-Native Infrastructure & Incident Diagnostic System
### Enterprise Serverless Cloud Architecture on Google Cloud Platform (GCP)

[![Google Cloud Run](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Google Cloud Storage](https://img.shields.io/badge/Google%20Cloud-Storage-009688?logo=googlecloud&logoColor=white)](https://cloud.google.com/storage)
[![Google Vertex AI](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-9C27B0?logo=googlecloud&logoColor=white)](https://cloud.google.com/vertex-ai)
[![Google Cloud Firestore](https://img.shields.io/badge/Google%20Cloud-Firestore-FFA611?logo=firebase&logoColor=white)](https://cloud.google.com/firestore)
[![Google BigQuery](https://img.shields.io/badge/Google%20Cloud-BigQuery-669DF6?logo=googlecloud&logoColor=white)](https://cloud.google.com/bigquery)
[![Google Looker Studio](https://img.shields.io/badge/Google-Looker%20Studio-EA4335?logo=looker&logoColor=white)](https://lookerstudio.google.com)

---

## 📌 Project Abstract
**CampusAI** is an enterprise-grade cloud facility management and hazard triage platform built specifically for **MIT World Peace University (MIT-WPU), Pune**. 
It empowers students and faculty to report damaged amenities (exposed electrical cables, pipe ruptures, structural leaks, lab hardware faults) via photo evidence. 

The application integrates **Google Gemini 2.5 Flash / Vertex AI Multimodal Vision** to inspect photographic evidence in real-time, extract OSHA-compliant hazard severity scores, auto-classify campus department ownership, and instantly dispatch structured work orders to on-call campus technicians across MIT-WPU buildings (*Dhruv, Jamdagni, Maitreyi, Chanakya, Vyasa, Vivekananda, Ganga, Gargi, Vasisht*).

---

## 👤 Project Author
- **Author**: Suyothan Vijayapandi
- **Roll No**: 23EC105
- **Department**: School of Electronics & Communication Engineering (ECE)
- **Institution**: Dr. Vishwanath Karad MIT World Peace University (MIT-WPU), Pune
- **Course**: Cloud Computing (CC) — Prof. Vinaya Gohokar

---

## 🏗️ 6-Service Google Cloud Architecture

```
+-------------------------------------------------------------------------+
|                              CLIENT TIER                                |
|   Students (Photo Incident Report)      Maintenance (Live Kanban Board) |
+-------------------------------------------------------------------------+
                                     │
                                     ▼ HTTPS
+-------------------------------------------------------------------------+
|                  GOOGLE CLOUD RUN (Serverless CaaS)                     |
|                 FastAPI Application (Port 8080)                         |
|             Autoscaling (0 to N instances) • Stateless                  |
+-------------------------------------------------------------------------+
       │                                     │
       ▼ (Raw Evidence Upload)               ▼ (Multimodal Image Triage)
+--------------------------------+   +------------------------------------+
|  CLOUD STORAGE (GCS Bucket)    |   |     VERTEX AI / GEMINI VISION      |
|  Blob Ingestion & Signed URLs  |   |  Hazard Scoring & Diagnostic JSON  |
+--------------------------------+   +------------------------------------+
                                                     │
                                                     ▼ (Verified Work Order)
                                     +------------------------------------+
                                     |      CLOUD FIRESTORE (NoSQL)       |
                                     | Real-time Transactional Store      |
                                     | Ticket Status: Reported -> Closed  |
                                     +------------------------------------+
                                                     │
                                                     ▼ (Streaming Pipeline)
                                     +------------------------------------+
                                     |       GOOGLE BIGQUERY (OLAP)       |
                                     | Petabyte-Scale Data Warehouse      |
                                     | Mean Time to Resolution (MTTR) SQL |
                                     +------------------------------------+
                                                     │
                                                     ▼ Direct Connector
                                     +------------------------------------+
                                     |        GOOGLE LOOKER STUDIO        |
                                     | Executive Maintenance BI Dashboard |
                                     +------------------------------------+
```

---

## 🚀 Key Modules & Portals
1. **Student Incident Reporter (`/`)**:
   - Photo evidence upload with drag-and-drop (WebP, PNG, JPG).
   - Real-time campus building selector with interactive custom location expansion.
   - Instant Multimodal AI Diagnostic Work Order modal powered by **Google Gemini 2.5 Flash**.
2. **Maintenance Dispatcher Kanban (`/dispatcher`)**:
   - Real-time work order triage board: *Reported ➔ Dispatched ➔ In Repair ➔ Resolved*.
   - Filterable by Category, Severity, and Campus Building.
3. **Executive Analytics Dashboard (`/analytics`)**:
   - BigQuery KPI summary cards (Total Incidents, Critical Safety Hazards, In Progress, Resolution Rate %, MTTR).
   - Real-time resolution curves, department breakdowns, and building hazard density charts.
   - BigQuery CSV export.
4. **Cloud Architecture Blueprint (`/architecture`)**:
   - Interactive system blueprint explaining the 6-service GCP pipeline and architectural trade-offs.

---

## 🎨 UI/UX Design System
Styled according to the **ElevenLabs Editorial Design System** (`DESIGN.md`):
- **Typography**: EB Garamond display serif paired with Inter and JetBrains Mono.
- **Color Palette**: Light Mode default (#f6f6f5 off-white canvas with #0c0a09 near-black ink) + Dark Mode toggle.
- **Atmosphere**: Subtle pastel ambient blooms (mint, peach, lavender).

---

## ☁️ Google Cloud Deployment Guide (Google Cloud Shell)

### Step 1: Clone Repository in Cloud Shell
```bash
git clone https://github.com/suyothan/campus-ai-incident-system.git
cd campus-ai-incident-system
```

### Step 2: Set Environment Variables & Deploy to Cloud Run
```bash
# 1. Set Google Cloud project
gcloud config set project college-events-cc

# 2. Deploy serverless container to Cloud Run
gcloud run deploy campus-ai-system \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GEMINI_API_KEY=YOUR_GEMINI_API_KEY,GCP_PROJECT_ID=college-events-cc"
```

### Step 3: Initialize BigQuery Schema (One-Time)
```bash
bq mk --dataset college-events-cc:campus_ai_analytics
bq query --use_legacy_sql=false < bigquery_schema.sql
```

---

## 💻 Local Execution (Windows)
1. Double-click `run.bat` or run:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
2. Open `http://localhost:8080` in your web browser.
