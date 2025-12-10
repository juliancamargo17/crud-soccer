#!/bin/bash
# Script para limpiar recursos de AWS (ECS Fargate tasks)
# Uso: ./cleanup.sh
#
# IMPORTANTE: Este script NO elimina:
#   - RDS (requiere confirmación manual por seguridad)
#   - Lambda functions
#   - ECR repositories
#   - Security Groups
#   - VPC
#
# Solo detiene tareas activas de Fargate para evitar cargos


set -e  # Detener ejecución si hay error

CLUSTER_NAME="crud-soccer-cluster"
REGION="us-east-1"

echo "Limpiando recursos de AWS"
echo "================================================"
echo "   - Cluster: $CLUSTER_NAME"
echo "   - Región: $REGION"
echo ""

# Verificar si el cluster existe
if ! aws ecs describe-clusters \
    --clusters $CLUSTER_NAME \
    --region $REGION \
    --query 'clusters[0].status' \
    --output text 2>/dev/null | grep -q "ACTIVE"; then
    echo "Cluster '$CLUSTER_NAME' no existe o no está activo"
    echo "Nada que limpiar"
    exit 0
fi

# Listar tareas en ejecución
echo "Buscando tareas en ejecución..."
TASKS=$(aws ecs list-tasks \
  --cluster $CLUSTER_NAME \
  --desired-status RUNNING \
  --query 'taskArns[]' \
  --output text \
  --region $REGION)

if [ -z "$TASKS" ]; then
    echo "No hay tareas en ejecución en el cluster"
    echo "Nada que limpiar"
    exit 0
fi

# Contar tareas
TASK_COUNT=$(echo "$TASKS" | wc -w)
echo "Encontradas $TASK_COUNT tarea(s) en ejecución"
echo ""

# Detener cada tarea
STOPPED=0
for task in $TASKS; do
    TASK_ID=$(basename $task)
    echo "Deteniendo tarea: $TASK_ID"
    
    if aws ecs stop-task \
        --cluster $CLUSTER_NAME \
        --task $task \
        --reason "Detenida por script de limpieza" \
        --region $REGION \
        --output text > /dev/null 2>&1; then
        echo "Tarea detenida exitosamente"
        ((STOPPED++))
    else
        echo "Error al detener tarea (puede que ya esté detenida)"
    fi
    echo ""
done

echo "================================================"
echo "LIMPIEZA COMPLETADA"
echo "================================================"
echo "Resumen:"
echo "- Tareas encontradas: $TASK_COUNT"
echo "- Tareas detenidas:   $STOPPED"
echo ""
echo "Recursos NO eliminados (requieren acción manual):"
echo "- RDS: crud-soccer-db (para eliminar, ver abajo)"
echo "- Lambda functions (6 funciones activas)"
echo "- ECR repositories (imágenes Docker)"
echo "- ECS Cluster: $CLUSTER_NAME"
echo "- CloudWatch Log Groups"
echo ""
echo "Para eliminar RDS manualmente (¡CUIDADO! Esto borra datos):"
echo "aws rds delete-db-instance \\"
echo "--db-instance-identifier crud-soccer-db \\"
echo "--skip-final-snapshot \\"
echo "--region $REGION"
echo ""
echo "Para eliminar ECS Cluster (solo si no hay tareas):"
echo "aws ecs delete-cluster \\"
echo "--cluster $CLUSTER_NAME \\"
echo "--region $REGION"
echo "================================================"
