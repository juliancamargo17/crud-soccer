# Guía Despliegue AWS: Lambda + Fargate + GHCR + GitHub Actions

## 🎯 Arquitectura (según DevOps)

```
GitHub Repository
       ↓
GitHub Actions (CI/CD) ←→ GRATIS
       ↓
GitHub Container Registry (GHCR) ←→ GRATIS (ilimitado público)
       ↓
    ┌──────────────┬─────────────┐
    ↓              ↓             ↓
AWS Lambda    AWS Fargate    Amazon RDS
(6 servicios)  (demo 10s)   (PostgreSQL)
   GRATIS       $0.01          GRATIS
```

## 💰 Costos: ~$0/mes

- ✅ GitHub Container Registry: **Gratis** (público ilimitado)
- ✅ GitHub Actions: **Gratis** (2000 min/mes)
- ✅ AWS Lambda: **Gratis** (1M requests/mes, 400K GB-seg)
- ✅ AWS Fargate: **$0.01** por task demo de 10 segundos
- ✅ RDS PostgreSQL: **Gratis** (750 horas/mes Free Tier)
- ❌ **NO Load Balancer** (cobraría $16/mes)

---

## FASE 1: Preparación AWS (30 min)

### 1.1 Configurar AWS CLI

```powershell
# Instalar AWS CLI si no lo tienes
winget install Amazon.AWSCLI

# Configurar credenciales
aws configure
# AWS Access Key ID: [TU ACCESS KEY]
# AWS Secret Access Key: [TU SECRET KEY]
# Default region: us-east-1
# Default output format: json

# Verificar
aws sts get-caller-identity
# Debe mostrar tu Account ID
```

### 1.2 Crear RDS PostgreSQL

```
1. AWS Console → RDS → Create database
2. PostgreSQL 15
3. Templates: Free tier
4. DB identifier: soccer-db
5. Master username: postgres
6. Master password: Soccer2025!
7. DB instance class: db.t3.micro
8. Storage: 20 GB gp3
9. Public access: Yes
10. VPC security group: Crear nuevo "soccer-db-sg"
11. Initial database name: postgres
12. Create database (esperar 10 min)
```

**Configurar Security Group:**
```
RDS → soccer-db → Security group → Edit inbound rules
Add rule: PostgreSQL (5432) from 0.0.0.0/0
```

**Guardar endpoint:**
```
soccer-db.xxxxx.us-east-1.rds.amazonaws.com
```

---

## FASE 2: Configurar GitHub (25 min)

### 2.1 Crear repositorio GitHub

```
1. GitHub → New repository
2. Repository name: crud-soccer
3. Visibility: Public (GHCR gratis ilimitado)
4. Create repository
```

### 2.2 Crear GitHub PAT para GHCR

```
1. GitHub → Settings (perfil) → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Note: "CRUD Soccer GHCR"
5. Scopes:
   ☑ write:packages
   ☑ read:packages
6. Generate token
7. COPIAR: ghp_xxxxxxxxxxxxxxxxx
```

### 2.3 Configurar Secrets del repositorio

```
Repositorio → Settings → Secrets and variables → Actions
New repository secret (crear 5):

1. AWS_ACCESS_KEY_ID: [TU IAM ACCESS KEY]
2. AWS_SECRET_ACCESS_KEY: [TU IAM SECRET KEY]
3. AWS_REGION: us-east-1
4. DB_HOST: [ENDPOINT DE RDS]
5. DB_PASSWORD: Soccer2025!
```

### 2.4 Inicializar Git local

```powershell
cd "C:\Users\juli1\OneDrive\Documentos\CRUD SOCCER"

git init
git remote add origin https://github.com/TU-USUARIO/crud-soccer.git

# Verificar
git remote -v
```

---

## FASE 3: Actualizar GitHub Actions Workflow (10 min)

El workflow actual (`.github/workflows/deploy-ecr.yml`) debe cambiar a GHCR.

**Crear nuevo workflow:**

```powershell
# Eliminar workflow viejo de ECR
Remove-Item ".github\workflows\deploy-ecr.yml"
```

Ahora voy a crear el workflow correcto para GHCR + Lambda + Fargate...

---

## FASE 4: Deploy a Lambda con GHCR (30 min)

### 4.1 Hacer imágenes públicas en GHCR

```
Importante: Lambda necesita que las imágenes GHCR sean públicas

1. GitHub → Tu repo → Packages
2. Click en cada package (equipos, estadios, etc.)
3. Package settings → Change visibility → Public
4. Repetir para los 6 packages
```

### 4.2 Crear función Lambda desde GHCR

