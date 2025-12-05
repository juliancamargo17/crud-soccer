# Script de Deployment Manual a AWS
# Ejecutar después de configurar AWS CLI con: aws configure

param(
    [string]$Region = "us-east-1",
    [string]$AccountId = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CRUD Soccer - Manual AWS Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ([string]::IsNullOrEmpty($AccountId)) {
    Write-Host "ERROR: Debes proporcionar tu AWS Account ID" -ForegroundColor Red
    Write-Host "Uso: .\deploy-manual.ps1 -AccountId 123456789012" -ForegroundColor Yellow
    exit 1
}

$EcrRegistry = "$AccountId.dkr.ecr.$Region.amazonaws.com"
$Services = @("equipos", "estadios", "dts", "jugadores", "participaciones", "torneos")
$Paths = @{
    "equipos" = "classEquipo"
    "estadios" = "estadio"
    "dts" = "dt"
    "jugadores" = "jugador"
    "participaciones" = "participacion"
    "torneos" = "torneo"
}

Write-Host "Configuración:" -ForegroundColor Green
Write-Host "  Region: $Region"
Write-Host "  Account ID: $AccountId"
Write-Host "  ECR Registry: $EcrRegistry"
Write-Host ""

# Paso 1: Login a ECR
Write-Host "[1/4] Autenticando con Amazon ECR..." -ForegroundColor Yellow
$LoginCommand = aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $EcrRegistry
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Falló la autenticación con ECR" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Autenticación exitosa" -ForegroundColor Green
Write-Host ""

# Paso 2: Build y Push de imágenes
Write-Host "[2/4] Construyendo y subiendo imágenes Docker..." -ForegroundColor Yellow
foreach ($Service in $Services) {
    $ServicePath = $Paths[$Service]
    $RepoName = "soccer/$Service"
    $ImageUri = "$EcrRegistry/$RepoName"
    
    Write-Host "  → Procesando: $Service" -ForegroundColor Cyan
    
    # Build
    Write-Host "    Building..." -NoNewline
    docker build -f "./$ServicePath/Dockerfile" -t "$RepoName`:latest" . 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host " FAILED" -ForegroundColor Red
        continue
    }
    Write-Host " OK" -ForegroundColor Green
    
    # Tag
    docker tag "$RepoName`:latest" "$ImageUri`:latest" 2>&1 | Out-Null
    
    # Push
    Write-Host "    Pushing..." -NoNewline
    docker push "$ImageUri`:latest" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host " FAILED" -ForegroundColor Red
        continue
    }
    Write-Host " OK" -ForegroundColor Green
}
Write-Host ""

# Paso 3: Verificar imágenes en ECR
Write-Host "[3/4] Verificando imágenes en ECR..." -ForegroundColor Yellow
foreach ($Service in $Services) {
    $RepoName = "soccer/$Service"
    Write-Host "  → $RepoName" -NoNewline
    $Images = aws ecr describe-images --repository-name $RepoName --region $Region 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓" -ForegroundColor Green
    } else {
        Write-Host " ✗ (No encontrado)" -ForegroundColor Red
    }
}
Write-Host ""

# Paso 4: Información de siguiente paso
Write-Host "[4/4] Deployment completado" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SIGUIENTES PASOS:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. LAMBDA - Crear funciones Lambda:" -ForegroundColor White
Write-Host "   AWS Console → Lambda → Create function → Container image"
Write-Host "   Usar URIs:"
foreach ($Service in $Services) {
    Write-Host "   - $EcrRegistry/soccer/$Service`:latest" -ForegroundColor Gray
}
Write-Host ""
Write-Host "2. FARGATE - Crear Task Definitions:" -ForegroundColor White
Write-Host "   AWS Console → ECS → Task Definitions → Create new"
Write-Host "   Usar las mismas URIs de arriba"
Write-Host ""
Write-Host "3. Actualizar AWS-ENDPOINTS.md con las URLs generadas" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
