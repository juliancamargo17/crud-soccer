# Scripts de Infraestructura - CRUD Soccer

Scripts automatizados para gestionar la infraestructura de AWS del proyecto CRUD Soccer.

## Prerequisitos

Antes de ejecutar estos scripts:

1. **AWS CLI instalado y configurado**
   ```bash
   aws --version
   aws configure list
   ```

2. **Credenciales de AWS configuradas**
   - Access Key ID
   - Secret Access Key
   - Región por defecto: `us-east-1`

3. **Permisos IAM necesarios**
   - RDS: `rds:CreateDBInstance`, `rds:DescribeDBInstances`, `rds:DeleteDBInstance`
   - ECS: `ecs:*`
   - EC2: `ec2:DescribeSubnets`, `ec2:DescribeNetworkInterfaces`
   - CloudWatch Logs: `logs:CreateLogGroup`, `logs:DescribeLogGroups`

4. **Security Group creado previamente**
   - ID: `sg-0f2f2b8096fe2a87b`
   - Reglas de entrada: Puerto 5432 (PostgreSQL), Puerto 8000 (FastAPI)

## Scripts Disponibles

### 1. `create-rds.sh` - Crear RDS PostgreSQL

Crea una instancia de RDS PostgreSQL configurada para el proyecto.

**Uso:**
```bash
cd infra/scripts
chmod +x create-rds.sh
./create-rds.sh
```

**¿Qué hace?**
- Crea instancia RDS db.t3.micro (Free Tier)
- Configura PostgreSQL 16.3
- Asigna 20GB de storage SSD
- Habilita acceso público
- Espera hasta que esté disponible
- Muestra el endpoint y connection string

**Tiempo de ejecución:** 5-10 minutos

**Output esperado:**
```
Creando RDS PostgreSQL para CRUD Soccer...
================================================
Configuración:
   - Identificador: crud-soccer-db
   - Tipo: db.t3.micro (Free Tier)
   ...
RDS disponible y listo para usar!
================================================
Información de conexión:
================================================
Endpoint: crud-soccer-db.XXXXXXX.us-east-1.rds.amazonaws.com
Puerto:   5432
Usuario:  postgres
Password: RDS2025!
```

** Nota:** Si el RDS ya existe, el script abortará para evitar duplicados.

---

### 2. `deploy-fargate.sh` - Desplegar en AWS Fargate

Despliega un microservicio específico en AWS Fargate usando la imagen de GHCR.

**Uso:**
```bash
cd infra/scripts
chmod +x deploy-fargate.sh
./deploy-fargate.sh <servicio>
```

**Servicios disponibles:**
- `equipos`
- `estadios`
- `dts`
- `jugadores`
- `participaciones`
- `torneos`

**Ejemplo:**
```bash
./deploy-fargate.sh estadios
```

**¿Qué hace?**
1. Crea ECS Cluster (si no existe)
2. Configura CloudWatch Log Group
3. Registra Task Definition
4. Obtiene subnet de la VPC
5. Ejecuta tarea en Fargate con IP pública
6. Muestra IP y endpoints disponibles

**Tiempo de ejecución:** 1-2 minutos

**Output esperado:**
```
DESPLIEGUE EXITOSO
================================================
Servicio:    estadios
IP Pública:  3.85.XXX.XXX

Endpoints disponibles:
   - Health:  http://3.85.XXX.XXX:8000/health
   - Docs:    http://3.85.XXX.XXX:8000/docs
   - API:     http://3.85.XXX.XXX:8000/estadios

IMPORTANTE: Esta tarea cobra ~$0.045/hora
```

**Costo:** ~$0.045/hora (~$0.0125 por 10 segundos de demo)

**IMPORTANTE:** Se debe detener la tarea después de la demo para evitar cargos:
```bash
aws ecs stop-task --cluster crud-soccer-cluster --task <TASK_ARN> --region us-east-1
```

O usa el script de limpieza (ver abajo).

---

### 3. `cleanup.sh` - Limpiar recursos temporales

Detiene todas las tareas de Fargate en ejecución para evitar cargos no deseados.

**Uso:**
```bash
cd infra/scripts
chmod +x cleanup.sh
./cleanup.sh
```

**¿Qué hace?**
- Lista todas las tareas en ejecución en el cluster
- Detiene cada tarea automáticamente
- Muestra resumen de tareas detenidas

