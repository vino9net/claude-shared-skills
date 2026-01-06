---
name: google-cloud-platform
description: Work with Google Cloud Platform services and resources. Use when deploying to GCP, managing cloud resources, or interacting with GCP APIs.
allowed-tools: Bash(gcloud*), Bash(gsutil*), Read, Grep, mcp__gcloud__run_gcloud_command
---

# Google Cloud Platform Skills

This skill provides guidance for working with Google Cloud Platform (GCP) services, resources, and deployments.

## Available Sub-Skills

This skill includes specialized sub-skills for specific GCP services:

- **cloud_run**: Operations for Google Cloud Run (jobs and services)
- **compute_engine**: Operations for Google Compute Engine (VMs)

These sub-skills provide detailed instructions and best practices for each service.

## MCP Server Installation

This skill works best with the **Google Cloud MCP server**. To install and configure it:

### Installation

The Google Cloud MCP server is available via npm and can be configured in your Claude Code settings.

Add the following configuration to your `.mcp.json` file in your home directory (`~/.mcp.json`) or project directory:

```json
{
  "mcpServers": {
    "gcloud": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gcp"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "${GOOGLE_APPLICATION_CREDENTIALS}",
        "GOOGLE_CLOUD_PROJECT": "${GOOGLE_CLOUD_PROJECT}"
      }
    }
  }
}
```

### Environment Variables

Make sure the following environment variables are set in your shell:

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your service account JSON key file
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID

You can set these in your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/your-service-account-key.json"
```

### Verification

After configuration, restart Claude Code. The MCP server should automatically connect and provide the `mcp__gcloud__run_gcloud_command` tool for programmatic access to GCP resources.

## Core Services

### Cloud Run
- Deploy containerized applications
- Manage services and revisions
- Configure scaling and traffic

### Cloud Storage
- Manage buckets and objects
- Handle file uploads/downloads
- Configure access controls

### Cloud Functions
- Deploy serverless functions
- Manage triggers and configurations
- Monitor logs and metrics

## Project Configuration

### Detecting Project Settings

Check `CLAUDE.md` for project-specific GCP configuration:
- GCP Project ID
- Default region/zone
- Service account details
- Environment (dev/staging/prod)

### Environment Variables

GCP configuration may be stored in:
- `.env` file (project secrets - do not commit)
- `.claude/settings.json` (project configuration)
- Environment variables set in shell

Common variables:
- `GCP_PROJECT_ID` or `GOOGLE_CLOUD_PROJECT`
- `GCP_REGION` or `GOOGLE_CLOUD_REGION`
- `GOOGLE_APPLICATION_CREDENTIALS`

## Tools and Commands

### gcloud CLI

**Authentication:**
```bash
gcloud auth login
gcloud auth application-default login
```

**Project Configuration:**
```bash
# Set active project
gcloud config set project PROJECT_ID

# Get current project
gcloud config get-value project

# List projects
gcloud projects list
```

**Cloud Run:**
```bash
# Deploy service
gcloud run deploy SERVICE_NAME \
  --image IMAGE_URL \
  --region REGION \
  --platform managed

# List services
gcloud run services list

# Get service details
gcloud run services describe SERVICE_NAME --region REGION

# Update traffic
gcloud run services update-traffic SERVICE_NAME \
  --to-revisions REVISION=PERCENT \
  --region REGION
```

**Cloud Storage:**
```bash
# List buckets
gcloud storage buckets list

# Create bucket
gcloud storage buckets create gs://BUCKET_NAME --location=REGION

# List objects
gcloud storage ls gs://BUCKET_NAME/

# Copy files
gcloud storage cp LOCAL_FILE gs://BUCKET_NAME/
gcloud storage cp gs://BUCKET_NAME/FILE LOCAL_FILE
```

### gsutil (Legacy Storage Tool)

```bash
# List buckets
gsutil ls

# Copy files
gsutil cp LOCAL_FILE gs://BUCKET_NAME/
gsutil cp -r gs://BUCKET_NAME/* LOCAL_DIR/

