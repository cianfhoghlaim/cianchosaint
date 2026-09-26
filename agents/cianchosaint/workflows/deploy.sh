#!/usr/bin/env bash
# CIANCHOSAINT — canonical Cloud Run deployment script.
#
# Per `openspec/changes/cianchosaint-3am-workflow-v1/specs/cianchosaint-3am-workflow/spec.md`.
#
# Wholesale-adapted from cianfhoghlaim's `monstertix/deploy-agent.sh`.
#
# Per cianfhoghlaim's pattern:
# - Builds the Docker image from the repo root
# - Deploys to Cloud Run with the canonical `gcr.io/$PROJECT/cianchosaint-agent:latest`
# - Registers a Cloud Scheduler job that POSTs `/wake` daily at 3am
#
# Usage:
#   PROJECT=cianchosaint-prod REGION=us-central1 bash agents/cianchosaint/workflows/deploy.sh
#   PROJECT=cianchosaint-prod bash agents/cianchosaint/workflows/deploy.sh destroy

set -euo pipefail

PROJECT="${PROJECT:-cianchosaint-dev}"
REGION="${REGION:-us-central1}"
IMAGE="gcr.io/${PROJECT}/cianchosaint-agent:latest"
SERVICE="cianchosaint-agent"
SCHEDULER_JOB="cianchosaint-3am-wake"
SCHEDULER_SCHEDULE="0 3 * * *"  # Daily at 3am UTC

case "${1:-deploy}" in
    deploy)
        echo "==> Building + deploying $SERVICE to $REGION"

        # 1. Build the Docker image (canonical Dockerfile)
        echo "    Building image..."
        gcloud builds submit --tag "$IMAGE" .

        # 2. Deploy to Cloud Run
        echo "    Deploying to Cloud Run..."
        gcloud run deploy "$SERVICE" \
            --image "$IMAGE" \
            --platform managed \
            --region "$REGION" \
            --no-allow-unauthenticated \
            --set-env-vars="CIANCHOSAINT_DEPLOYED=true,CIANCHOSAINT_REGION=$REGION"

        # 3. Register the Cloud Scheduler job (3am daily wake)
        echo "    Registering Cloud Scheduler job..."
        SERVICE_URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)')"
        gcloud scheduler jobs create http "$SCHEDULER_JOB" \
            --location "$REGION" \
            --schedule "$SCHEDULER_SCHEDULE" \
            --uri "${SERVICE_URL}/wake" \
            --http-method POST \
            --message-body '{"workflow_id": "politician_resolver_3am"}' \
            --time-zone "Etc/UTC" \
            --attempt-deadline 600s \
            || gcloud scheduler jobs update http "$SCHEDULER_JOB" \
                --location "$REGION" \
                --schedule "$SCHEDULER_SCHEDULE" \
                --uri "${SERVICE_URL}/wake" \
                --http-method POST \
                --message-body '{"workflow_id": "politician_resolver_3am"}' \
                --time-zone "Etc/UTC" \
                --attempt-deadline 600s

        echo "==> Done. Service URL: $SERVICE_URL"
        echo "    Scheduler: $SCHEDULER_JOB at $SCHEDULER_SCHEDULE UTC"
        ;;

    destroy)
        echo "==> Destroying $SERVICE + $SCHEDULER_JOB"
        gcloud scheduler jobs delete "$SCHEDULER_JOB" --location "$REGION" --quiet || true
        gcloud run services delete "$SERVICE" --region "$REGION" --quiet || true
        gcloud container images delete "$IMAGE" --quiet || true
        echo "==> Done."
        ;;

    *)
        echo "Usage: bash deploy.sh [deploy|destroy]"
        exit 1
        ;;
esac
