#!/bin/bash
# Actualiza el ARN del secreto DB_PASSWORD en todas las task definitions de Fargate.
# Uso:
#   ./set-task-secret-arn.sh arn:aws:secretsmanager:us-east-1:123456789012:secret:crud-soccer/db-password-abc123

set -e

SECRET_ARN="$1"
TASK_DIR="infra/task"

if [ -z "$SECRET_ARN" ]; then
  echo "Error: Debes pasar el ARN del secreto."
  echo "Uso: ./set-task-secret-arn.sh <SECRET_ARN>"
  exit 1
fi

for file in "$TASK_DIR"/fargate-task-*.json; do
  if [ ! -f "$file" ]; then
    continue
  fi

  sed -i.bak "s|REPLACE_WITH_DB_PASSWORD_SECRET_ARN|$SECRET_ARN|g" "$file"
  rm -f "$file.bak"
  echo "Actualizado: $file"
done

echo ""
echo "Completado: task definitions actualizadas con el ARN del secreto."
