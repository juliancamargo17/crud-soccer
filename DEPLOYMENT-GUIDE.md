# Guía Paso a Paso - Despliegue en AWS (Lambda + Fargate + GHCR)

Esta guía implementa **exactamente** lo que pidió tu DevOps:
- **AWS Lambda** (contenedores serverless)
- **AWS Fargate** (task de demostración)
- **GitHub Container Registry (GHCR)** (gratis, ilimitado para públicos)
- **GitHub Actions** (CI/CD automático, gratis)

## 🎯 Arquitectura Final:

```
GitHub Repo (código)
       ↓
GitHub Actions (CI/CD) - GRATIS
       ↓
GitHub Container Registry (GHCR) - GRATIS
       ↓
    ┌──────────────┬─────────────┐
    ↓              ↓             ↓
AWS Lambda    AWS Fargate    Amazon RDS
(6 servicios)  (demo task)   (PostgreSQL)
   GRATIS      $0.01/demo      GRATIS
```

## 💰 Estrategia de costos: ~$0/mes

- ✅ **GitHub Container Registry**: Gratis (público ilimitado)
- ✅ **GitHub Actions**: Gratis (2000 min/mes)
- ✅ **AWS Lambda**: Gratis (1M requests/mes)
- ✅ **AWS Fargate**: $0.01 por demo de 10 segundos, luego $0
- ✅ **RDS PostgreSQL**: Gratis (750 horas/mes Free Tier)
- ❌ **ALB**: No usar (cobra $16/mes siempre)

**Total: $0.00-0.10/mes** (solo cargos mínimos de demos de Fargate)

---

## ✅ Pre-requisitos

Antes de comenzar, asegúrate de tener:

- [ ] Cuenta de AWS activa (Free Tier)
- [ ] Cuenta de GitHub (gratis)
- [ ] Repositorio de GitHub (crear uno nuevo)
- [ ] AWS CLI instalado: `aws --version`
- [ ] Git instalado: `git --version`
- [ ] Docker instalado (opcional, para pruebas locales)

---

## 🚀 FASE 1: Configuración AWS (30 minutos)

### Paso 1.1: Crear usuario IAM

```bash
# En AWS Console
1. IAM → Users → Create user
2. User name: github-actions-deployer
3. Attach policies directly:
   - AmazonECS_FullAccess
   - AmazonEC2ContainerRegistryFullAccess
   - AWSLambda_FullAccess
   - AmazonRDSFullAccess
   - CloudWatchLogsFullAccess
4. Create user
5. Security credentials → Create access key
6. Use case: CLI
7. GUARDAR:
   - Access Key ID: AKIA...
   - Secret Access Key: ...
```

**Configurar AWS CLI localmente:**
```powershell
aws configure
# AWS Access Key ID: [PEGAR TU ACCESS KEY]
# AWS Secret Access Key: [PEGAR TU SECRET KEY]
# Default region name: us-east-1
# Default output format: json
```

**Verificar:**
```powershell
aws sts get-caller-identity
# Debe mostrar tu Account ID (usuario ARN)
# Si da error, verificar que Access Key sea correcta
```

**Obtener tu Account ID:**
```powershell
# El Account ID es el número de 12 dígitos en el ARN
# Ejemplo: arn:aws:iam::123456789012:user/nombre
#                         ^^^^^^^^^^^^
# GUARDAR ESTE NÚMERO, lo necesitarás después
```

---

### Paso 1.2: Crear RDS PostgreSQL

```bash
# En AWS Console
1. RDS → Create database
2. Choose a database creation method: Standard create
3. Engine options: PostgreSQL 15.x
4. Templates: Free tier
5. Settings:
   - DB instance identifier: soccer-db
   - Master username: postgres
   - Master password: Soccer2025! (o tu contraseña)
   - Confirm password: Soccer2025!
6. Instance configuration:
   - DB instance class: db.t3.micro (Free tier)
7. Storage:
   - Storage type: General Purpose SSD (gp3)
   - Allocated storage: 20 GiB
8. Connectivity:
   - Compute resource: Don't connect to an EC2 compute resource
   - VPC: Default VPC
   - Public access: Yes (para demo)
   - VPC security group: Create new → soccer-db-sg
9. Additional configuration:
   - Initial database name: postgres
10. Create database
```

