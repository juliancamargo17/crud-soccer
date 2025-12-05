# ✅ Plan Aprobado: Lambda + Fargate + GHCR + GitHub Actions

## 🎯 Cumple 100% con requisitos de DevOps

Tu DevOps pidió:
- ✅ AWS Lambda
- ✅ AWS Fargate  
- ✅ GitHub Container Registry (GHCR)
- ✅ GitHub Actions

## 💰 Costo Final: **$0.00 - $0.10/mes**

| Servicio | Costo | Notas |
|----------|-------|-------|
| GitHub Container Registry | **$0.00** | Gratis ilimitado (público) |
| GitHub Actions | **$0.00** | 2000 min/mes gratis |
| AWS Lambda (6 funciones) | **$0.00** | 1M requests/mes gratis |
| AWS Fargate (demo) | **$0.01** | Task de 10 seg, luego detener |
| RDS PostgreSQL | **$0.00** | 750 hrs/mes Free Tier |
| **TOTAL** | **~$0.01/mes** | Prácticamente gratis |

## 🏗️ Arquitectura Final

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Repository                      │
│                    (código fuente)                       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions (CI/CD)                      │
│  • Build: Construye 6 imágenes Docker                   │
│  • Push: Sube a GHCR automáticamente                    │
│  • Trigger: Cada push a main                            │
│  • Costo: $0 (2000 min/mes gratis)                      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│       GitHub Container Registry (GHCR)                   │
│  • 6 imágenes públicas                                   │
│  • ghcr.io/usuario/crud-soccer-equipos:latest           │
│  • ghcr.io/usuario/crud-soccer-estadios:latest          │
│  • ghcr.io/usuario/crud-soccer-dts:latest               │
│  • ghcr.io/usuario/crud-soccer-jugadores:latest         │
│  • ghcr.io/usuario/crud-soccer-participaciones:latest   │
│  • ghcr.io/usuario/crud-soccer-torneos:latest           │
│  • Costo: $0 (ilimitado para públicos)                  │
└──────────────┬──────────────────┬────────────────────────┘
               │                  │
               ↓                  ↓
    ┌──────────────────┐  ┌──────────────────┐
    │   AWS Lambda     │  │  AWS Fargate     │
    │  (Production)    │  │  (Demo Only)     │
    ├──────────────────┤  ├──────────────────┤
    │ • 6 funciones    │  │ • 1 task demo    │
    │ • Serverless     │  │ • Ejecuta 10s    │
    │ • Function URLs  │  │ • Se detiene     │
    │ • Costo: $0      │  │ • Costo: $0.01   │
    └────────┬─────────┘  └──────────────────┘
             │
             ↓
    ┌──────────────────┐
    │  Amazon RDS      │
    │  PostgreSQL      │
    ├──────────────────┤
    │ • db.t3.micro    │
    │ • 20 GB storage  │
    │ • Free Tier      │
    │ • Costo: $0      │
    └──────────────────┘