```
1. Lambda → Create function
2. Container image
3. Function name: soccer-equipos-lambda
4. Container image URI: ghcr.io/TU-USUARIO/crud-soccer-equipos:latest
5. Browse images → External registry
6. Pegar URI y Continue
7. Create function

8. Configuration → General configuration:
   - Memory: 512 MB
   - Timeout: 30 seconds

9. Configuration → Environment variables:
   - DB_HOST: [RDS ENDPOINT]
   - DB_USER: postgres
   - DB_PASSWORD: Soccer2025!
   - DB_NAME: postgres
   - DB_PORT: 5432

10. Configuration → Function URL:
    - Create function URL
    - Auth type: NONE
    - Save
    - COPIAR URL

11. Probar:
    curl https://[FUNCTION-URL]/health
```

Repetir para los 6 servicios.

---

## FASE 5: Demo Fargate ($0.01) (30 min)

### 5.1 Crear ECS Cluster

```
1. ECS → Clusters → Create cluster
2. Cluster name: soccer-cluster
3. Infrastructure: AWS Fargate
4. Create
```

### 5.2 Crear Task Definition

```
1. ECS → Task Definitions → Create new
2. Family: soccer-demo-task
3. Launch type: Fargate
4. CPU: 0.25 vCPU
5. Memory: 0.5 GB
6. Task role: ecsTaskExecutionRole
7. Container:
   - Name: equipos
   - Image: ghcr.io/TU-USUARIO/crud-soccer-equipos:latest
   - Port: 8000
   - Environment variables: (mismas que Lambda)
8. Create
```

### 5.3 Ejecutar Task de demostración (10 segundos)

```
1. ECS → Clusters → soccer-cluster
2. Tasks → Run new task
3. Launch type: Fargate
4. Task definition: soccer-demo-task
5. VPC: Default
6. Subnets: Públicas
7. Security group: Permitir 8000
8. Public IP: ENABLED
9. Run task

10. Esperar a que task esté RUNNING
11. Copiar Public IP
12. Probar: curl http://[IP]:8000/health

13. IMPORTANTE: Stop task después de probar
    (Costo: ~$0.01 por 10 segundos)
```

**Después de la demo:**
```
Tasks → Select task → Stop
```

Costo total de la demo: **$0.01**

---

## FASE 6: Testing y Documentación (15 min)

### Test completo

```powershell
# Lambda - Health checks
curl https://[LAMBDA-URL-EQUIPOS]/health
curl https://[LAMBDA-URL-ESTADIOS]/health
# ... todos los 6

# Lambda - Swagger UI
https://[LAMBDA-URL]/docs

# Lambda - POST test
curl -X POST https://[LAMBDA-URL]/ `
  -H "Content-Type: application/json" `
  -d '{
    "nombre": "Real Madrid",
    "pais": "España",
    "ciudad": "Madrid",
    "fundacion": 1902,
    "estadio_id": null
  }'
```

### Actualizar AWS-ENDPOINTS.md

Documentar todas las URLs de Lambda.

---

## ✅ Checklist Final

- [ ] RDS PostgreSQL creada (Free Tier)
- [ ] Repositorio GitHub creado
- [ ] GitHub Actions ejecutado correctamente
- [ ] 6 imágenes en GHCR (públicas)
- [ ] 6 funciones Lambda funcionando
- [ ] ECS Cluster + Task Definition creados
- [ ] Fargate task ejecutada y detenida ($0.01)
- [ ] Todos los healthchecks OK
- [ ] Swagger UI funcionando
- [ ] POST/GET probados
- [ ] Screenshots tomados

---

## 🎓 Cumplimiento con DevOps

✅ **AWS Lambda**: 6 servicios serverless desde contenedores GHCR
✅ **AWS Fargate**: Task demo ejecutada y detenida
✅ **GitHub Container Registry**: Imágenes públicas
✅ **GitHub Actions**: CI/CD automático
❌ **Sin ALB**: Como solicitó

**Costo total: $0.01** (solo la demo de Fargate)

---

## 🧹 Limpieza

```powershell
# Lambda (no cobra por existir, solo por invocaciones)
# Dejar activas si quieres seguir demostrando

# Fargate (ya está detenido = $0)

# RDS (eliminar al finalizar demo)
aws rds delete-db-instance --db-instance-identifier soccer-db --skip-final-snapshot

# ECS Cluster
aws ecs delete-cluster --cluster soccer-cluster

# GHCR packages (dejar, son gratis)
```

---

## 📸 Screenshots para DevOps

1. GitHub Actions workflow completado
2. GHCR con 6 packages públicos
3. Lambda functions listadas
4. Lambda Function URL funcionando
5. ECS Cluster con Task Definition
6. Fargate task ejecutándose (antes de detener)
7. RDS database
8. Swagger UI desde Lambda
9. Postman con requests exitosos

---

**Tiempo total: 2.5 horas**
**Costo total: $0.01**
