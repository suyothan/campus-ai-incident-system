@echo off
REM ===================================================================
REM Google Cloud Run Deployment Script - CampusAI (Windows)
REM ===================================================================
echo =======================================================
echo Deploying CampusAI Platform to Google Cloud Run
echo =======================================================

set PROJECT_ID=college-events-cc
set SERVICE_NAME=campus-ai-system
set REGION=us-central1

echo [1/3] Setting GCP project to %PROJECT_ID%...
call gcloud config set project %PROJECT_ID%

echo [2/3] Building and deploying container to Google Cloud Run...
call gcloud run deploy %SERVICE_NAME% ^
    --source . ^
    --region %REGION% ^
    --platform managed ^
    --allow-unauthenticated ^
    --set-env-vars GCP_PROJECT_ID=%PROJECT_ID%

echo [3/3] Deployment complete!
echo Live Service URL printed above.
pause