```

## 📋 Checklist de Implementación

### FASE 1: Preparación (30 min)
- [ ] Configurar AWS CLI con credenciales
- [ ] Crear RDS PostgreSQL (Free Tier)
- [ ] Guardar endpoint de RDS

### FASE 2: GitHub Setup (25 min)
- [ ] Crear repositorio GitHub (público)
- [ ] Crear Personal Access Token para GHCR
- [ ] Configurar 5 secrets en el repositorio:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_REGION
  - DB_HOST
  - DB_PASSWORD
- [ ] Inicializar Git local

### FASE 3: Primer Deployment (30 min)
- [ ] Commit y push del código
- [ ] Verificar GitHub Actions ejecutándose
- [ ] Esperar a que termine (15 min aprox)
- [ ] Verificar 6 imágenes en GHCR
- [ ] Hacer packages públicos

### FASE 4: AWS Lambda (40 min)
- [ ] Crear función Lambda para equipos
- [ ] Configurar Function URL
- [ ] Configurar variables de entorno
- [ ] Probar /health y /docs
- [ ] Repetir para los 5 servicios restantes
- [ ] Probar POST/GET en todos

### FASE 5: AWS Fargate Demo (30 min)
- [ ] Crear ECS Cluster
- [ ] Crear Task Definition
- [ ] Ejecutar task de demostración
- [ ] Probar por 5-10 minutos
- [ ] **Detener task** (importante)

### FASE 6: Documentación (15 min)
- [ ] Actualizar AWS-ENDPOINTS.md
- [ ] Tomar screenshots
- [ ] Documentar costos reales
- [ ] Preparar presentación para DevOps

**Tiempo total: 2.5 - 3 horas**

## 🎯 Diferencias con plan anterior

| Aspecto | Plan Anterior | Plan Nuevo (DevOps) |
|---------|---------------|---------------------|
| **Registry** | Amazon ECR | ✅ GitHub Container Registry |
| **CI/CD** | Manual/Script | ✅ GitHub Actions |
| **Lambda** | Desde ECR | ✅ Desde GHCR |
| **Fargate** | No ejecutar | ✅ Demo de 10s ($0.01) |
| **Costo GHCR** | ECR $0-0.10 | GHCR $0.00 |
| **Automatización** | Manual | ✅ Automática |
| **Deployment** | Local | ✅ Push to GitHub |

## 🚀 Ventajas de este Plan

### 1. **Sin costos de registry**
- ECR cobra después de 500MB
- GHCR gratis ilimitado para públicos

### 2. **CI/CD automático**
- Cada push → build → deploy automático
- No necesitas ejecutar comandos manualmente

### 3. **Portable**
- Imágenes en GitHub, no lockeado a AWS
- Podrías usar GCP, Azure sin cambiar registry

### 4. **Profesional**
- GitHub Actions es estándar de industria
- Demuestra conocimiento de CI/CD moderno

### 5. **Cumple requisitos**
- DevOps pidió Lambda + Fargate + GHCR + Actions
- Este plan cumple 100%

## 📊 Comparación de Costos

### Plan Anterior (ECR + Manual)
```
ECR Storage: $0.10/GB después de 500MB
Deployment: Manual (tiempo humano)
Total: $0.10 - $1.00/mes
```

### Plan Nuevo (GHCR + Actions)
```
GHCR: $0.00 (público ilimitado)
GitHub Actions: $0.00 (2000 min gratis)
Lambda: $0.00 (Free Tier)
Fargate demo: $0.01 (una vez)
RDS: $0.00 (Free Tier)
Total: $0.01 total (no recurrente)
```

**Ahorro: 90-99% vs plan anterior**

## ⚠️ Puntos Importantes

### Lambda desde GHCR

**Restricción de AWS Lambda:**
- Solo puede usar imágenes públicas de GHCR
- Las privadas requieren configuración compleja

**Solución:**
- Hacer packages públicos después de push
- O configurar ECR con copy desde GHCR (más complejo)

### Fargate = Demo Only

**Importante:**
- Fargate cobra por minuto ejecutando
- Para demo: ejecutar 10 segundos = $0.01
- **Luego DETENER task**
- No dejar corriendo = $0/mes

### Free Tier RDS

**Límites:**
- 750 horas/mes = 31 días × 24 hrs
- Si excedes: $15/mes aprox
- Para demo corta: sin problema

## 🎓 Para Presentar a DevOps

### Demostración exitosa de:

1. ✅ **GitHub Actions**: CI/CD pipeline funcional
2. ✅ **GHCR**: Registry con 6 imágenes
3. ✅ **Lambda**: 6 funciones serverless desde contenedores
4. ✅ **Fargate**: Task definition + demo ejecutada
5. ✅ **RDS**: Base de datos compartida
6. ✅ **Costo**: $0.01 total

### Screenshots clave:

1. GitHub Actions workflow completado
2. GHCR packages (6 imágenes públicas)
3. Lambda functions funcionando
4. Lambda Function URLs respondiendo
5. Swagger UI desde Lambda
6. ECS Task Definition
7. Fargate task ejecutándose
8. RDS database details
9. Billing dashboard ($0.00)

## 🆚 vs Alternativas

### ¿Por qué NO Docker en EC2?

```
EC2 t2.micro (Free Tier): 750 hrs/mes
Problema: Solo 1 instancia, no 6 servicios
Costo después Free Tier: $8-15/mes
```

### ¿Por qué NO ECS con EC2?

```
Requiere: EC2 + ECS + ALB
Mínimo: $16/mes (ALB) + $8/mes (EC2)
Total: $24/mes
```

### ¿Por qué SÍ Lambda + GHCR?

```
Lambda: Serverless, escala automático
GHCR: Gratis, ilimitado
Actions: Automático
Total: $0/mes
```

## 🔄 Flujo de Trabajo Diario

```
1. Haces cambios en código local
2. git add . && git commit -m "Update"
3. git push
4. GitHub Actions se activa automáticamente
5. Construye 6 imágenes
6. Pushea a GHCR
7. Lambda usa nuevas imágenes automáticamente*
8. Sin intervención manual

*Nota: Lambda cachea imágenes, puede requerir 
"Update function code" manual o configurar 
webhook para auto-update
```

## ✅ Confirmación Final

Este plan cumple **exactamente** con lo pedido:

- [x] AWS Lambda ← 6 funciones desde GHCR
- [x] AWS Fargate ← Task demo ejecutada
- [x] GHCR ← Registry con imágenes
- [x] GitHub Actions ← CI/CD automático
- [x] Sin ALB ← Como solicitó
- [x] Costo mínimo ← $0.01 total

**¿Procedemos con este plan?**

---

**Siguiente paso: Configurar AWS CLI**

```powershell
aws configure
```
