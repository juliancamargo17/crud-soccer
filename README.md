# CRUD Soccer - Microservices Architecture

Sistema de gestión de fútbol con arquitectura de microservicios desplegado en AWS Lambda y Fargate usando GitHub Container Registry.

## Arquitectura

**6 Microservicios independientes:**
- **Equipos** - Gestión de equipos de fútbol
- **Estadios** - Administración de estadios
- **DTs** - Directores técnicos
- **Jugadores** - Gestión de jugadores
- **Participaciones** - Participaciones en torneos
- **Torneos** - Administración de torneos

## Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLModel** - ORM basado en Pydantic y SQLAlchemy
- **PostgreSQL** - Base de datos relacional
- **Mangum** - Adapter para ejecutar FastAPI en AWS Lambda

### Infraestructura
- **AWS Lambda** - Serverless compute (6 funciones desplegadas)
- **Amazon ECR** - Container registry para Lambda images
- **Amazon RDS** - PostgreSQL managed database (Free Tier)
- **GitHub Container Registry (GHCR)** - Registry de imágenes Fargate
- **GitHub Actions** - CI/CD automatizado (dual pipeline)

### Contenedores
- **Docker** - Containerización de servicios
- **Multi-stage builds** - Optimización de imágenes

## Seguridad y Hardening

- Se eliminaron credenciales hardcodeadas del repositorio y se migró la gestión de contraseñas a **AWS Secrets Manager** para despliegues en **ECS/Fargate**.
- Se reforzó la configuración para fallar de forma explícita cuando faltan variables sensibles, evitando defaults inseguros en tiempo de ejecución.
- Se reescribió el historial de Git para purgar secretos previamente expuestos y se aplicó push protegido con `--force-with-lease`.
- Se añadieron scripts de automatización para crear/actualizar secretos y propagar su ARN a task definitions, reduciendo riesgo operativo y errores manuales.

## Prerequisitos

- Python 3.11+
- Docker
- AWS CLI configurado
- Cuenta GitHub
- Cuenta AWS (Free Tier)

## Configuración Local

### 1. Clonar repositorio
```bash
git clone https://github.com/juliancamargo17/crud-soccer.git
cd crud-soccer
```

### 2. Variables de entorno
Crear `.env` en cada servicio:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=soccer_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Ejecutar con Docker Compose
```bash
docker-compose up -d
```

### 4. Acceder a servicios
- Equipos: http://localhost/equipo/docs
- Estadios: http://localhost/estadio/docs
- DTs: http://localhost/dt/docs
- Jugadores: http://localhost/jugador/docs
- Participaciones: http://localhost/participacion/docs
- Torneos: http://localhost/torneo/docs

## Deployment en AWS

### Estado Actual: DESPLEGADO Y FUNCIONAL

**Endpoints de producción:** Ver [AWS-ENDPOINTS.md](AWS-ENDPOINTS.md)

### Arquitectura de Deployment
1. **GitHub Actions** - Construye imágenes automáticamente en cada push
2. **Dual Pipeline**:
   - Job 1: Imágenes Fargate → GHCR (demo)
   - Job 2: Imágenes Lambda → Amazon ECR (producción)
3. **AWS Lambda** - 6 funciones con Function URLs públicas
4. **Amazon ECR** - Almacena imágenes Lambda (~480 MB total)
5. **Amazon RDS** - PostgreSQL compartido (crud-soccer-db)

### Infrastructure as Code

Scripts automatizados para provisionar y gestionar infraestructura:

```bash
# Crear RDS PostgreSQL
cd infra/scripts
./create-rds.sh

# Desplegar servicio en Fargate (demo)
./deploy-fargate.sh estadios

# Limpiar recursos temporales
./cleanup.sh
```

**Documentación completa:** [infra/scripts/README.md](infra/scripts/README.md)

