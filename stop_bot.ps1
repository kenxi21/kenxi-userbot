Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       KENXI USERBOT - STOP SCRIPT          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "[INFO] Mencari proses Python yang berjalan..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "[FOUND] Ditemukan $($pythonProcesses.Count) proses Python:" -ForegroundColor Green
    $pythonProcesses | Format-Table Id, ProcessName, StartTime -AutoSize
    
    Write-Host ""
    $confirm = Read-Host "Apakah Anda ingin menghentikan semua proses Python? (Y/N)"
    
    if ($confirm -eq 'Y' -or $confirm -eq 'y') {
        Write-Host "[STOPPING] Menghentikan semua proses Python..." -ForegroundColor Red
        Stop-Process -Name python -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        
        $remaining = Get-Process python -ErrorAction SilentlyContinue
        if ($remaining) {
            Write-Host "[WARNING] Masih ada proses yang berjalan, force stopping..." -ForegroundColor Yellow
            foreach ($proc in $remaining) {
                Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
            }
        }
        
        Write-Host "[SUCCESS] ✅ Semua proses Python dihentikan!" -ForegroundColor Green
    } else {
        Write-Host "[CANCELLED] Operasi dibatalkan" -ForegroundColor Yellow
    }
} else {
    Write-Host "[INFO] ✅ Tidak ada proses Python yang berjalan" -ForegroundColor Green
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