**Esperar 5-10 minutos**

**Configurar Security Group:**
```bash
1. RDS → Databases → soccer-db
2. Connectivity & security → VPC security groups → Click en el security group
3. Inbound rules → Edit inbound rules → Add rule
   - Type: PostgreSQL
   - Protocol: TCP
   - Port: 5432
   - Source: 0.0.0.0/0 (Anywhere-IPv4)
4. Save rules
```

**Obtener endpoint:**
```bash
1. RDS → Databases → soccer-db
2. Connectivity & security
3. Copiar: Endpoint (ejemplo: soccer-db.xxxx.us-east-1.rds.amazonaws.com)
4. GUARDAR ESTE ENDPOINT
```

---

### Paso 1.3: Crear repositorios ECR

**Opción A: Mediante AWS CLI (Recomendado)**
```powershell
# Crear los 6 repositorios
aws ecr create-repository --repository-name soccer/equipos --region us-east-1
aws ecr create-repository --repository-name soccer/estadios --region us-east-1
aws ecr create-repository --repository-name soccer/dts --region us-east-1
aws ecr create-repository --repository-name soccer/jugadores --region us-east-1
aws ecr create-repository --repository-name soccer/participaciones --region us-east-1
aws ecr create-repository --repository-name soccer/torneos --region us-east-1

# Verificar
aws ecr describe-repositories --region us-east-1
```

**Opción B: Mediante Console**
```bash
1. ECR → Repositories → Create repository (repetir 6 veces)
2. Visibility settings: Private
3. Repository name:
   - soccer/equipos
   - soccer/estadios
   - soccer/dts
   - soccer/jugadores
   - soccer/participaciones
   - soccer/torneos
4. Image scan settings: Scan on push (opcional)
5. Create repository
---

## 📦 FASE 2: Build y Push a ECR - MANUAL (30 minutos)

**SIN GitHub Actions - Deployment manual con PowerShell**

### Paso 2.1: Preparar variables

```powershell
# Definir tu Account ID (obtenerlo de aws sts get-caller-identity)
$AccountId = "123456789012"  # ← CAMBIAR POR TU ACCOUNT ID
$Region = "us-east-1"
$RdsEndpoint = "soccer-db.xxxx.us-east-1.rds.amazonaws.com"  # ← CAMBIAR
```

### Paso 2.2: Login a ECR

```powershell
# Autenticar Docker con ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AccountId.dkr.ecr.us-east-1.amazonaws.com
```

### Paso 2.3: Build y Push usando el script

```powershell
# Ejecutar el script de deployment
.\deploy-manual.ps1 -AccountId $AccountId

# El script automáticamente:
# - Construye las 6 imágenes Docker
# - Las tagea correctamente para ECR
# - Las sube a ECR
# - Verifica que estén disponibles
```

**O manualmente (si prefieres hacerlo paso a paso):**

```powershell
# Para cada servicio, ejemplo con equipos:
$EcrUri = "$AccountId.dkr.ecr.us-east-1.amazonaws.com/soccer/equipos"

# Build
docker build -f ./classEquipo/Dockerfile -t soccer/equipos:latest .

# Tag
docker tag soccer/equipos:latest $EcrUri:latest

# Push
docker push $EcrUri:latest

# Repetir para: estadios, dts, jugadores, participaciones, torneos
```

### Paso 2.4: Verificar imágenes en ECR
```bash
1. GitHub → Tu repo → Actions
2. Click en el workflow "Build and Push to AWS ECR"
3. Ver progreso en tiempo real
4. Esperar a que termine (aprox. 10-15 minutos)
5. Verificar que todos los jobs estén en verde ✓
```

### Paso 3.3: Verificar imágenes en ECR

```powershell
# Ver todas las imágenes
aws ecr list-images --repository-name soccer/equipos --region us-east-1
aws ecr list-images --repository-name soccer/estadios --region us-east-1
# ... repetir para todos

