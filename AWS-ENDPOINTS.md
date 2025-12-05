# AWS Deployment Endpoints

## Servicios desplegados

Este documento contiene los endpoints de acceso a los microservicios del CRUD Soccer desplegados en AWS.

---

##  AWS Lambda (Function URLs)

### Equipos 
- **URL**: `https://ffgrl6q2fgdzl4rl7wb5exzbcq0wqaus.lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://ffgrl6q2fgdzl4rl7wb5exzbcq0wqaus.lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://ffgrl6q2fgdzl4rl7wb5exzbcq0wqaus.lambda-url.us-east-1.on.aws/health`

### Estadios 
- **URL**: `https://jxvduha7ri4b2sw7mf4hirs2ia0hykgs.lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://jxvduha7ri4b2sw7mf4hirs2ia0hykgs.lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://jxvduha7ri4b2sw7mf4hirs2ia0hykgs.lambda-url.us-east-1.on.aws/health`

### DTs 
- **URL**: `https://5n26ji6ftuvrxoljww2nr3q3by0bqbkl.lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://5n26ji6ftuvrxoljww2nr3q3by0bqbkl.lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://5n26ji6ftuvrxoljww2nr3q3by0bqbkl.lambda-url.us-east-1.on.aws/health`

### Jugadores 
- **URL**: `https://lxvf4z2bxs7gparrkaqotifk6q0ccvna.lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://lxvf4z2bxs7gparrkaqotifk6q0ccvna.lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://lxvf4z2bxs7gparrkaqotifk6q0ccvna.lambda-url.us-east-1.on.aws/health`

### Participaciones 
- **URL**: `https://iv3vwzolquk243pvthhfphgeta0dwjxq.lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://iv3vwzolquk243pvthhfphgeta0dwjxq.lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://iv3vwzolquk243pvthhfphgeta0dwjxq.lambda-url.us-east-1.on.aws/health`

### Torneos 
- **URL**: `https://ccbcul3ezi7r42szipbmmfqpfm0hjrnf.lambda-url.us-east-1.on.aws/`
- **Swagger**: `https://ccbcul3ezi7r42szipbmmfqpfm0hjrnf.lambda-url.us-east-1.on.aws/docs`
- **Health**: `https://ccbcul3ezi7r42szipbmmfqpfm0hjrnf.lambda-url.us-east-1.on.aws/health`

---

## AWS Fargate (ECS Services)

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

## Base de datos ✅

### Amazon RDS PostgreSQL
- **Endpoint**: `crud-soccer-db.c27m2g066462.us-east-1.rds.amazonaws.com`
- **Puerto**: `5432`
- **Database**: `soccer_db`
- **Usuario**: `postgres`
- **Contraseña**: `[CONFIGURADO EN SECRETS - RDS2025!]`
- **Estado**: Available (Free Tier - db.t3.micro)

---

## Amazon ECR Repositories ✅

- `288761759102.dkr.ecr.us-east-1.amazonaws.com/crud-soccer/equipos-lambda:latest`
- `288761759102.dkr.ecr.us-east-1.amazonaws.com/crud-soccer/estadios-lambda:latest`
- `288761759102.dkr.ecr.us-east-1.amazonaws.com/crud-soccer/dts-lambda:latest`
- `288761759102.dkr.ecr.us-east-1.amazonaws.com/crud-soccer/jugadores-lambda:latest`
- `288761759102.dkr.ecr.us-east-1.amazonaws.com/crud-soccer/participaciones-lambda:latest`
- `288761759102.dkr.ecr.us-east-1.amazonaws.com/crud-soccer/torneos-lambda:latest`

---

## GitHub Container Registry (GHCR) ✅

**Imágenes Fargate (públicas):**
- `ghcr.io/juliancamargo17/crud-soccer-equipos:latest`
- `ghcr.io/juliancamargo17/crud-soccer-estadios:latest`
- `ghcr.io/juliancamargo17/crud-soccer-dts:latest`
- `ghcr.io/juliancamargo17/crud-soccer-jugadores:latest`
- `ghcr.io/juliancamargo17/crud-soccer-participaciones:latest`
- `ghcr.io/juliancamargo17/crud-soccer-torneos:latest`

**Imágenes Lambda (públicas):**
- `ghcr.io/juliancamargo17/crud-soccer-equipos-lambda:latest`
- `ghcr.io/juliancamargo17/crud-soccer-estadios-lambda:latest`
- `ghcr.io/juliancamargo17/crud-soccer-dts-lambda:latest`
- `ghcr.io/juliancamargo17/crud-soccer-jugadores-lambda:latest`
- `ghcr.io/juliancamargo17/crud-soccer-participaciones-lambda:latest`
- `ghcr.io/juliancamargo17/crud-soccer-torneos-lambda:latest`

---

## Ejemplos de uso

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

## Arquitectura

```
GitHub Actions (CI/CD)
       ↓
   Amazon ECR (Registry)
       ↓
    ┌──────────────┬─────────────┐
    ↓              ↓             ↓
AWS Lambda    AWS Fargate    Amazon RDS
(6 services)  (6 services)   (PostgreSQL)
```

---

## Notas

- **Lambda**: Serverless, pago por uso, ideal para cargas esporádicas
- **Fargate**: Contenedores persistentes, IPs pueden cambiar al reiniciar
- **RDS**: Base de datos compartida por todos los servicios
- **ECR**: Imágenes Docker versionadas con tags `latest` y commit SHA
- **GitHub Actions**: Deployment automático en cada push a main

---

## 💰 Costos del Deployment

- **Lambda**: $0.00/mes (Free Tier - 1M requests)
- **ECR**: $0.00/mes (480 MB < 500 MB Free Tier)
- **GHCR**: $0.00/mes (ilimitado para públicos)
- **RDS**: $0.00/mes (Free Tier - 750 hrs/mes)
- **Fargate**: $0.01 (demo de 10 segundos) - NO EJECUTADO AÚN
- **GitHub Actions**: $0.00/mes (2000 min gratis)

**Total actual: $0.00/mes** ✅

---

**Última actualización**: December 5, 2025 - Deployment completado
**Estado**: ✅ Lambda Functions desplegadas y funcionales | ⏳ Fargate pendiente de demo
