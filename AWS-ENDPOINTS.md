# AWS Deployment Endpoints

## 🌐 Servicios desplegados

Este documento contiene los endpoints de acceso a los microservicios del CRUD Soccer desplegados en AWS.

---

## 📍 AWS Lambda (Function URLs)

### Equipos
- **URL**: `https://[PENDING].lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://[PENDING].lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://[PENDING].lambda-url.us-east-1.on.aws/health`

### Estadios
- **URL**: `https://[PENDING].lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://[PENDING].lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://[PENDING].lambda-url.us-east-1.on.aws/health`

### DTs
- **URL**: `https://[PENDING].lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://[PENDING].lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://[PENDING].lambda-url.us-east-1.on.aws/health`

### Jugadores
- **URL**: `https://[PENDING].lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://[PENDING].lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://[PENDING].lambda-url.us-east-1.on.aws/health`

### Participaciones
- **URL**: `https://[PENDING].lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://[PENDING].lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://[PENDING].lambda-url.us-east-1.on.aws/health`

### Torneos
- **URL**: `https://[PENDING].lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://[PENDING].lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://[PENDING].lambda-url.us-east-1.on.aws/health`

---

## 🚀 AWS Fargate (ECS Services)

### Equipos
- **URL**: `http://[IP-PENDING]:8000/`
- **Swagger**: `http://[IP-PENDING]:8000/docs`
- **Health**: `http://[IP-PENDING]:8000/health`

### Jugadores
- **URL**: `http://[IP-PENDING]:8000/`
- **Swagger**: `http://[IP-PENDING]:8000/docs`
- **Health**: `http://[IP-PENDING]:8000/health`

### Torneos
- **URL**: `http://[IP-PENDING]:8000/`
- **Swagger**: `http://[IP-PENDING]:8000/docs`
- **Health**: `http://[IP-PENDING]:8000/health`

---

## 🗄️ Base de datos

### Amazon RDS PostgreSQL
- **Endpoint**: `[PENDING].us-east-1.rds.amazonaws.com`
- **Puerto**: `5432`
- **Database**: `postgres`
- **Usuario**: `postgres`
- **Contraseña**: `[CONFIGURADO EN SECRETS]`

---

## 📦 Amazon ECR Repositories

- `[ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/soccer/equipos`
- `[ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/soccer/estadios`
- `[ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/soccer/dts`
- `[ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/soccer/jugadores`
- `[ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/soccer/participaciones`
- `[ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/soccer/torneos`

---

## 🧪 Ejemplos de uso

### Lambda - GET todos los equipos
```bash
curl https://[YOUR-LAMBDA-URL].lambda-url.us-east-1.on.aws/
```

### Lambda - POST crear equipo
```bash
curl -X POST https://[YOUR-LAMBDA-URL].lambda-url.us-east-1.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Real Madrid",
    "pais": "España",
    "ciudad": "Madrid",
    "fundacion": 1902,
    "estadio_id": null
  }'
```

### Fargate - GET todos los equipos
```bash
curl http://[YOUR-FARGATE-IP]:8000/
```

### Fargate - Acceder a Swagger UI
```
http://[YOUR-FARGATE-IP]:8000/docs
```

### Healthcheck
```bash
curl https://[YOUR-LAMBDA-URL].lambda-url.us-east-1.on.aws/health
# Respuesta: {"status":"healthy","service":"equipos"}
```

---

## 🔄 Actualización de endpoints

Este archivo se actualizará después de completar el despliegue con las URLs e IPs reales.

### Instrucciones para obtener URLs:

**Lambda Function URLs:**
1. AWS Console → Lambda → Functions
2. Seleccionar función (ej: soccer-equipos-lambda)
3. Configuration → Function URL → Copiar URL

**Fargate IPs públicas:**
1. AWS Console → ECS → Clusters → soccer-cluster
2. Services → Seleccionar servicio
3. Tasks → Click en Task ID
4. Network → Copiar Public IP

**RDS Endpoint:**
1. AWS Console → RDS → Databases
2. Seleccionar soccer-db
3. Connectivity & security → Copiar Endpoint

---

## 📊 Arquitectura

```
GitHub Actions (CI/CD)
       ↓
   Amazon ECR (Registry)
       ↓
    ┌──────────────┬─────────────┐
    ↓              ↓             ↓
AWS Lambda    AWS Fargate    Amazon RDS
(6 services)  (3 services)   (PostgreSQL)
```

---

## 📝 Notas

- **Lambda**: Serverless, pago por uso, ideal para cargas esporádicas
- **Fargate**: Contenedores persistentes, IPs pueden cambiar al reiniciar
- **RDS**: Base de datos compartida por todos los servicios
- **ECR**: Imágenes Docker versionadas con tags `latest` y commit SHA
- **GitHub Actions**: Deployment automático en cada push a main

---

**Última actualización**: [PENDIENTE - Completar después del despliegue]
