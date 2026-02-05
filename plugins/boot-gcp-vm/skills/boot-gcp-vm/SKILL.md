---
name: boot-gcp-vm
description: Start a Google Compute Engine VM and update the local SSH config with its new IP address. Use when asked to boot up, start, or connect to a GCP VM.
allowed-tools: Bash(gcloud*), Read, Edit, Grep
---

# Start GCP VM and Update SSH Config

Start a Google Compute Engine VM and automatically update `~/.ssh/config` with the VM's new external IP so you can `ssh <vm-name>` immediately.

## Prerequisites

- `gcloud` CLI installed and authenticated (`gcloud auth login`)
- Compute Engine API enabled: `gcloud services enable compute.googleapis.com`
- An existing VM in your GCP project
- An existing SSH config entry for the VM in `~/.ssh/config`

## SSH Config Format

The VM **must** already have an entry in `~/.ssh/config`. The start script updates the `HostName` field but does not create new entries.

```
Host <vm-name>
  HostName <current-or-placeholder-ip>
  User <your-username>
  StrictHostKeyChecking accept-new
  UserKnownHostsFile ~/.ssh/known_hosts
```

## Start VM and Update SSH Config

```bash
#!/bin/bash
set -e

VM_NAME="${1:-my-vm}"
ZONE="${2:-us-central1-a}"
SSH_CONFIG="$HOME/.ssh/config"

echo "Starting VM: $VM_NAME in zone $ZONE"

# Start the VM
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
EXTERNAL_IP=$(gcloud compute instances describe "$VM_NAME" \
  --zone="$ZONE" \
  --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

if [ -z "$EXTERNAL_IP" ]; then
  echo "Error: Could not get external IP"
  exit 1
fi

echo "External IP: $EXTERNAL_IP"

# Update SSH config
if grep -q "^Host $VM_NAME\$" "$SSH_CONFIG"; then
  cp "$SSH_CONFIG" "${SSH_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"

  awk -v vm="$VM_NAME" -v ip="$EXTERNAL_IP" '
    /^Host / { in_block=0 }
    /^Host '"$VM_NAME"'$/ { in_block=1; print; next }
    in_block && /^  HostName / { print "  HostName " ip; next }
    { print }
  ' "$SSH_CONFIG" > "${SSH_CONFIG}.tmp" && mv "${SSH_CONFIG}.tmp" "$SSH_CONFIG"

  echo "SSH config updated. Connect with: ssh $VM_NAME"
else
  echo "WARNING: No SSH config entry found for $VM_NAME"
  echo "Add this to $SSH_CONFIG:"
  echo ""
  echo "Host $VM_NAME"
  echo "  HostName $EXTERNAL_IP"
  echo "  User YOUR_USERNAME"
  echo "  StrictHostKeyChecking accept-new"
  echo "  UserKnownHostsFile ~/.ssh/known_hosts"
fi
```

## Stop VM

```bash
gcloud compute instances stop VM_NAME --zone=ZONE
```

## Quick Reference

```bash
# List VMs
gcloud compute instances list

# Start VM + update SSH config (inline)
VM_NAME="my-vm" ZONE="us-central1-a" && \
  gcloud compute instances start "$VM_NAME" --zone="$ZONE" && \
  sleep 10 && \
  EXTERNAL_IP=$(gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --format="get(networkInterfaces[0].accessConfigs[0].natIP)") && \
  echo "IP: $EXTERNAL_IP"

# Check VM status
gcloud compute instances describe VM_NAME --zone=ZONE --format="value(status)"

# Get external IP
gcloud compute instances describe VM_NAME --zone=ZONE \
  --format="get(networkInterfaces[0].accessConfigs[0].natIP)"

# SSH via gcloud (no config needed)
gcloud compute ssh VM_NAME --zone=ZONE

# SSH via native ssh (after config update)
ssh VM_NAME
```

## Troubleshooting

### VM Won't Start
```bash
gcloud compute instances get-serial-port-output VM_NAME --zone=ZONE
```

### SSH Connection Refused
- VM may still be booting — wait 30 seconds after start
- Check firewall rules allow SSH (port 22)
- Verify SSH config has correct IP: `grep -A3 "Host VM_NAME" ~/.ssh/config`

### No External IP
```bash
gcloud compute instances add-access-config VM_NAME \
  --zone=ZONE \
  --access-config-name="External NAT"
```