# O verificar en Console
# ECR → Repositories → Click en cada repo → Ver imágenes con tag "latest"
```

---

## 🚀 FASE 3: Deploy a Lambda - GRATIS (40 minutos)

### Paso 3.1: Crear función Lambda para Equipos
- 1 millón de requests/mes
- 400,000 GB-segundos de compute/mes
- Para demo es 100% gratis

### Paso 4.1: Crear función Lambda para Equipos

```bash
1. Lambda → Functions → Create function
2. Container image
3. Function name: soccer-equipos-lambda
4. Container image URI: [COPIAR URI de ECR]/soccer/equipos:latest
   Ejemplo: 123456789012.dkr.ecr.us-east-1.amazonaws.com/soccer/equipos:latest
5. Architecture: x86_64
6. Create function (esperar 1-2 minutos)
```

**Configurar la función:**
```bash
7. Configuration → General configuration → Edit
   - Memory: 512 MB
   - Timeout: 30 seconds
   - Save

8. Configuration → Environment variables → Edit
   - Add environment variable (repetir 5 veces):
     DB_HOST: [TU RDS ENDPOINT]
     DB_USER: postgres
     DB_PASSWORD: Soccer2025!
     DB_NAME: postgres
     DB_PORT: 5432
   - Save

9. Configuration → Function URL → Create function URL
   - Auth type: NONE (solo para demo)
   - CORS:
     Allow origin: *
     Allow methods: GET, POST, PUT, DELETE, OPTIONS
     Allow headers: *
   - Save

10. COPIAR LA FUNCTION URL generada
    Ejemplo: https://abcd1234.lambda-url.us-east-1.on.aws/
```

**Probar la función:**
```powershell
# Test básico
curl https://[TU-FUNCTION-URL].lambda-url.us-east-1.on.aws/health

# Debe responder:
# {"status":"healthy","service":"equipos"}

# Ver Swagger
# Abrir en navegador:
https://[TU-FUNCTION-URL].lambda-url.us-east-1.on.aws/docs
```

### Paso 3.2: Repetir para los otros 5 servicios

**Crear funciones Lambda para:**
- soccer-estadios-lambda → soccer/estadios:latest
- soccer-dts-lambda → soccer/dts:latest
- soccer-jugadores-lambda → soccer/jugadores:latest
- soccer-participaciones-lambda → soccer/participaciones:latest
- soccer-torneos-lambda → soccer/torneos:latest

**Para cada una:**
- Configurar memoria, timeout
- Agregar variables de entorno (mismas que equipos)
- Crear Function URL
- Probar endpoint /health

---

## 🐳 FASE 4: Configuración Fargate - SOLO DEMO (20 minutos)

**⚠️ IMPORTANTE: NO ejecutar tasks en Fargate (genera cargos inmediatos)**

**Objetivo:** Crear configuración de ECS/Fargate para demostrar conocimiento, pero sin ejecutar servicios.

### Paso 4.1: Crear ECS Cluster (SIN COSTO)

```bash
1. ECS → Clusters → Create cluster
2. Cluster name: soccer-cluster
3. Infrastructure: AWS Fargate (serverless)
### Paso 4.2: Crear Task Definition para Equipos (SIN COSTO)
5. Create
```

### Paso 5.2: Crear Task Definition para Equipos

```bash
1. ECS → Task Definitions → Create new task definition
2. Task definition family: soccer-equipos-task
3. Launch type: Fargate
4. Operating system/Architecture: Linux/X86_64
5. Task size:
   - CPU: 0.25 vCPU
   - Memory: 0.5 GB
6. Task role: Create new role → ecsTaskExecutionRole
7. Task execution role: ecsTaskExecutionRole

8. Container - 1:
   - Name: equipos
   - Image URI: [URI DE ECR]/soccer/equipos:latest
   - Port mappings: 8000 TCP
   - Environment variables - Add individually:
     * DB_HOST: [RDS ENDPOINT]
     * DB_USER: postgres
     * DB_PASSWORD: Soccer2025!
     * DB_NAME: postgres
     * DB_PORT: 5432
   
   - HealthCheck (opcional):
     * Command: CMD-SHELL,curl -f http://localhost:8000/health || exit 1
     * Interval: 30
     * Timeout: 5
     * Retries: 3
   
   - Log collection:
     * Log driver: awslogs
     * Log group: Create new → /ecs/soccer-equipos
     * Log stream prefix: ecs
