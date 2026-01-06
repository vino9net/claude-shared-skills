---
name: google-compute-engine
description: Work with Google Compute Engine VMs. Use for managing VM instances, starting/stopping VMs, SSH access, and VM configuration.
allowed-tools: Bash(gcloud*), Read, Edit, Grep, mcp__gcloud__run_gcloud_command
---

# Google Compute Engine Operations

This skill provides instructions for working with Google Compute Engine (GCE) VMs.

## Prerequisites

```bash
# Enable Compute Engine API
gcloud services enable compute.googleapis.com

# Set default zone (optional)
gcloud config set compute/zone us-central1-a
gcloud config set compute/region us-central1
```

## VM Instance Management

### Listing VMs

```bash
# List all VMs in the project
gcloud compute instances list

# List VMs in a specific zone
gcloud compute instances list --zones=us-central1-a

# List VMs with specific fields
gcloud compute instances list \
  --format="table(name,zone,machineType,status,EXTERNAL_IP)"
```

### Starting a VM

**IMPORTANT**: When starting a VM, you MUST update the `~/.ssh/config` file with the VM's public IP address.

```bash
#!/bin/bash
# Start a VM and update SSH config

VM_NAME="your-vm-name"
ZONE="us-central1-a"

# Start the VM
echo "Starting VM: $VM_NAME"
gcloud compute instances start $VM_NAME --zone=$ZONE

# Wait for VM to be running
echo "Waiting for VM to start..."
gcloud compute instances describe $VM_NAME \
  --zone=$ZONE \
  --format="value(status)" | grep -q "RUNNING"

# Get the external IP address
EXTERNAL_IP=$(gcloud compute instances describe $VM_NAME \
  --zone=$ZONE \
  --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

echo "VM started with IP: $EXTERNAL_IP"

# Update ~/.ssh/config (only if entry exists)
echo "Updating ~/.ssh/config..."

# Check if entry exists
if grep -q "^Host $VM_NAME\$" ~/.ssh/config; then
  # Create backup of SSH config
  cp ~/.ssh/config ~/.ssh/config.backup

  # Update existing entry's HostName
  sed -i.bak "/^Host $VM_NAME\$/,/^Host / { s/^  HostName .*/  HostName $EXTERNAL_IP/; }" ~/.ssh/config

  echo "SSH config updated. You can now connect with: ssh $VM_NAME"
else
  echo "Warning: No SSH config entry found for $VM_NAME"
  echo "Please add this entry to ~/.ssh/config manually:"
  echo ""
  echo "Host $VM_NAME"
  echo "  HostName $EXTERNAL_IP"
  echo "  User YOUR_USERNAME"
  echo "  StrictHostKeyChecking accept-new"
  echo "  UserKnownHostsFile ~/.ssh/known_hosts"
fi
```

### Stopping a VM

```bash
# Stop a VM
gcloud compute instances stop VM_NAME --zone=ZONE

# Stop multiple VMs
gcloud compute instances stop VM1 VM2 VM3 --zone=ZONE
```

### Creating a New VM

```bash
# Create a basic VM
gcloud compute instances create VM_NAME \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=10GB \
  --boot-disk-type=pd-standard

# Create a VM with custom configuration
gcloud compute instances create VM_NAME \
  --zone=us-central1-a \
  --machine-type=n2-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --boot-disk-type=pd-ssd \
  --network-tier=PREMIUM \
  --metadata=enable-oslogin=true \
  --scopes=cloud-platform

# Create a spot/preemptible VM (cheaper)
gcloud compute instances create VM_NAME \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --preemptible \
  --image-family=debian-11 \
  --image-project=debian-cloud
```

### Describing a VM

```bash
# Get VM details
gcloud compute instances describe VM_NAME --zone=ZONE

# Get specific information
# Get external IP
gcloud compute instances describe VM_NAME \
  --zone=ZONE \
  --format="get(networkInterfaces[0].accessConfigs[0].natIP)"

# Get machine type
gcloud compute instances describe VM_NAME \
  --zone=ZONE \
  --format="get(machineType)"

# Get status
gcloud compute instances describe VM_NAME \
  --zone=ZONE \
  --format="get(status)"
```

### Deleting a VM

```bash
# Delete a VM
gcloud compute instances delete VM_NAME \
  --zone=ZONE \
  --quiet

# Delete a VM and keep the boot disk
gcloud compute instances delete VM_NAME \
  --zone=ZONE \
  --keep-disks=boot \
  --quiet
```

## SSH Access

### SSH Config Format

**IMPORTANT**: VM start scripts will only UPDATE existing SSH config entries. You must manually create the initial entry in `~/.ssh/config` for each VM using this format:

```
Host <vm_name>
  HostName <vm_ipv4_address>
  User <your_username>
  StrictHostKeyChecking accept-new
  UserKnownHostsFile ~/.ssh/known_hosts
```

Example:
```
Host my-dev-vm
  HostName 34.123.45.67
  User myuser
  StrictHostKeyChecking accept-new
  UserKnownHostsFile ~/.ssh/known_hosts
```

