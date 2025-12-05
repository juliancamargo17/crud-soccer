# ⚽ CRUD Soccer - Microservices Architecture

Sistema de gestión de fútbol con arquitectura de microservicios desplegado en AWS Lambda y Fargate usando GitHub Container Registry.

## 🏗️ Arquitectura

**6 Microservicios independientes:**
- 🏟️ **Equipos** - Gestión de equipos de fútbol
- 🏢 **Estadios** - Administración de estadios
- 👔 **DTs** - Directores técnicos
- ⚽ **Jugadores** - Gestión de jugadores
- 📊 **Participaciones** - Participaciones en torneos
- 🏆 **Torneos** - Administración de torneos

## 🚀 Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLModel** - ORM basado en Pydantic y SQLAlchemy
- **PostgreSQL** - Base de datos relacional
- **Mangum** - Adapter para ejecutar FastAPI en AWS Lambda

### Infraestructura
- **AWS Lambda** - Serverless compute (función por servicio)
- **AWS Fargate** - Contenedores ECS sin servidor
- **Amazon RDS** - PostgreSQL managed database
- **GitHub Container Registry (GHCR)** - Registry de imágenes Docker
- **GitHub Actions** - CI/CD automatizado

### Contenedores
- **Docker** - Containerización de servicios
- **Multi-stage builds** - Optimización de imágenes

## 📋 Prerequisitos

- Python 3.11+
- Docker
- AWS CLI configurado
- Cuenta GitHub
- Cuenta AWS (Free Tier)

## 🔧 Configuración Local

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
- Equipos: http://localhost:8001/docs
- Estadios: http://localhost:8002/docs
- DTs: http://localhost:8003/docs
- Jugadores: http://localhost:8004/docs
- Participaciones: http://localhost:8005/docs
- Torneos: http://localhost:8006/docs

## 🌩️ Deployment en AWS

### Documentación Completa
Ver [DEPLOYMENT-GUIDE-GHCR.md](DEPLOYMENT-GUIDE-GHCR.md) para instrucciones paso a paso.

### Resumen
1. **GitHub Actions** construye imágenes Docker automáticamente
2. **GHCR** almacena las imágenes (gratis ilimitado)
3. **Lambda** ejecuta contenedores desde GHCR (serverless)
4. **Fargate** opción alternativa para contenedores ECS
5. **RDS PostgreSQL** base de datos compartida (Free Tier)

### Costos Estimados
- GitHub Container Registry: **$0.00** (público ilimitado)
- GitHub Actions: **$0.00** (2000 min/mes gratis)
- AWS Lambda: **$0.00** (1M requests/mes gratis)
- AWS Fargate: **$0.01** (demo de 10 segundos)
- Amazon RDS: **$0.00** (Free Tier 750 hrs/mes)

**Total: ~$0.01/mes** 💰

## 🔄 CI/CD Pipeline

```
Push a main → GitHub Actions → Build → GHCR → AWS Lambda
```

### Workflow automático:
1. Detecta cambios en cada servicio
2. Construye imagen Docker
3. Pushea a GHCR (`ghcr.io/juliancamargo17/crud-soccer-{service}:latest`)
4. Lambda usa la nueva imagen automáticamente

## 📚 API Endpoints

Cada servicio expone:
- `GET /health` - Healthcheck
- `GET /docs` - Swagger UI
- `GET /{resource}/` - Listar todos
- `GET /{resource}/{id}` - Obtener por ID
- `POST /{resource}/` - Crear nuevo
- `PUT /{resource}/{id}` - Actualizar
- `DELETE /{resource}/{id}` - Eliminar

## 🏗️ Estructura del Proyecto

```
crud-soccer/
├── .github/workflows/
│   └── deploy-ghcr.yml          # CI/CD pipeline
├── classEquipo/                  # Servicio Equipos
│   ├── app/
│   │   ├── lambda_handler.py    # Handler para Lambda
│   │   ├── main.py              # FastAPI app
│   │   ├── routes/
│   │   └── schemas/
│   ├── Dockerfile
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
├── docker-compose.yml           # Local development
├── DEPLOYMENT-GUIDE-GHCR.md     # Guía de deployment
└── README.md
```

## 🧪 Testing

### Healthcheck
```bash
curl https://your-lambda-url/health
```

### Crear equipo
```bash
curl -X POST "https://your-lambda-url/equipos/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Real Madrid", "ciudad": "Madrid"}'
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es open source y está disponible bajo la [MIT License](LICENSE).

## 👤 Autor

**Julian Camargo**
- GitHub: [@juliancamargo17](https://github.com/juliancamargo17)
- Email: juliancamargo17@gmail.com

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- AWS por los servicios en la nube
- GitHub por GHCR y Actions gratuitos
- SQLModel por el ORM moderno

---

⭐ Si este proyecto te ayudó, dale una estrella en GitHub!
