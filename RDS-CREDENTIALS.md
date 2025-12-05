# 🗄️ RDS PostgreSQL - Credenciales

**⚠️ ARCHIVO SOLO LOCAL - NO SUBIR A GITHUB**

## Información de Conexión

```
Endpoint:   crud-soccer-db.c27m2g066462.us-east-1.rds.amazonaws.com
Puerto:     5432
Usuario:    postgres
Contraseña: CrudSoccer2024!
Base Datos: soccer_db
```

## Connection String

```
postgresql://postgres:CrudSoccer2024!@crud-soccer-db.c27m2g066462.us-east-1.rds.amazonaws.com:5432/soccer_db
```

## Variables de Entorno (para Lambda)

```
DB_HOST=crud-soccer-db.c27m2g066462.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=soccer_db
DB_USER=postgres
DB_PASSWORD=CrudSoccer2024!
```

## Estado

- ✅ Instancia creada: `crud-soccer-db`
- ✅ Estado: `available`
- ✅ Security Group: `sg-0f2f2b8096fe2a87b`
- ✅ Puerto 5432: Abierto
- ✅ Free Tier: db.t3.micro (750 hrs/mes)

## Próximos Pasos

1. ✅ RDS creado y disponible
2. ⏳ Configurar GitHub Secrets con estas credenciales
3. ⏳ Crear funciones Lambda
4. ⏳ Configurar variables de entorno en Lambda

---

**Fecha de creación:** December 5, 2025
**Región:** us-east-1