When you start a VM, the automation scripts will automatically update the `HostName` field with the new IP address, but they will NOT create new entries.

### Connecting to a VM

```bash
# SSH using gcloud (automatically manages keys)
gcloud compute ssh VM_NAME --zone=ZONE

# SSH with custom user
gcloud compute ssh USER@VM_NAME --zone=ZONE

# SSH and run a command
gcloud compute ssh VM_NAME \
  --zone=ZONE \
  --command="sudo apt-get update && sudo apt-get upgrade -y"

# SSH using native ssh (after updating ~/.ssh/config)
ssh VM_NAME
```

### Copying Files

```bash
# Copy file to VM
gcloud compute scp LOCAL_FILE VM_NAME:REMOTE_PATH --zone=ZONE

# Copy file from VM
gcloud compute scp VM_NAME:REMOTE_FILE LOCAL_PATH --zone=ZONE

# Copy directory recursively
gcloud compute scp --recurse LOCAL_DIR VM_NAME:REMOTE_PATH --zone=ZONE
```

## VM Configuration

### Changing Machine Type

```bash
# Must stop the VM first
gcloud compute instances stop VM_NAME --zone=ZONE

# Change machine type
gcloud compute instances set-machine-type VM_NAME \
  --machine-type=n2-standard-8 \
  --zone=ZONE

# Start the VM again
gcloud compute instances start VM_NAME --zone=ZONE
```

### Attaching Disks

```bash
# Create a disk
gcloud compute disks create DISK_NAME \
  --zone=ZONE \
  --size=100GB \
  --type=pd-standard

# Attach disk to VM
gcloud compute instances attach-disk VM_NAME \
  --disk=DISK_NAME \
  --zone=ZONE

# Detach disk
gcloud compute instances detach-disk VM_NAME \
  --disk=DISK_NAME \
  --zone=ZONE
```

### Setting Metadata

```bash
# Set metadata
gcloud compute instances add-metadata VM_NAME \
  --zone=ZONE \
  --metadata=KEY1=VALUE1,KEY2=VALUE2

# Set startup script
gcloud compute instances add-metadata VM_NAME \
  --zone=ZONE \
  --metadata-from-file=startup-script=startup.sh
```

## Monitoring and Logs

### Viewing Serial Port Output

```bash
# View serial port output (useful for debugging boot issues)
gcloud compute instances get-serial-port-output VM_NAME --zone=ZONE

# Follow serial port output
gcloud compute instances tail-serial-port-output VM_NAME --zone=ZONE
```

### Viewing Logs

```bash
# View VM logs in Cloud Logging
gcloud logging read "resource.type=gce_instance AND resource.labels.instance_id=INSTANCE_ID" \
  --limit=50 \
  --format=json

# View logs for a specific VM by name
VM_NAME="your-vm-name"
ZONE="us-central1-a"
INSTANCE_ID=$(gcloud compute instances describe $VM_NAME \
  --zone=$ZONE \
  --format="get(id)")

gcloud logging read "resource.type=gce_instance AND resource.labels.instance_id=$INSTANCE_ID" \
  --limit=50
```

## Automation Scripts

### Complete Start VM and Update SSH Config Script

```bash
#!/bin/bash
set -e

# Configuration
VM_NAME="${1:-my-vm}"
ZONE="${2:-us-central1-a}"
SSH_CONFIG="$HOME/.ssh/config"

echo "========================================="
echo "Starting VM: $VM_NAME"
echo "Zone: $ZONE"
echo "========================================="

# Check if VM exists
if ! gcloud compute instances describe "$VM_NAME" \
    --zone="$ZONE" &>/dev/null; then
  echo "Error: VM $VM_NAME does not exist in zone $ZONE"
  exit 1
fi

# Start the VM
echo "Starting VM..."
gcloud compute instances start "$VM_NAME" --zone="$ZONE"

# Wait for VM to be running
echo "Waiting for VM to start..."
for i in {1..30}; do
  STATUS=$(gcloud compute instances describe "$VM_NAME" \
    --zone="$ZONE" \
    --format="value(status)")

  if [ "$STATUS" = "RUNNING" ]; then
    echo "VM is running!"
    break
  fi

  if [ $i -eq 30 ]; then
    echo "Error: VM failed to start within timeout"
    exit 1
  fi

  sleep 2
done

# Get external IP
echo "Getting external IP..."
EXTERNAL_IP=$(gcloud compute instances describe "$VM_NAME" \
  --zone="$ZONE" \
  --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

if [ -z "$EXTERNAL_IP" ]; then
  echo "Error: Could not get external IP"
  exit 1
fi

echo "External IP: $EXTERNAL_IP"

# Update SSH config (only if entry exists)
echo "Updating SSH config at $SSH_CONFIG..."

# Check if host entry exists
if grep -q "^Host $VM_NAME\$" "$SSH_CONFIG"; then
  # Create backup
  cp "$SSH_CONFIG" "${SSH_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"

  # Update existing entry's HostName
  echo "Updating existing SSH config entry..."

  # Use awk to update HostName in the specific host block
  awk -v vm="$VM_NAME" -v ip="$EXTERNAL_IP" '
    /^Host / { in_block=0 }
    /^Host '"$VM_NAME"'$/ { in_block=1; print; next }
    in_block && /^  HostName / { print "  HostName " ip; next }
    { print }
  ' "$SSH_CONFIG" > "${SSH_CONFIG}.tmp" && mv "${SSH_CONFIG}.tmp" "$SSH_CONFIG"
else
  # Warn if entry doesn't exist
  echo "========================================="
  echo "WARNING: No SSH config entry found for $VM_NAME"
  echo "========================================="
  echo "Please add this entry to $SSH_CONFIG manually:"
  echo ""
  echo "Host $VM_NAME"
  echo "  HostName $EXTERNAL_IP"
  echo "  User YOUR_USERNAME"
  echo "  StrictHostKeyChecking accept-new"
  echo "  UserKnownHostsFile ~/.ssh/known_hosts"
  echo ""
  echo "========================================="
fi

echo "========================================="
echo "VM started successfully!"
echo "External IP: $EXTERNAL_IP"
echo "SSH config updated!"
echo ""
echo "You can now connect with:"
echo "  ssh $VM_NAME"
echo "  OR"
echo "  gcloud compute ssh $VM_NAME --zone=$ZONE"
echo "========================================="
```

