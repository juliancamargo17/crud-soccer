#!/bin/bash
# Script para desplegar microservicio en AWS Fargate
# Uso: ./deploy-fargate.sh <servicio>
# Ejemplo: ./deploy-fargate.sh estadios
#
# Requisitos:
#   - AWS CLI configurado con credenciales
#   - Permisos: ecs:*, ec2:DescribeSubnets, ec2:DescribeNetworkInterfaces
#   - Task definition en: infra/task/fargate-task-definition.json
#   - Imagen disponible en GHCR
#
# Autor: Julian Camargo
# Fecha: Diciembre 2025

set -e  # Detener ejecución si hay error

# Validar argumento
if [ -z "$1" ]; then
  echo "❌ Error: Debes especificar el servicio a desplegar"
  echo ""
  echo "Uso: ./deploy-fargate.sh <servicio>"
  echo ""
  echo "Servicios disponibles:"
  echo "  - equipos"
  echo "  - estadios"
  echo "  - dts"
  echo "  - jugadores"
  echo "  - participaciones"
  echo "  - torneos"
  echo ""
  echo "Ejemplo: ./deploy-fargate.sh estadios"
  exit 1
fi

SERVICE=$1
CLUSTER_NAME="crud-soccer-cluster"
VPC_ID="vpc-04f29f21da938f7cc"
SECURITY_GROUP="sg-0f2f2b8096fe2a87b"
REGION="us-east-1"

echo "🚀 Desplegando '$SERVICE' en AWS Fargate"
echo "================================================"
echo "   - Servicio: $SERVICE"
echo "   - Cluster: $CLUSTER_NAME"
echo "   - Región: $REGION"
echo ""

# 1. Crear ECS Cluster si no existe
echo "📦 Paso 1/6: Verificando ECS Cluster..."
if aws ecs describe-clusters \
    --clusters $CLUSTER_NAME \
    --region $REGION \
    --query 'clusters[0].status' \
    --output text 2>/dev/null | grep -q "ACTIVE"; then
    echo "   ✅ Cluster '$CLUSTER_NAME' ya existe"
else
    echo "   📦 Creando cluster '$CLUSTER_NAME'..."
    aws ecs create-cluster \
      --cluster-name $CLUSTER_NAME \
      --region $REGION \
      --tags key=Name,value=crud-soccer-cluster key=Environment,value=demo
    echo "   ✅ Cluster creado"
fi

# 2. Crear CloudWatch Log Group si no existe
echo ""
echo "📝 Paso 2/6: Configurando CloudWatch Logs..."
LOG_GROUP="/ecs/crud-soccer-$SERVICE"

if aws logs describe-log-groups \
    --log-group-name-prefix $LOG_GROUP \
    --region $REGION \
    --query 'logGroups[0].logGroupName' \
    --output text 2>/dev/null | grep -q "$LOG_GROUP"; then
    echo "   ✅ Log group '$LOG_GROUP' ya existe"
else
    echo "   📝 Creando log group '$LOG_GROUP'..."
    aws logs create-log-group \
      --log-group-name $LOG_GROUP \
      --region $REGION
    echo "   ✅ Log group creado"
fi

# 3. Registrar Task Definition
echo ""
echo "📋 Paso 3/6: Registrando Task Definition..."
TASK_DEF_FILE="infra/task/fargate-task-definition.json"

if [ ! -f "$TASK_DEF_FILE" ]; then
    echo "   ❌ Error: No se encontró $TASK_DEF_FILE"
    exit 1
fi

TASK_REVISION=$(aws ecs register-task-definition \
  --cli-input-json file://$TASK_DEF_FILE \
  --region $REGION \
  --query 'taskDefinition.revision' \
  --output text)

echo "   ✅ Task definition registrada (revisión: $TASK_REVISION)"

# 4. Obtener Subnet ID de la VPC
echo ""
echo "🌐 Paso 4/6: Obteniendo configuración de red..."
SUBNET=$(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[0].SubnetId' \
  --output text \
  --region $REGION)

if [ -z "$SUBNET" ] || [ "$SUBNET" = "None" ]; then
    echo "   ❌ Error: No se pudo obtener subnet de VPC $VPC_ID"
    exit 1
fi

echo "   ✅ Subnet: $SUBNET"
echo "   ✅ Security Group: $SECURITY_GROUP"

# 5. Ejecutar tarea en Fargate
echo ""
echo "🚢 Paso 5/6: Ejecutando tarea en Fargate..."
TASK_ARN=$(aws ecs run-task \
  --cluster $CLUSTER_NAME \
  --launch-type FARGATE \
  --task-definition crud-soccer-$SERVICE-task \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET],securityGroups=[$SECURITY_GROUP],assignPublicIp=ENABLED}" \
  --region $REGION \
  --query 'tasks[0].taskArn' \
  --output text)

if [ -z "$TASK_ARN" ] || [ "$TASK_ARN" = "None" ]; then
    echo "   ❌ Error: No se pudo crear la tarea"
    exit 1
fi

echo "   ✅ Tarea creada: $TASK_ARN"
echo "   ⏳ Esperando que la tarea esté en ejecución (30-60 segundos)..."

# Esperar 60 segundos para que la tarea inicie
sleep 60

# 6. Obtener IP pública
echo ""
echo "🔍 Paso 6/6: Obteniendo IP pública..."

# Obtener ENI (Elastic Network Interface)
ENI=$(aws ecs describe-tasks \
  --cluster $CLUSTER_NAME \
  --tasks $TASK_ARN \
  --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' \
  --output text \
  --region $REGION)

if [ -z "$ENI" ] || [ "$ENI" = "None" ]; then
    echo "   ⚠️  No se pudo obtener ENI. La tarea puede estar iniciando aún."
    echo "   Verifica manualmente con:"
    echo "   aws ecs describe-tasks --cluster $CLUSTER_NAME --tasks $TASK_ARN --region $REGION"
    exit 0
fi

# Obtener IP pública del ENI
PUBLIC_IP=$(aws ec2 describe-network-interfaces \
  --network-interface-ids $ENI \
  --query 'NetworkInterfaces[0].Association.PublicIp' \
  --output text \
  --region $REGION)

if [ -z "$PUBLIC_IP" ] || [ "$PUBLIC_IP" = "None" ]; then
    echo "   ⚠️  No se pudo obtener IP pública. Verifica la configuración de red."
    exit 1
fi

echo ""
echo "================================================"
echo "✅ DESPLIEGUE EXITOSO"
echo "================================================"
echo "📌 Servicio:    $SERVICE"
echo "📌 Task ARN:    $TASK_ARN"
echo "📌 IP Pública:  $PUBLIC_IP"
echo ""
echo "🌐 Endpoints disponibles:"
echo "   - Health:  http://$PUBLIC_IP:8000/health"
echo "   - Docs:    http://$PUBLIC_IP:8000/docs"
echo "   - API:     http://$PUBLIC_IP:8000/$SERVICE"
echo ""
echo "📊 Ver logs:"
echo "   aws logs tail /ecs/crud-soccer-$SERVICE --follow --region $REGION"
echo ""
echo "⚠️  IMPORTANTE: Esta tarea cobra ~\$0.045/hora"
echo "    Para detenerla después de la demo, ejecuta:"
echo ""
echo "    aws ecs stop-task --cluster $CLUSTER_NAME --task $TASK_ARN --region $REGION"
echo ""
echo "    O usa el script de limpieza:"
echo "    ./cleanup.sh"
echo "================================================"
