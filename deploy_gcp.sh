#!/usr/bin/env bash
# ===================================================================
# Google Cloud Run Deployment Script - CampusAI (Linux / Cloud Shell)
# ===================================================================
set -e

PROJECT_ID=${GCP_PROJECT_ID:-"college-events-cc"}
SERVICE_NAME="campus-ai-system"
REGION="us-central1"

echo "======================================================="
echo "Deploying CampusAI to Google Cloud Run: ${SERVICE_NAME}"
echo "Project: ${PROJECT_ID} | Region: ${REGION}"
echo "======================================================="

gcloud config set project "${PROJECT_ID}"

GEMINI_KEY=${GEMINI_API_KEY:-""}

gcloud run deploy "${SERVICE_NAME}" \
    --source . \
    --region "${REGION}" \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars GCP_PROJECT_ID="${PROJECT_ID}",GEMINI_API_KEY="${GEMINI_KEY}"

echo "Deployment complete! Live Cloud Run URL printed above."