### Paso 4.3: **NO CREAR SERVICES** (evitar cargos)

**⚠️ DETENER AQUÍ - NO CREAR SERVICES EN FARGATE**

**Para evitar cargos:**
- ✅ Crear Cluster (gratis)
- ✅ Crear Task Definitions (gratis)
- ❌ NO crear Services
- ❌ NO ejecutar Tasks

**Para demostración:**
1. Tomar screenshots del Cluster creado
2. Tomar screenshots de las Task Definitions
3. Explicar que conoces Fargate pero no lo ejecutas por costos

**Si quieres probar Fargate (costará $0.50-1.00/hora):**
```bash
1. ECS → Clusters → soccer-cluster → Services → Create
2. Desired tasks: 1
3. ⚠️ IMPORTANTE: Después de probar, eliminar el service inmediatamente
4. No dejar corriendo más de 5-10 minutos
```

**Alternativa sin costo:**
- Lambda cubre todos los servicios gratuitamente
- Fargate solo para demostrar que sabes configurarlo
- soccer-jugadores-task → soccer-jugadores-service
- soccer-torneos-task → soccer-torneos-service

*Nota: Para demo, solo 3 servicios en Fargate es suficiente*

---

## 📝 FASE 6: Documentar y Probar (15 minutos)

### Paso 6.1: Actualizar AWS-ENDPOINTS.md

```bash
1. Abrir AWS-ENDPOINTS.md
2. Reemplazar [PENDING] con tus URLs reales de Lambda
3. Reemplazar [IP-PENDING] con las IPs de Fargate
4. Actualizar endpoint de RDS
5. Actualizar Account ID en ECR URIs
6. Git commit y push
```

### Paso 6.2: Testing completo

**Test 1: Lambda - GET**
```powershell
curl https://[TU-LAMBDA-URL]/
```

**Test 2: Lambda - POST**
```powershell
curl -X POST https://[TU-LAMBDA-URL]/ `
---

## 📝 FASE 5: Documentar y Probar (15 minutos)

### Paso 5.1: Actualizar AWS-ENDPOINTS.md
    "fundacion": 1902,
    "estadio_id": null
  }'
```

**Test 3: Fargate - GET**
```powershell
curl http://[TU-FARGATE-IP]:8000/
```

**Test 4: Verificar Swagger UI**
```
Abrir en navegador:
- https://[LAMBDA-URL]/docs
### Paso 5.2: Testing completo (solo Lambda)s
```

**Test 5: Healthcheck**
```powershell
# Lambda
curl https://[LAMBDA-URL]/health

# Fargate
curl http://[FARGATE-IP]:8000/health
```

---

## ✅ CHECKLIST FINAL

- [ ] RDS PostgreSQL creada y accesible
- [ ] 6 repositorios ECR creados
- [ ] 6 imágenes Docker en ECR
- [ ] GitHub Actions ejecutándose correctamente
**Test 3: Verificar Swagger UI**
```
Abrir en navegador:
- https://[LAMBDA-URL]/docs
```

**Test 4: Healthcheck**
```powershell
curl https://[LAMBDA-URL]/health
# Debe responder: {"status":"healthy","service":"equipos"}
## 🎉 ¡PROYECTO COMPLETADO SIN COSTO!

Has desplegado exitosamente el CRUD Soccer en AWS usando:
- ✅ Deployment manual con PowerShell (sin GitHub Actions)
- ✅ Amazon ECR (6 imágenes Docker)
- ✅ AWS Lambda (6 funciones serverless - **GRATIS**)
- ✅ AWS ECS/Fargate (configuración creada, sin ejecutar - **GRATIS**)
- ✅ Amazon RDS PostgreSQL (base de datos compartida - **GRATIS en Free Tier**)

**Costo total: $0/mes** 🎊
curl https://[JUGADORES-URL]/health
## 📸 Screenshots para portfolio/demo