# Set permissions
gsutil iam ch USER:ROLE gs://BUCKET_NAME
```

### MCP Server for GCloud

See the [MCP Server Installation](#mcp-server-installation) section at the top of this document for setup instructions.

The MCP server provides the `mcp__gcloud__run_gcloud_command` tool for:
- Running gcloud commands programmatically
- Querying GCP resources
- Managing deployments

## Common Workflows

### Deploying to Cloud Run

1. **Check project configuration:**
   - Read `CLAUDE.md` for GCP project ID and region
   - Verify authentication: `gcloud auth list`
   - Set project: `gcloud config set project PROJECT_ID`

2. **Build container (if needed):**
   ```bash
   docker build -t IMAGE_NAME .
   docker tag IMAGE_NAME gcr.io/PROJECT_ID/IMAGE_NAME
   docker push gcr.io/PROJECT_ID/IMAGE_NAME
   ```

3. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy SERVICE_NAME \
     --image gcr.io/PROJECT_ID/IMAGE_NAME \
     --region REGION \
     --platform managed \
     --allow-unauthenticated
   ```

4. **Verify deployment:**
   ```bash
   gcloud run services describe SERVICE_NAME --region REGION
   ```

### Managing Cloud Storage

1. **Check project and bucket configuration in CLAUDE.md**

2. **Create bucket (if needed):**
   ```bash
   gcloud storage buckets create gs://BUCKET_NAME --location=REGION
   ```

3. **Upload files:**
   ```bash
   gcloud storage cp FILE gs://BUCKET_NAME/PATH/
   ```

4. **Set public access (if needed):**
   ```bash
   gcloud storage buckets add-iam-policy-binding gs://BUCKET_NAME \
     --member=allUsers \
     --role=roles/storage.objectViewer
   ```

### Checking Logs

```bash
# Cloud Run logs
gcloud run services logs read SERVICE_NAME --region REGION

# Cloud Functions logs
gcloud functions logs read FUNCTION_NAME

# General logs
gcloud logging read "resource.type=cloud_run_revision"
```

## Security Best Practices

### Service Accounts
- Use service accounts for application authentication
- Never commit service account keys to git
- Store credentials in `.env` (gitignored)
- Reference via `GOOGLE_APPLICATION_CREDENTIALS` env var

### IAM and Permissions
- Follow principle of least privilege
- Use predefined roles when possible
- Audit permissions regularly

### Secrets Management
- Use Secret Manager for sensitive data
- Never hardcode credentials
- Use environment variables or Secret Manager

## Environment-Specific Configuration

### Development
- Use separate GCP project for dev
- Lower resource limits
- Public access for testing (if safe)

### Staging
- Mirror production configuration
- Use staging-specific service accounts
- Test deployments before production

### Production
- Strict access controls
- Enable monitoring and alerting
- Use CI/CD for deployments
- No direct manual deployments

## Integration with Project Settings

### Reading from CLAUDE.md

Example project configuration:
```markdown
## GCP Configuration
- Project ID: my-project-prod
- Default region: us-central1
- Cloud Run service: my-service
- Storage bucket: my-project-data
```

Use these values when running gcloud commands.

### Reading from .env

```bash
# Load environment variables
source .env

# Or read specific variables
GCP_PROJECT_ID=$(grep GCP_PROJECT_ID .env | cut -d'=' -f2)
```

## Troubleshooting

### Authentication Issues
```bash
# Re-authenticate
gcloud auth login
gcloud auth application-default login

# Check current auth
gcloud auth list
```

### Project Not Set
```bash
# Check current project
gcloud config get-value project

# Set project
gcloud config set project PROJECT_ID
```

### Permission Denied
- Verify service account has required roles
- Check IAM policies
- Ensure project billing is enabled

### Deployment Failures
- Check service logs: `gcloud run services logs read SERVICE_NAME`
- Verify image exists and is accessible
- Check region and project settings
- Ensure quotas are not exceeded

## Additional Resources

When working with GCP:
- Check official GCP documentation for detailed API reference
- Use `gcloud --help` for command syntax
- Review CLAUDE.md for project-specific GCP configuration
- Consult .env for environment-specific settings

## Remember

- ✅ Always check CLAUDE.md for project GCP settings
- ✅ Verify authentication before running commands
- ✅ Use environment-specific projects (dev/staging/prod)
- ❌ Never commit service account keys or credentials
- ✅ Use Secret Manager for sensitive data
- ✅ Test in dev/staging before deploying to production
- ✅ Monitor logs and metrics after deployments
