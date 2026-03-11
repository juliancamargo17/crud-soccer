#!/bin/bash
# Crea o actualiza un secreto en AWS Secrets Manager para DB_PASSWORD.
# Uso:
#   export DB_PASSWORD="tu_password_segura"
#   ./create-db-secret.sh
# Opcional:
#   SECRET_NAME=crud-soccer/db-password REGION=us-east-1 ./create-db-secret.sh

set -e

SECRET_NAME="${SECRET_NAME:-crud-soccer/db-password}"
REGION="${REGION:-us-east-1}"
DB_PASSWORD="${DB_PASSWORD:-}"

if [ -z "$DB_PASSWORD" ]; then
  echo "Error: DB_PASSWORD no esta configurada."
  echo "Ejemplo: DB_PASSWORD='tu_password_segura' ./create-db-secret.sh"
  exit 1
fi

if aws secretsmanager describe-secret --secret-id "$SECRET_NAME" --region "$REGION" >/dev/null 2>&1; then
  echo "Secreto existente detectado. Actualizando valor..."
  aws secretsmanager put-secret-value \
    --secret-id "$SECRET_NAME" \
    --secret-string "$DB_PASSWORD" \
    --region "$REGION" >/dev/null
else
  echo "Creando secreto en Secrets Manager..."
  aws secretsmanager create-secret \
    --name "$SECRET_NAME" \
    --secret-string "$DB_PASSWORD" \
    --region "$REGION" >/dev/null
fi

SECRET_ARN=$(aws secretsmanager describe-secret \
  --secret-id "$SECRET_NAME" \
  --query 'ARN' \
  --output text \
  --region "$REGION")

echo ""
echo "Secreto listo."
echo "SECRET_NAME=$SECRET_NAME"
echo "SECRET_ARN=$SECRET_ARN"
echo ""
echo "Siguiente paso:"
echo "  ./set-task-secret-arn.sh \"$SECRET_ARN\""
