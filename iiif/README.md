# README - IIIF Server Auto-Restart Guide

## Introduction
This guide provides instructions on how to start, restart, and stop the IIIF server using Singularity.

---

## 🚀 Start and Auto-Restart the IIIF Server

### Step 1: Go to directory
```bash
cd /ocean/projects/hum160002p/shared/iiif-server/
```

### Step 2: Stop any currently-running instance
```bash
singularity instance stop iiif1
```

### Step 2: Create the Singularity instance
```bash
singularity instance start --contain -B /ocean/projects/hum160002p/shared:/usr/local/images,config:/etc/iiif-server go-iiif-vips_latest.sif iiif1
```

### Step 3: Activate the IIIF server inside the container
```bash
nohup singularity run --env VIPS_DISC_THRESHOLD=250m instance://iiif1 > iiif.log &
```

### Step 4: Check that images are loading
Visit: [https://printprobdb.psc.edu/books](https://printprobdb.psc.edu/books)

### Step 5: Logout of the shell
```bash
exit
```

---

## 🔄 Automatically Restart the IIIF Server

If you want the server to restart automatically in case of failure, follow these steps:

### Step 1: Create the restart script `restart_iiif.sh`
```bash
#!/bin/bash

# Configure the IIIF server port
IIIF_PORT=8080

while true; do
    # Check if the server is running
    if ! ss -tulnp | grep -q ":$IIIF_PORT"; then
        echo "$(date) - IIIF server is down. Restarting..." | tee -a iiif_restart.log

        singularity instance stop iiif1
        singularity instance start --contain -B /ocean/projects/hum160002p/shared:/usr/local/images,config:/etc/iiif-server go-iiif-vips_latest.sif iiif1
        singularity run --env VIPS_DISC_THRESHOLD=250m instance://iiif1 > iiif.log 2>&1 &

        echo "$(date) - IIIF server restarted successfully." | tee -a iiif_restart.log
    fi
    sleep 5
done
```

### Step 2: Grant execution permission
```bash
chmod +x restart_iiif.sh
```

### Step 3: Run the script in the background
```bash
nohup ./restart_iiif.sh > restart_iiif.out 2>&1 &
```

---

## ❌ Stop the Auto-Restart Process
If you need to stop the auto-restart script, use one of the following methods:

### Method 1: Find and Kill the Process Manually
```bash
ps aux | grep restart_iiif.sh
kill <PID>
kill -9 <PID>  # Force kill if necessary
```

### Method 2: Use `pkill` to Stop the Script
```bash
pkill -f restart_iiif.sh
```

### Method 3: Stop Using `jobs` (If Running in Background)
```bash
jobs -l
kill %1
```

### Method 4: Stop All `nohup` Processes
```bash
pkill -f "nohup"
```
⚠️ **Warning:** This might stop other unrelated processes running with `nohup`.

---

## ✅ Verify That the Script Has Stopped
```bash
ps aux | grep restart_iiif.sh
ss -tulnp | grep 8080
```
If no output is returned, the script and server have successfully stopped.


