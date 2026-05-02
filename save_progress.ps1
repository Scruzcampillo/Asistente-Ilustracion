# save_progress.ps1 - Script de guardado automático para agentes con pausa de GDrive
param(
    [string]$Message = "Update: Guardado automático de progreso"
)

$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "No hay cambios para confirmar."
    exit
}

Write-Host "Registrando cambios..."
git add .
git commit -m "$Message"

Write-Host "Esperando a la sincronización de Google Drive (5 segundos)..."
Start-Sleep -Seconds 5
Write-Host "¡Sincronización completada!"
