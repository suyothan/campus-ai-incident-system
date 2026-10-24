"""
CampusAI - Multimodal Cloud-Native Infrastructure & Incident Diagnostic System
Google Cloud Stack: Cloud Run (Host) | Cloud Storage (Media) | Vertex AI/Gemini (AI) | Firestore (OLTP) | BigQuery (OLAP) | Looker Studio (BI)
"""

import os
import io
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

from cloud_ai_service import analyze_incident_image
from cloud_database import db_service, analytics_service

app = FastAPI(
    title="CampusAI: Multimodal Facility & Hazard Diagnostic Platform",
    description="Enterprise serverless cloud infrastructure built for Google Cloud Platform",
    version="2.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ==========================================
# Web HTML Routes
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def student_portal(request: Request):
    """Student & Faculty Incident Reporting Portal"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "page_title": "CampusAI - Facility Hazard Reporting Portal"
        }
    )


@app.get("/dispatcher", response_class=HTMLResponse)
async def dispatcher_board(request: Request):
    """Campus Maintenance Dispatcher Kanban Board"""
    incidents = db_service.get_incidents()
    return templates.TemplateResponse(
        request=request,
        name="dispatcher.html",
        context={
            "incidents": incidents,
            "page_title": "Maintenance Dispatcher Board - CampusAI"
        }
    )


@app.get("/analytics", response_class=HTMLResponse)
async def executive_analytics(request: Request):
    """Executive Maintenance & BigQuery Analytics Dashboard"""
    kpis = analytics_service.get_kpi_summary()
    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "kpis": kpis,
            "page_title": "Executive Cloud Analytics & Looker BI - CampusAI"
        }
    )


@app.get("/architecture", response_class=HTMLResponse)
async def architecture_blueprint(request: Request):
    """Interactive GCP System Architecture Blueprint & Technical Design Rationale"""
    return templates.TemplateResponse(
        request=request,
        name="architecture.html",
        context={
            "page_title": "GCP Cloud Architecture Blueprint - CampusAI"
        }
    )


# ==========================================
# REST API Endpoints
# ==========================================

@app.post("/api/incidents/report")
async def report_incident(
    student_name: str = Form(...),
    roll_no: str = Form(...),
    email: str = Form(...),
    building: str = Form(...),
    room: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    department: Optional[str] = Form("Electronics & Communication"),
    other_building: Optional[str] = Form(None),
    user_category: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Ingests photo and report into Cloud Storage pipeline, triggers Vertex AI / Gemini vision triage,
    and commits verified incident document into Cloud Firestore.
    """
    image_bytes = None
    saved_filename = "incident_placeholder.jpg"

    # Resolve custom building name if 'Other' was selected
    actual_building = other_building.strip() if (building == "Other" and other_building and other_building.strip()) else building

    if image and image.filename:
        image_bytes = await image.read()
        saved_filename = f"img_{int(os.times().elapsed * 1000)}_{image.filename}"
        save_path = os.path.join(UPLOADS_DIR, saved_filename)
        with open(save_path, "wb") as f:
            f.write(image_bytes)

    # 1. Run Multimodal Cloud AI Assessment
    ai_result = analyze_incident_image(
        image_bytes=image_bytes,
        image_filename=saved_filename,
        description=description,
        building=actual_building,
        room=room,
        user_category=user_category
    )

    # 2. Commit to Firestore database
    payload = {
        "student_name": student_name,
        "roll_no": roll_no,
        "email": email,
        "department": department or "Electronics & Communication",
        "building": actual_building,
        "room": room,
        "title": title,
        "description": description,
        "image_filename": saved_filename
    }
    incident = db_service.create_incident(payload, ai_result)

    return {
        "success": True,
        "message": "Incident analyzed and dispatched successfully by CampusAI!",
        "incident": incident
    }


@app.get("/api/incidents")
async def get_incidents(
    status: Optional[str] = None,
    category: Optional[str] = None,
    building: Optional[str] = None,
    search: Optional[str] = None
):
    """Retrieve filtered incident tickets from Firestore"""
    return db_service.get_incidents(status=status, category=category, building=building, search=search)


@app.patch("/api/incidents/{incident_id}/status")
async def update_status(incident_id: str, request: Request):
    """Updates incident status on the maintenance Kanban board"""
    data = await request.json()
    new_status = data.get("status")
    technician = data.get("technician")
    if not new_status:
        raise HTTPException(status_code=400, detail="Missing status parameter")

    updated = db_service.update_incident_status(incident_id, new_status, technician)
    if not updated:
        raise HTTPException(status_code=404, detail="Incident not found")

    return {"success": True, "incident": updated}


@app.get("/api/analytics/summary")
async def get_analytics_summary():
    """BigQuery OLAP summary metrics for executive dashboard"""
    return analytics_service.get_kpi_summary()


@app.get("/api/analytics/trends")
async def get_analytics_trends():
    """BigQuery time-series trend metrics"""
    return analytics_service.get_time_series_trends()


@app.get("/api/export/csv")
async def export_csv():
    """Exports BigQuery-compatible incident dataset as CSV"""
    csv_data = analytics_service.export_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=campus_incidents_bigquery.csv"}
    )


@app.get("/api/sync-bigquery")
@app.post("/api/sync-bigquery")
async def sync_bigquery():
    """Sync all operational incidents into Google BigQuery warehouse"""
    count = db_service.sync_all_to_bigquery()
    return {"success": True, "synced_incidents": count, "message": f"Successfully synced {count} incidents to BigQuery"}


@app.get("/health")
async def health_check():
    """Google Cloud Run container health check probe"""
    return {
        "status": "healthy",
        "service": "campus-ai-diagnostic-engine",
        "cloud_provider": "Google Cloud Platform",
        "architecture_tier": {
            "compute": "Google Cloud Run (Serverless CaaS)",
            "object_storage": "Google Cloud Storage (GCS Buckets)",
            "ai_engine": "Google Vertex AI / Gemini Vision",
            "operational_db": "Cloud Firestore (OLTP)",
            "data_warehouse": "Google BigQuery (OLAP)",
            "bi_reporting": "Google Looker Studio"
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    print("\n=======================================================")
    print("  CampusAI - Multimodal Facility & Hazard Diagnostics")
    print(f"  Google Cloud Run Server active at: http://localhost:{port}")
    print("=======================================================\n")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
