"""
Lambda handler para el servicio de Equipos
Adaptador Mangum para ejecutar FastAPI en AWS Lambda
"""
from mangum import Mangum
from app.main import app

# Handler que Lambda ejecutará
handler = Mangum(app)
