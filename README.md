# Task Management API - Crehana FastAPI

Una API robusta de gestión de tareas construida con FastAPI, implementando Clean Architecture, autenticación JWT, y containerizada con Docker.

## 📋 Descripción del Proyecto

Este proyecto es un sistema completo de gestión de tareas que permite:

- ✅ **Gestión de Usuarios**: Registro, login y autenticación con JWT
- ✅ **Listas de Tareas**: Crear, leer, actualizar y eliminar listas de tareas
- ✅ **Tareas**: CRUD completo con asignación de usuarios, estados y prioridades
- ✅ **Filtrado y Búsqueda**: Búsqueda por título, filtrado por estado, prioridad, usuario
- ✅ **Notificaciones**: Sistema de notificaciones por email (mock)
- ✅ **Arquitectura Limpia**: Separación clara de responsabilidades
- ✅ **Base de Datos**: PostgreSQL con migraciones usando Alembic
- ✅ **Testing**: Cobertura >89% con tests unitarios e integración
- ✅ **Calidad de Código**: Linting con flake8, formateo con black, type hints

### 🏗️ Arquitectura

```
app/
├── api/              # Capa de presentación (endpoints, dependencias)
├── domain/           # Modelos de dominio y value objects
├── use_cases/        # Casos de uso (lógica de negocio)
├── services/         # Servicios de aplicación
├── infrastructure/   # Base de datos, repositories, externos
└── schemas/          # Schemas de Pydantic para validación
```

### 🛠️ Stack Tecnológico

- **Framework**: FastAPI 0.115
- **Base de Datos**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migraciones**: Alembic
- **Autenticación**: JWT con bcrypt
- **Testing**: pytest, coverage
- **Linting**: flake8, black, isort, ruff
- **Containerización**: Docker & Docker Compose
- **Python**: 3.9+

## 🚀 Configuración del Entorno Local

### Prerrequisitos

Asegúrate de tener instalados los siguientes componentes según tu sistema operativo:

#### 🐧 Linux (Ubuntu/Debian)
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Python 3.9+ (si no está instalado)
sudo apt install python3.9 python3.9-venv python3.9-dev python3-pip

# PostgreSQL (opcional para desarrollo local)
sudo apt install postgresql postgresql-contrib

# Git
sudo apt install git

# Docker (opcional)
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER  # Reiniciar sesión después
```

#### 🍎 macOS
```bash
# Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.9+
brew install python@3.9

# PostgreSQL (opcional)
brew install postgresql@15
brew services start postgresql@15

# Git (usualmente ya está instalado)
brew install git

# Docker (opcional)
brew install --cask docker
```

#### 🪟 Windows
```powershell
# Opción 1: Usando Chocolatey (recomendado)
# Instalar Chocolatey primero: https://chocolatey.org/install

choco install python --version=3.9.0
choco install postgresql --version=15.0
choco install git
choco install docker-desktop

# Opción 2: Descarga manual
# Python: https://www.python.org/downloads/
# PostgreSQL: https://www.postgresql.org/download/windows/
# Git: https://git-scm.com/download/win
# Docker Desktop: https://www.docker.com/products/docker-desktop
```

### 📦 Instalación del Proyecto

#### 1. Clonar el repositorio
```bash
git clone git@github.com:allanos94/crehana_fastapi.git
cd crehana_fastapi
```

#### 2. Crear entorno virtual

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### 3. Instalar dependencias

```bash
# Dependencias de desarrollo (incluye testing y linting)
pip install -r requirements/dev.txt

# O solo dependencias de producción
pip install -r requirements/prod.txt
```

#### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env-example .env

# Editar .env con tu configuración
# DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db
# SECRET_KEY=tu_secret_key_super_seguro_aqui
# ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 5. Configurar base de datos

**Opción A: PostgreSQL local**
```bash
# Linux/macOS
sudo -u postgres createdb tareas_db

# Windows (desde psql)
psql -U postgres
CREATE DATABASE tareas_db;
\q
```

**Opción B: Docker (recomendado)**
```bash
# Solo la base de datos
docker run --name postgres-tareas \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=tareas_db \
  -p 5433:5432 -d postgres:15
