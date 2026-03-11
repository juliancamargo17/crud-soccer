#!/bin/bash
# Script para crear RDS PostgreSQL para CRUD Soccer
# Uso: ./create-rds.sh
# 
# Requisitos:
#   - AWS CLI configurado con credenciales
#   - Permisos: rds:CreateDBInstance, rds:DescribeDBInstances
#   - Security Group ya creado: sg-0f2f2b8096fe2a87b
#
# Autor: Julian Camargo
# Fecha: Diciembre 2025

set -e  # Detener ejecución si hay error

echo "Creando RDS PostgreSQL para CRUD Soccer..."
echo "================================================"

# Variables de configuración
DB_IDENTIFIER="crud-soccer-db"
DB_CLASS="db.t3.micro"
DB_ENGINE="postgres"
DB_ENGINE_VERSION="16.3"
DB_USERNAME="postgres"
# Definir DB_PASSWORD por variable de entorno para evitar credenciales hardcodeadas.
DB_PASSWORD="${DB_PASSWORD:-}"
ALLOCATED_STORAGE=20
STORAGE_TYPE="gp2"
SECURITY_GROUP="sg-0f2f2b8096fe2a87b"
REGION="us-east-1"

if [ -z "$DB_PASSWORD" ]; then
  echo "Error: DB_PASSWORD no esta configurada."
  echo "Ejemplo de uso: DB_PASSWORD='tu_password_segura' ./create-rds.sh"
  exit 1
fi

echo "Configuración:"
echo "- Identificador: $DB_IDENTIFIER"
echo "- Tipo: $DB_CLASS (Free Tier)"
echo "- Motor: $DB_ENGINE $DB_ENGINE_VERSION"
echo "- Storage: ${ALLOCATED_STORAGE}GB $STORAGE_TYPE"
echo "- Región: $REGION"
echo ""

# Verificar si RDS ya existe
if aws rds describe-db-instances \
    --db-instance-identifier $DB_IDENTIFIER \
    --region $REGION \
    --output text > /dev/null 2>&1; then
    echo "RDS '$DB_IDENTIFIER' ya existe. Abortando..."
    exit 1
fi

echo "Creando instancia RDS..."
aws rds create-db-instance \
  --db-instance-identifier $DB_IDENTIFIER \
  --db-instance-class $DB_CLASS \
  --engine $DB_ENGINE \
  --engine-version $DB_ENGINE_VERSION \
  --master-username $DB_USERNAME \
  --master-user-password $DB_PASSWORD \
  --allocated-storage $ALLOCATED_STORAGE \
  --storage-type $STORAGE_TYPE \
  --vpc-security-group-ids $SECURITY_GROUP \
  --publicly-accessible \
  --backup-retention-period 0 \
  --port 5432 \
  --no-storage-encrypted \
  --region $REGION \
  --tags "Key=Name,Value=crud-soccer-db" "Key=Environment,Value=demo" "Key=ManagedBy,Value=script"

echo ""
echo "RDS creado exitosamente!"
echo "Esperando hasta que esté disponible (esto puede tomar 5-10 minutos)..."

# Esperar hasta que esté disponible
aws rds wait db-instance-available \
  --db-instance-identifier $DB_IDENTIFIER \
  --region $REGION

echo ""
echo "RDS disponible y listo para usar!"

# Obtener y mostrar información del endpoint
ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier $DB_IDENTIFIER \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region $REGION)

PORT=$(aws rds describe-db-instances \
  --db-instance-identifier $DB_IDENTIFIER \
  --query 'DBInstances[0].Endpoint.Port' \
  --output text \
  --region $REGION)

echo ""
echo "================================================"
echo "Información de conexión:"
echo "================================================"
echo "Endpoint: $ENDPOINT"
echo "Puerto:   $PORT"
echo "Usuario:  $DB_USERNAME"
echo "Password: [CONFIGURADO VIA VARIABLE DE ENTORNO]"
echo "Database: postgres"
echo ""
echo "Connection String:"
echo "postgresql://$DB_USERNAME:[DB_PASSWORD_FROM_SECRET]@$ENDPOINT:$PORT/postgres"
echo ""
echo "Configurar en Lambda Environment Variables:"
echo "   DB_HOST=$ENDPOINT"
echo "   DB_PORT=$PORT"
echo "   DB_USER=$DB_USERNAME"
echo "   DB_PASSWORD=[VALOR DEFINIDO EN SECRETS]"
echo "   DB_NAME=postgres"
echo ""
echo "IMPORTANTE: Actualiza GitHub Secrets con el nuevo endpoint"
echo "================================================"