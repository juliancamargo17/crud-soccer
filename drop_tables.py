import psycopg2

# Conectar a RDS
conn = psycopg2.connect(
    host='crud-soccer-db.c27m2g066462.us-east-1.rds.amazonaws.com',
    database='postgres',
    user='postgres',
    password='REDACTED',
    port=5432
)

cur = conn.cursor()

# Eliminar todas las tablas
tables = ['participacion', 'jugador', 'torneo', 'dt', 'equipo', 'estadio']
for table in tables:
    cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
    print(f'✅ Tabla {table} eliminada')

conn.commit()
cur.close()
conn.close()

print('\n✅ Todas las tablas eliminadas correctamente')
