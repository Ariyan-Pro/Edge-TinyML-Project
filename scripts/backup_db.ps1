# PowerShell backup script for Windows
param(
    [string] = "C:\Backups\edgetinyml",
    [string] = "C:\Logs\edgetinyml_backup.log"
)

function Write-Log {
    param([string])
     = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    " : " | Out-File -FilePath  -Append
    Write-Host 
}

Write-Log "Starting database backup"

# Create backup directory
New-Item -ItemType Directory -Path  -Force | Out-Null

# Verify database exists
if (-not (Test-Path "db\cognitive_memory.db")) {
    Write-Log "ERROR: Database file not found"
    exit 1
}

# Create backup with timestamp
 = Get-Date -Format "yyyyMMdd_HHmmss"
 = "\cognitive_memory_.db"

try {
    Copy-Item "db\cognitive_memory.db" 
     = (Get-Item ).Length
    Write-Log "Backup created:  ( bytes)"
    
    # Compress backup
    Compress-Archive -Path  -DestinationPath ".zip" -Force
    Remove-Item 
    Write-Log "Backup compressed: .zip"
    
    # Cleanup old backups (keep 30 days)
    Get-ChildItem "\*.db.zip" | Where-Object { 
        .LastWriteTime -lt (Get-Date).AddDays(-30) 
    } | Remove-Item -Force
    Write-Log "Cleaned up backups older than 30 days"
    
    Write-Log "Backup process completed successfully"
}
catch {
    Write-Log "ERROR: Backup failed - "
    exit 1
}