### Stop VM Script

```bash
#!/bin/bash
set -e

VM_NAME="${1:-my-vm}"
ZONE="${2:-us-central1-a}"

echo "Stopping VM: $VM_NAME in zone $ZONE..."

gcloud compute instances stop "$VM_NAME" --zone="$ZONE"

echo "VM stopped successfully!"
```

## Common Machine Types

- **e2-micro**: 0.25-2 vCPU, 1GB RAM (free tier eligible)
- **e2-small**: 0.5-2 vCPU, 2GB RAM
- **e2-medium**: 1-2 vCPU, 4GB RAM
- **e2-standard-2**: 2 vCPU, 8GB RAM
- **n2-standard-4**: 4 vCPU, 16GB RAM
- **n2-standard-8**: 8 vCPU, 32GB RAM
- **n2-highmem-8**: 8 vCPU, 64GB RAM
- **c2-standard-16**: 16 vCPU, 64GB RAM (compute-optimized)

## Common Image Families

- **debian-11**: `--image-family=debian-11 --image-project=debian-cloud`
- **ubuntu-2204-lts**: `--image-family=ubuntu-2204-lts --image-project=ubuntu-os-cloud`
- **centos-stream-9**: `--image-family=centos-stream-9 --image-project=centos-cloud`
- **rocky-linux-9**: `--image-family=rocky-linux-9 --image-project=rocky-linux-cloud`

## IAM Permissions

Required IAM roles:

- `roles/compute.admin`: Full control over Compute Engine resources
- `roles/compute.instanceAdmin.v1`: Manage VM instances
- `roles/compute.viewer`: Read-only access
- `roles/iam.serviceAccountUser`: Required to run VMs with service accounts

## Tips

1. **Stop VMs when not in use**: Avoid unnecessary charges by stopping idle VMs
2. **Use preemptible VMs**: For non-critical workloads, save up to 80% with `--preemptible`
3. **Update SSH config**: After starting a VM, always update `~/.ssh/config` with the new IP
4. **Use startup scripts**: Automate VM setup with `--metadata-from-file=startup-script=script.sh`
5. **Label resources**: Use `--labels` for better organization and cost tracking
6. **Zone selection**: Choose zones close to your data/users for lower latency

## Troubleshooting

### VM Won't Start

```bash
# Check serial port output for errors
gcloud compute instances get-serial-port-output VM_NAME --zone=ZONE

# Check quota limits
gcloud compute project-info describe
```

### SSH Connection Issues

```bash
# Reset SSH keys
gcloud compute config-ssh --remove
gcloud compute config-ssh

# Or use gcloud ssh which handles keys automatically
gcloud compute ssh VM_NAME --zone=ZONE --troubleshoot
```

### Can't Get External IP

```bash
# Check if VM has external IP configured
gcloud compute instances describe VM_NAME \
  --zone=ZONE \
  --format="get(networkInterfaces[0].accessConfigs[0])"

# If no external IP, add one
gcloud compute instances add-access-config VM_NAME \
  --zone=ZONE \
  --access-config-name="External NAT"
```

## Best Practices

1. **Backup before changes**: Create snapshots before major changes
2. **Use service accounts**: Assign minimal necessary permissions to VM service accounts
3. **Enable OS Login**: Use `--metadata=enable-oslogin=true` for better security
4. **Regular maintenance**: Keep VMs updated with security patches
5. **Cost optimization**: Stop or delete unused VMs, use preemptible VMs where appropriate
6. **Network security**: Use firewall rules and VPC configurations appropriately
7. **Monitoring**: Set up Cloud Monitoring alerts for critical VMs
