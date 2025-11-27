Write-Host "🎯 ULTIMATE PROFESSIONAL SERVICE DEPLOYMENT" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Please run as Administrator" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green

# Step 1: Remove existing service
Write-Host "`n1. 🧹 REMOVING EXISTING SERVICE" -ForegroundColor Yellow
& "C:\Windows\System32\sc.exe" delete EdgeTinyMLAssistant 2>$null
Write-Host "✅ Clean slate created" -ForegroundColor Green

# Step 2: Create professional service
Write-Host "`n2. 🏗️ CREATING PROFESSIONAL SERVICE" -ForegroundColor Yellow
$pythonPath = "C:\Users\dell\Projects\Edge-TinyML-Project\edge-tinyml-env\Scripts\python.exe"
$scriptPath = "C:\Users\dell\Projects\Edge-TinyML-Project\phase6_edgeos_integration\service\professional_service.py"

$createCommand = "sc create EdgeTinyMLAssistant binPath= `"$pythonPath $scriptPath`" DisplayName= `"Edge TinyML AI Assistant`""
cmd /c $createCommand 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Service created successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Service creation failed" -ForegroundColor Red
    exit 1
}

# Step 3: Professional configuration
Write-Host "`n3. ⚙️ PROFESSIONAL CONFIGURATION" -ForegroundColor Yellow

& "C:\Windows\System32\sc.exe" failure EdgeTinyMLAssistant reset= 60 actions= restart/30000/restart/30000/restart/30000
& "C:\Windows\System32\sc.exe" config EdgeTinyMLAssistant start= auto
& "C:\Windows\System32\sc.exe" description EdgeTinyMLAssistant "Professional system-wide AI assistant with self-optimizing core and Android integration"

Write-Host "✅ Professional configuration applied" -ForegroundColor Green

# Step 4: Start service
Write-Host "`n4. 🚀 STARTING SERVICE" -ForegroundColor Yellow
& "C:\Windows\System32\sc.exe" start EdgeTinyMLAssistant

Start-Sleep -Seconds 3

# Step 5: Verification
Write-Host "`n5. 🔍 PROFESSIONAL VERIFICATION" -ForegroundColor Yellow

$service = Get-Service -Name "EdgeTinyMLAssistant*" -ErrorAction SilentlyContinue

if ($service) {
    Write-Host "✅ SERVICE STATUS:" -ForegroundColor Green
    Write-Host "   Name: $($service.Name)" -ForegroundColor Gray
    Write-Host "   Status: $($service.Status)" -ForegroundColor Gray
    
    $detailed = & "C:\Windows\System32\sc.exe" query EdgeTinyMLAssistant
    Write-Host "`n📊 DETAILED STATUS:" -ForegroundColor Cyan
    $detailed | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
    
    if ($service.Status -eq 'Running') {
        Write-Host "`n🎉 PROFESSIONAL SUCCESS!" -ForegroundColor Green
        Write-Host "   Edge TinyML Assistant is now SYSTEM-WIDE!" -ForegroundColor White
        Write-Host "   ✅ Auto-start enabled" -ForegroundColor Gray
        Write-Host "   ✅ Service recovery configured" -ForegroundColor Gray
        Write-Host "   ✅ Professional deployment complete" -ForegroundColor Gray
    } else {
        Write-Host "`n⚠️  Service installed - manual start required" -ForegroundColor Yellow
        Write-Host "   Run: sc start EdgeTinyMLAssistant" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ Service not found" -ForegroundColor Red
}

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "🎯 ULTIMATE DEPLOYMENT COMPLETE" -ForegroundColor Cyan