```

#### 6. Ejecutar migraciones

```bash
# Aplicar migraciones
make migrate

# O manualmente según tu SO:
# Linux/macOS:
DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db' alembic upgrade head

# Windows (PowerShell):
$env:DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db'; alembic upgrade head

# Windows (CMD):
set DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db && alembic upgrade head
```

#### 7. Ejecutar la aplicación

```bash
# Con Make (recomendado)
make run-local

# O manualmente
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en: http://localhost:8000

- 📖 **Documentación**: http://localhost:8000/docs
- 🔍 **ReDoc**: http://localhost:8000/redoc

## 🐳 Ejecutar con Docker

Docker simplifica el despliegue y garantiza consistencia entre entornos.

### Prerrequisitos Docker

#### 🐧 Linux
```bash
# Ubuntu/Debian
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
# Reiniciar sesión o ejecutar: newgrp docker
```

#### 🍎 macOS
```bash
brew install --cask docker
# O descargar Docker Desktop desde: https://www.docker.com/products/docker-desktop
```

#### 🪟 Windows
```powershell
# Con Chocolatey
choco install docker-desktop

# O descargar Docker Desktop desde: https://www.docker.com/products/docker-desktop
# Asegúrate de habilitar WSL 2 backend
```

### 🔧 Entorno de Desarrollo

```bash
# Construir y ejecutar contenedores de desarrollo
make dev

# O manualmente
docker-compose -f docker-compose.dev.yml up --build -d
```

**Servicios incluidos:**
- 🚀 **Backend FastAPI**: http://localhost:8000 (hot reload activado)
- 🗄️ **PostgreSQL**: localhost:5433
- 📁 **Volúmenes**: Código sincronizado para desarrollo

### 🏭 Entorno de Producción

```bash
# Construir y ejecutar contenedores de producción
make prod

# O manualmente
docker-compose -f docker-compose.prod.yml up --build -d
```

### 📋 Comandos Docker Útiles

```bash
# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Acceder al contenedor backend
docker-compose -f docker-compose.dev.yml exec backend bash

# Ejecutar migraciones en Docker
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head

# Parar servicios
docker-compose -f docker-compose.dev.yml down

# Limpiar (eliminar volúmenes)
make clean
```

## 🧪 Ejecutar Pruebas

El proyecto incluye una suite completa de tests con >89% de cobertura.

### 🚀 Comandos Make (Recomendado)

```bash
# Ejecutar todos los tests con cobertura
make test

# Solo tests unitarios
make test-unit

# Solo tests de integración
make test-integration

# Generar reporte HTML de cobertura
make test-coverage
```

### 🔧 Comandos Manuales

#### Todos los Tests
```bash
# Linux/macOS
python -m pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=75

# Windows (PowerShell)
python -m pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=75

# Windows (CMD)
python -m pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=75
```

#### Tests Específicos
```bash
# Tests unitarios
python -m pytest tests/unit/ -v

# Tests de integración
python -m pytest tests/integration/ -v

# Test específico
python -m pytest tests/unit/test_auth_service.py::TestAuthService::test_password_hashing -v

# Con marcadores
python -m pytest -m "not slow" -v
python -m pytest -m "auth" -v
```

#### Opciones Avanzadas
```bash
# Ejecutar en paralelo (si tienes pytest-xdist)
python -m pytest tests/ -n auto

# Con output detallado
python -m pytest tests/ -v -s

# Solo tests que fallaron la última vez
python -m pytest tests/ --lf

# Detener en el primer fallo
python -m pytest tests/ -x

# Generar reporte de cobertura HTML
python -m pytest tests/ --cov=app --cov-report=html
```

### 📊 Interpretación de Cobertura

```bash
# El reporte mostrará algo como:
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
app/api/v1/endpoints/auth.py         31      0   100%
app/services/auth.py                 38      0   100%
app/infrastructure/db/models.py      50      5    90%   23-27
----------------------------------------------------------------
TOTAL                               997    109    89%
```

- **Stmts**: Líneas de código
- **Miss**: Líneas no cubiertas por tests
- **Cover**: Porcentaje de cobertura
- **Missing**: Números de línea específicos sin cobertura