**¿Por qué scripts bash?**
- Reproducibles - Cualquiera puede replicar la infraestructura
- Versionados - Infrastructure as Code en git
- Transparentes - Comandos AWS CLI literales
- Documentación ejecutable - No puede quedar desactualizada

### Costos Reales
- **Lambda**: $0.00/mes (Free Tier - 1M requests)
- **ECR**: $0.00/mes (480 MB < 500 MB Free Tier)
- **GHCR**: $0.00/mes (ilimitado para públicos)
- **RDS**: $0.00/mes (Free Tier - 750 hrs/mes)
- **GitHub Actions**: $0.00/mes (2000 min/mes gratis)

**Total actual: $0.00/mes** 

## CI/CD Pipeline

```
Push a main → GitHub Actions
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
   Build Fargate          Build Lambda
        ↓                       ↓
      GHCR                    ECR
        ↓                       ↓
      demo                  AWS Lambda
```

### Workflow automático:
1. **Trigger**: Push a rama `main` o ejecución manual
2. **Job Fargate**: Construye 6 imágenes → GHCR (públicas)
3. **Job Lambda**: Construye 6 imágenes → ECR (para Lambda)
4. **Deployment**: Lambda usa imágenes de ECR automáticamente
5. **Secrets**: AWS credentials y DB password desde GitHub Secrets

## API Endpoints

Cada servicio expone:
- `GET /health` - Healthcheck
- `GET /docs` - Swagger UI
- `GET /{resource}/` - Listar todos
- `GET /{resource}/{id}` - Obtener por ID
- `POST /{resource}/` - Crear nuevo
- `PUT /{resource}/{id}` - Actualizar
- `DELETE /{resource}/{id}` - Eliminar

## Estructura del Proyecto

```
crud-soccer/
├── .github/workflows/
│   └── deploy-ghcr.yml          # CI/CD dual pipeline (GHCR + ECR)
├── infra/                        # Infrastructure as Code
│   ├── scripts/
│   │   ├── create-rds.sh        # Script para crear RDS PostgreSQL
│   │   ├── deploy-fargate.sh    # Script para desplegar en Fargate
│   │   ├── cleanup.sh           # Script de limpieza de recursos
│   │   └── README.md            # Documentación de scripts
│   └── task/
│       └── fargate-task-definition.json  # Configuración Fargate
├── classEquipo/                  # Servicio Equipos
│   ├── app/
│   │   ├── lambda_handler.py    # Handler para Lambda
│   │   ├── main.py              # FastAPI app
│   │   ├── routes/
│   │   └── schemas/
│   ├── Dockerfile               # Para Fargate/local
│   ├── Dockerfile.lambda        # Para AWS Lambda
│   └── requirements.txt
├── estadio/                      # Servicio Estadios
├── dt/                           # Servicio DTs
├── jugador/                      # Servicio Jugadores
├── participacion/                # Servicio Participaciones
├── torneo/                       # Servicio Torneos
├── database/
│   └── database.py              # Configuración DB
├── models/
│   └── models.py                # SQLModel models
├── .gitignore                   # Seguridad (credentials)
├── AWS-ENDPOINTS.md             # URLs de producción
├── docker-compose.yml           # Desarrollo local
├── nginx.conf                   # Proxy config
└── README.md
```

## Testing

### Lambda Endpoints
```bash
# Healthcheck
curl https://ffgrl6q2fgdzl4rl7wb5exzbcq0wqaus.lambda-url.us-east-1.on.aws/health
# Respuesta: {"status":"healthy","service":"equipos"}

# Swagger UI
https://ffgrl6q2fgdzl4rl7wb5exzbcq0wqaus.lambda-url.us-east-1.on.aws/docs
```

### Fargate Endpoints (Demo)
```bash
# Estadios en Fargate
# Health: http://3.87.126.10:8000/health
# Swagger: http://3.87.126.10:8000/docs
# API: http://3.87.126.10:8000/estadios/
```

**Ver todas las URLs:** [AWS-ENDPOINTS.md](AWS-ENDPOINTS.md)