Captura pantallas de:
1. AWS CLI: `aws sts get-caller-identity` (mostrar que tienes acceso)
2. ECR con las 6 imágenes (probar conocimiento de registry)
3. Lambda functions listadas en Console (6 funciones)
4. Lambda function URL respondiendo (Swagger UI)
5. ECS Cluster creado (demostrar conocimiento)
6. Task Definitions creadas (configuración sin ejecutar)
7. RDS database activa
8. Postman/curl con requests exitosos a Lambda
9. PowerShell con comandos de deployment manual

## 🧹 Limpieza (cuando termines la demo)

**Importante: Eliminar recursos para no usar Free Tier en el futuro**

```powershell
# 1. Eliminar funciones Lambda (NO generan cargo, pero limpiar)
# Lambda no cobra por tener funciones, solo por invocaciones portfolio

**Costos totales: $0/mes (dentro de Free Tier)**
---

## 🧹 Limpieza (cuando termines la demo)

**Para evitar cargos:**
```powershell
# 1. Detener servicios ECS
aws ecs update-service --cluster soccer-cluster --service soccer-equipos-service --desired-count 0 --region us-east-1
# Repetir para cada servicio

# 2. Eliminar servicios ECS (esperar que desired count = 0)
aws ecs delete-service --cluster soccer-cluster --service soccer-equipos-service --force --region us-east-1

# 3. Eliminar funciones Lambda
aws lambda delete-function --function-name soccer-equipos-lambda --region us-east-1
# Repetir para cada función
# 6. Eliminar ECS Cluster (no tiene cargos si no hay services)
aws ecs delete-cluster --cluster soccer-cluster --region us-east-1
```

**O desde Console (más fácil):**
- Lambda → Seleccionar todas → Actions → Delete
- ECR → Repositories → Seleccionar todos → Delete
- RDS → Delete database → Skip final snapshot (es demo)
- ECS → Clusters → Delete cluster
- CloudWatch → Logs → Eliminar log groups /ecs/* y /aws/lambda/*
---

## 🎓 Lo que demuestras con este proyecto

**Habilidades técnicas:**
1. ✅ **Containerización**: Docker, Dockerfiles, multi-stage builds
2. ✅ **AWS Lambda**: Serverless, Function URLs, container images
3. ✅ **Amazon ECR**: Registry privado, gestión de imágenes
4. ✅ **AWS ECS/Fargate**: Configuración (aunque no ejecutes)
5. ✅ **RDS**: Bases de datos gestionadas, PostgreSQL
6. ✅ **AWS CLI**: Automatización, scripting
7. ✅ **IaC conceptos**: Deployment scripts, configuración como código
8. ✅ **Networking**: Security groups, VPCs, IPs públicas
9. ✅ **Cost optimization**: Free Tier, estrategia de costos

**Respuestas para entrevistas:**
- "Implementé toda la arquitectura en Free Tier para demostrar conocimiento sin generar costos"
- "Usé Lambda para deployment productivo ($0) y configuré Fargate como alternativa"
- "Automaticé deployment con scripts PowerShell en lugar de CI/CD para reducir complejidad"
- "El proyecto completo corre por $0/mes durante 12 meses de Free Tier"

---

**Tiempo total estimado: 1.5-2 horas** (sin GitHub Actions es más rápido)

**Costo total: $0/mes** 💰

**¡Buena suerte con el deployment!** 🚀

**⚠️ Recursos que SÍ pueden generar cargo mínimo:**
- RDS después de 750 horas/mes (25 horas/día × 30 días)
- ECR después de 500MB
- Data transfer (generalmente incluido)
aws rds delete-db-instance --db-instance-identifier soccer-db --skip-final-snapshot --region us-east-1

# 7. Eliminar ECS Cluster
aws ecs delete-cluster --cluster soccer-cluster --region us-east-1
```

**O desde Console:**
- ECS → Delete services → Delete cluster
- Lambda → Delete functions
- ECR → Delete repositories
- RDS → Delete database (sin snapshot final para demo)

---

**Tiempo total estimado: 2-3 horas**

**¡Buena suerte con el deployment!** 🚀