## 🛠️ Herramientas de Desarrollo

### 🎨 Formateo y Linting

```bash
# Verificar estilo de código
make check-style

# Formatear código automáticamente
make format

# Linting completo
make lint

# Arreglar problemas automáticamente
make lint-fix
```

### 🔧 Pre-commit (Recomendado)

Pre-commit ejecuta automáticamente verificaciones antes de cada commit:

```bash
# Instalar hooks (solo primera vez)
make install-hooks

# Ejecutar en todos los archivos
make pre-commit-all

# Actualizar hooks
make pre-commit-update
```

**Uso automático**: Una vez instalado, pre-commit se ejecuta automáticamente en cada `git commit`.

### 🗄️ Gestión de Base de Datos

```bash
# Crear migración automática
make migrations

# Aplicar migraciones
make migrate

# Ver historial de migraciones
make migrate-history

# Rollback de migración
make migrate-down

# Crear migración manual
make migrate-create MESSAGE="add_user_avatar"
```

### 📦 Gestión de Dependencias

```bash
# Actualizar archivos de dependencias
make update-deps

# Instalar dependencias de desarrollo
make install-dev

# Instalar dependencias de producción
make install-prod
```

## 🌐 API Endpoints

### 🔐 Autenticación
- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Login (obtener token JWT)
- `GET /auth/me` - Información del usuario actual

### 📝 Listas de Tareas
- `GET /task-lists/` - Listar listas de tareas
- `POST /task-lists/` - Crear lista de tareas
- `GET /task-lists/{id}` - Obtener lista específica
- `PUT /task-lists/{id}` - Actualizar lista
- `DELETE /task-lists/{id}` - Eliminar lista

### ✅ Tareas
- `GET /tasks/` - Listar tareas (con filtros)
- `POST /tasks/` - Crear tarea
- `GET /tasks/{id}` - Obtener tarea específica
- `PUT /tasks/{id}` - Actualizar tarea
- `DELETE /tasks/{id}` - Eliminar tarea
- `POST /tasks/{id}/assign` - Asignar tarea a usuario
- `POST /tasks/{id}/unassign` - Desasignar tarea

### 📱 Ejemplos de Uso

```bash
# Registrar usuario
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "mi_password"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@ejemplo.com&password=mi_password"

# Crear lista de tareas (con token)
curl -X POST "http://localhost:8000/task-lists/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mi Lista de Tareas"}'
```

## ⚠️ Consideraciones Importantes

### 🔒 Seguridad
- **SECRET_KEY**: Usa una clave secreta fuerte en producción
- **DATABASE_URL**: No incluyas credenciales en el código
- **CORS**: Configura dominios permitidos en producción
- **HTTPS**: Usa siempre HTTPS en producción

### 🏗️ Producción
- **Variables de Entorno**: Usa un gestor de secretos
- **Base de Datos**: Configura backup automático
- **Logs**: Implementa logging centralizado
- **Monitoreo**: Agrega métricas y health checks
- **Reverse Proxy**: Usa Nginx o similar

### 🖥️ Diferencias por SO

#### Linux
- Usa `sudo` para comandos de sistema
- PostgreSQL por defecto en puerto 5432
- Paths con `/` (slash)

#### macOS
- Homebrew como gestor de paquetes
- Mismo comportamiento que Linux
- Puede requerir permisos adicionales para Docker

#### Windows
- PowerShell recomendado sobre CMD
- Paths con `\` (backslash)
- Variables de entorno diferentes (`$env:` vs `export`)
- WSL2 recomendado para mejor compatibilidad Docker

### 🐛 Solución de Problemas Comunes

#### Puerto en uso
```bash
# Linux/macOS
sudo lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### Problemas de permisos Docker
```bash
# Linux
sudo usermod -aG docker $USER
newgrp docker

# Windows: Ejecutar PowerShell como administrador
```

#### Base de datos no responde
```bash
# Verificar que PostgreSQL esté corriendo
# Linux
sudo systemctl status postgresql

# macOS
brew services list | grep postgresql

# Windows
services.msc  # Buscar PostgreSQL
```

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.
