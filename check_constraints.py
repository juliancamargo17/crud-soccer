import psycopg2

conn = psycopg2.connect(
    host='crud-soccer-db.c27m2g066462.us-east-1.rds.amazonaws.com',
    database='postgres',
    user='postgres',
    password='REDACTED',
    port=5432
)

cur = conn.cursor()

# Verificar constraints en la tabla estadio
cur.execute("""
    SELECT constraint_name, constraint_type 
    FROM information_schema.table_constraints 
    WHERE table_name = 'estadio'
""")

constraints = cur.fetchall()
print("Constraints en tabla estadio:")
for c in constraints:
    print(f"  - {c[0]}: {c[1]}")

cur.close()
conn.close()
