#!/bin/bash
# scripts/backup_db.sh
set -e

BACKUP_DIR="/var/backups/edgetinyml"
LOG_FILE="/var/log/edgetinyml_backup.log"
TIMESTAMP=
BACKUP_FILE="/cognitive_memory_.db"

echo "11/26/2025 20:10:28: Starting database backup" >> 

# Create backup directory
mkdir -p ""

# Verify database exists
if [ ! -f "db/cognitive_memory.db" ]; then
    echo "11/26/2025 20:10:28: ERROR - Database file not found" >> 
    exit 1
fi

# Create backup
echo "Creating database backup: "
cp "db/cognitive_memory.db" ""

# Verify backup
if [ -f "" ]; then
    BACKUP_SIZE=
    echo "11/26/2025 20:10:28: Backup created successfully - Size:  bytes" >> 
    
    # Compress backup
    gzip ""
    echo "11/26/2025 20:10:28: Backup compressed: .gz" >> 
else
    echo "11/26/2025 20:10:28: ERROR - Backup file not created" >> 
    exit 1
fi

# Cleanup old backups (keep 30 days)
echo "Cleaning up backups older than 30 days..."
find "" -name "cognitive_memory_*.db.gz" -mtime +30 -delete -print >> 

# Database integrity check (if sqlite3 available)
if command -v sqlite3 &> /dev/null; then
    if sqlite3 "db/cognitive_memory.db" "PRAGMA integrity_check;" | grep -q "ok"; then
        echo "11/26/2025 20:10:28: Database integrity check: PASSED" >> 
    else
        echo "11/26/2025 20:10:28: WARNING - Database integrity check failed" >> 
    fi
fi

echo "11/26/2025 20:10:28: Backup process completed successfully" >> 
echo "Backup completed: .gz"
