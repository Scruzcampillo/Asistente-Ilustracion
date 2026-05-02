#!/bin/bash
# save_progress.sh - Script de guardado automático para agentes con pausa de GDrive

# Comprobar si hay cambios
if [ -z "$(git status --porcelain)" ]; then
  echo "No hay cambios para confirmar."
  exit 0
fi

# El commit message se puede pasar como argumento, si no, uno por defecto
MSG=${1:-"Update: Guardado automático de progreso"}

echo "Registrando cambios..."
git add .
git commit -m "$MSG"

echo "Esperando a la sincronización de Google Drive (5 segundos)..."
sleep 5
echo "¡Sincronización completada!"
