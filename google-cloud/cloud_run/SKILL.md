---
name: google-cloud-run
description: Work with Google Cloud Run jobs and services. Use for deploying containerized applications, managing Cloud Run services and jobs, or executing batch workloads.
allowed-tools: Bash(gcloud*), Read, Grep, mcp__gcloud__run_gcloud_command
---

# Google Cloud Run Operations

This skill provides instructions for working with Google Cloud Run jobs and services.

## Overview

Cloud Run supports two types of workloads:
- **Services**: Long-running HTTP services that scale to zero
- **Jobs**: One-off or scheduled tasks that run to completion

## Prerequisites

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Set default region (optional)
gcloud config set run/region us-central1
```

## Cloud Run Jobs

### Starting a Cloud Run Job

To execute a Cloud Run job:

```bash
# Execute a job (creates a new execution)
gcloud run jobs execute JOB_NAME \
  --region=REGION

# Execute a job with overrides
gcloud run jobs execute JOB_NAME \
  --region=REGION \
  --tasks=5 \
  --max-retries=3 \
  --task-timeout=30m

# Execute a job and wait for completion
gcloud run jobs execute JOB_NAME \
  --region=REGION \
  --wait

# Execute a job with environment variables
gcloud run jobs execute JOB_NAME \
  --region=REGION \
  --update-env-vars=KEY1=value1,KEY2=value2
```

### Monitoring Job Executions

```bash
# List job executions
gcloud run jobs executions list \
  --job=JOB_NAME \
  --region=REGION

# Get execution status
gcloud run jobs executions describe EXECUTION_NAME \
  --region=REGION

# Stream logs from a job execution
gcloud run jobs executions logs read EXECUTION_NAME \
  --region=REGION

# Follow logs in real-time
gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=JOB_NAME" \
  --project=PROJECT_ID \
  --limit=50 \
  --format=json
```

### Managing Cloud Run Jobs

```bash
# List all jobs
gcloud run jobs list --region=REGION

# Describe a job
gcloud run jobs describe JOB_NAME --region=REGION

# Update a job
gcloud run jobs update JOB_NAME \
  --region=REGION \
  --image=IMAGE_URL \
  --tasks=10 \
  --max-retries=5

# Delete a job
gcloud run jobs delete JOB_NAME --region=REGION
```

### Creating a New Cloud Run Job

```bash
# Create a job from a container image
gcloud run jobs create JOB_NAME \
  --image=IMAGE_URL \
  --region=REGION \
  --tasks=1 \
  --max-retries=3 \
  --task-timeout=10m \
  --cpu=1 \
  --memory=512Mi \
  --service-account=SERVICE_ACCOUNT_EMAIL

# Create a job with environment variables
gcloud run jobs create JOB_NAME \
  --image=IMAGE_URL \
  --region=REGION \
  --set-env-vars=KEY1=value1,KEY2=value2

# Create a job with secrets
gcloud run jobs create JOB_NAME \
  --image=IMAGE_URL \
  --region=REGION \
  --set-secrets=SECRET_NAME=SECRET_NAME:latest
```

## Cloud Run Services

### Deploying Services

```bash
# Deploy a service
gcloud run deploy SERVICE_NAME \
  --image=IMAGE_URL \
  --region=REGION \
  --platform=managed \
  --allow-unauthenticated

# Deploy with specific configuration
gcloud run deploy SERVICE_NAME \
  --image=IMAGE_URL \
  --region=REGION \
  --cpu=2 \
  --memory=1Gi \
  --min-instances=0 \
  --max-instances=10 \
  --concurrency=80 \
  --timeout=300s
```

### Managing Services

```bash
# List services
gcloud run services list --region=REGION

# Describe a service
gcloud run services describe SERVICE_NAME --region=REGION

# Delete a service
gcloud run services delete SERVICE_NAME --region=REGION

# Get service URL
gcloud run services describe SERVICE_NAME \
  --region=REGION \
  --format='value(status.url)'
```

## Common Patterns

### Execute Job and Wait for Results

```bash
#!/bin/bash
set -e

JOB_NAME="my-job"
REGION="us-central1"

echo "Starting job execution..."
EXECUTION_NAME=$(gcloud run jobs execute $JOB_NAME \
  --region=$REGION \
  --format='value(metadata.name)')

echo "Execution: $EXECUTION_NAME"

# Wait for completion
echo "Waiting for job to complete..."
gcloud run jobs executions wait $EXECUTION_NAME \
  --region=$REGION

# Check final status
STATUS=$(gcloud run jobs executions describe $EXECUTION_NAME \
  --region=$REGION \
  --format='value(status.conditions[0].type)')

if [ "$STATUS" = "Completed" ]; then
  echo "Job completed successfully!"
  exit 0
else
  echo "Job failed!"
  exit 1
fi
```

### Execute Job with Parameters

```bash
# Execute job with custom environment variables
gcloud run jobs execute my-processing-job \
  --region=us-central1 \
  --update-env-vars=INPUT_FILE=gs://bucket/file.csv,BATCH_SIZE=1000 \
  --wait
```

## Environment Variables

Common environment variables used by Cloud Run:

- `CLOUD_RUN_JOB`: Name of the Cloud Run job (auto-set)
- `CLOUD_RUN_EXECUTION`: Execution name (auto-set)
- `CLOUD_RUN_TASK_INDEX`: Task index for parallel jobs (auto-set)
- `CLOUD_RUN_TASK_COUNT`: Total number of tasks (auto-set)

## IAM Permissions

Required IAM roles:

- `roles/run.admin`: Full access to Cloud Run resources
- `roles/run.developer`: Deploy and manage services/jobs
- `roles/run.invoker`: Execute jobs and invoke services

## Tips

1. **Use `--wait` flag**: When executing jobs interactively, use `--wait` to see the result
2. **Task parallelism**: For batch processing, use `--tasks` to run multiple parallel tasks
3. **Retry logic**: Set `--max-retries` appropriately for fault-tolerant jobs
4. **Timeouts**: Set realistic `--task-timeout` values to avoid premature termination
5. **Monitoring**: Use Cloud Logging and Cloud Monitoring to track job performance
6. **Service accounts**: Always use dedicated service accounts with minimal permissions

## Troubleshooting

```bash
# View recent logs
gcloud logging read "resource.type=cloud_run_job" \
  --limit=100 \
  --format=json

# Check job configuration
gcloud run jobs describe JOB_NAME \
  --region=REGION \
  --format=yaml

# List failed executions
gcloud run jobs executions list \
  --job=JOB_NAME \
  --region=REGION \
  --filter="status.conditions.type:Failed"
```