**¿Qué NO hace?** (Por seguridad, estos recursos requieren eliminación manual)
- NO elimina RDS (contiene datos)
- NO elimina Lambda functions
- NO elimina imágenes ECR
- NO elimina Security Groups
- NO elimina VPC

**Output esperado:**
```
Limpiando recursos de AWS
================================================
Encontradas 1 tarea(s) en ejecución

Deteniendo tarea: abc123def456
   Tarea detenida exitosamente

LIMPIEZA COMPLETADA
Resumen:
   - Tareas encontradas: 1
   - Tareas detenidas:   1
```

---

## Flujo de trabajo típico

### Demo rápida de Fargate (10 segundos, $0.01)

```bash
# 1. Desplegar servicio
./deploy-fargate.sh estadios

# 2. Probar endpoints (abre en navegador)
# http://<IP_PUBLICA>:8000/health
# http://<IP_PUBLICA>:8000/docs

# 3. Limpiar inmediatamente (después de 10 segundos)
./cleanup.sh
```

**Costo total:** ~$0.0125 (10 segundos)

### Setup completo desde cero

```bash
# 1. Crear RDS (una sola vez)
./create-rds.sh

# 2. Esperar 5-10 minutos hasta que esté disponible

# 3. Actualizar GitHub Secrets con el nuevo endpoint
# (Ir a: https://github.com/juliancamargo17/crud-soccer/settings/secrets/actions)

# 4. Desplegar Lambda via GitHub Actions
# (Push a main o ejecutar workflow manualmente)

# 5. (Opcional) Demo de Fargate
./deploy-fargate.sh estadios
./cleanup.sh  # Detener después de la demo
```

---

## Troubleshooting

### Error: "An error occurred (DBInstanceAlreadyExists)"
**Causa:** El RDS ya existe  
**Solución:** El script aborta automáticamente. Si quieres recrearlo, elimina el existente primero:
```bash
aws rds delete-db-instance --db-instance-identifier crud-soccer-db --skip-final-snapshot --region us-east-1
```

### Error: "Unable to assume role"
**Causa:** El rol IAM `ecsTaskExecutionRole` no existe  
**Solución:** Créalo manualmente desde AWS Console:
```
IAM > Roles > Create Role > ECS Task > ecsTaskExecutionRole
```

### Error: "No se pudo obtener subnet de VPC"
**Causa:** La VPC no existe o no tiene subnets  
**Solución:** Verifica la VPC ID en el script:
```bash
aws ec2 describe-vpcs --region us-east-1
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-04f29f21da938f7cc" --region us-east-1
```

### La IP pública no responde después de deploy
**Causa:** La tarea está iniciando (puede tomar 30-60 segundos)  
**Solución:** Esperar 1-2 minutos y verifica logs:
```bash
aws logs tail /ecs/crud-soccer-estadios --follow --region us-east-1
```

---

## Arquitectura de scripts

```
infra/scripts/
├── create-rds.sh          # Provisión de base de datos
├── deploy-fargate.sh      # Despliegue de contenedores
├── cleanup.sh             # Limpieza de recursos temporales
└── README.md             # Esta documentación

infra/task/
└── fargate-task-definition.json  # Configuración de Fargate (usado por deploy-fargate.sh)
```

---

## Best Practices

1. **Siempre ejecutar `cleanup.sh` después de demos de Fargate**
   - Fargate cobra por segundo (~$0.045/hora)
   - Un olvido de 24 horas = ~$1.08

2. **No eliminar RDS accidentalmente**
   - Contiene tus datos
   - No tiene backups configurados (para ahorrar $)
   - Eliminación es irreversible

3. **Mantener las credenciales seguras**
   - No commitees `RDS2025!` en código
   - Usa GitHub Secrets para CI/CD
   - En producción se debe usar AWS Secrets Manager

4. **Documentar cambios en task definitions**
   - Si se modifica `fargate-task-definition.json`, documenta el cambio
   - Incrementa la revisión manualmente en el nombre


## Recursos adicionales

- [AWS CLI Reference - RDS](https://docs.aws.amazon.com/cli/latest/reference/rds/)
- [AWS CLI Reference - ECS](https://docs.aws.amazon.com/cli/latest/reference/ecs/)
- [AWS Fargate Pricing](https://aws.amazon.com/fargate/pricing/)
- [Documentación del proyecto](../../README.md)
- [Endpoints desplegados](../../AWS-ENDPOINTS.md)