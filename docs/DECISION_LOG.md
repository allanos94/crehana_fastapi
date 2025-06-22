# Decision Log - Task Management API

Este documento registra las decisiones técnicas importantes tomadas durante el desarrollo del proyecto, explicando el contexto, las alternativas consideradas y las razones detrás de cada elección.

## Tabla de Contenidos

1. [Arquitectura y Patrones](#1-arquitectura-y-patrones)
2. [Framework y Tecnologías Core](#2-framework-y-tecnologías-core)
3. [Base de Datos](#3-base-de-datos)
4. [Autenticación y Seguridad](#4-autenticación-y-seguridad)
5. [Testing](#5-testing)
6. [Calidad de Código](#6-calidad-de-código)
7. [Containerización](#7-containerización)
8. [Gestión de Dependencias](#8-gestión-de-dependencias)
9. [Configuración y Variables de Entorno](#9-configuración-y-variables-de-entorno)
10. [Notificaciones](#10-notificaciones)

---

## 1. Arquitectura y Patrones

### Decision: Clean Architecture (Hexagonal Architecture)

**Fecha**: Inicio del proyecto
**Estado**: ✅ Implementado
**Stakeholders**: Equipo de desarrollo

#### Contexto

Necesitábamos una arquitectura que permita:

- Separación clara de responsabilidades
- Testabilidad alta
- Independencia de frameworks externos
- Facilidad de mantenimiento a largo plazo

#### Alternativas Consideradas

1. **MVC Simple**: Modelo-Vista-Controlador básico
2. **Clean Architecture**: Arquitectura por capas con inversión de dependencias
3. **Domain-Driven Design (DDD)**: Enfoque completo en el dominio
4. **Arquitectura de Microservicios**: Separación por servicios

#### Decisión

**Clean Architecture** con las siguientes capas:

```
app/
├── api/              # Capa de presentación (controllers, routes)
├── domain/           # Entidades y reglas de negocio
├── use_cases/        # Casos de uso (application layer)
├── services/         # Servicios de aplicación
├── infrastructure/   # Adaptadores externos (DB, APIs)
└── schemas/          # Contratos de entrada/salida
```

#### Razones

- ✅ **Testabilidad**: Fácil mockear dependencias externas
- ✅ **Mantenibilidad**: Cada capa tiene responsabilidades claras
- ✅ **Flexibilidad**: Fácil cambiar implementaciones sin afectar lógica de negocio
- ✅ **SOLID Principles**: Cumple principios de diseño sólido
- ✅ **Escalabilidad**: Estructura preparada para crecimiento

#### Consecuencias

- ➕ Código más organizado y mantenible
- ➕ Tests más focalizados y rápidos
- ➕ Menor acoplamiento entre componentes
- ➖ Más archivos y estructura inicial compleja
- ➖ Curva de aprendizaje para desarrolladores nuevos

---

## 2. Framework y Tecnologías Core

### Decision: FastAPI como Framework Principal

**Fecha**: Inicio del proyecto
**Estado**: ✅ Implementado
**Stakeholders**: Equipo técnico

#### Contexto

Necesitábamos un framework web moderno para Python con:

- Alto rendimiento
- Documentación automática de API
- Validación de tipos nativa
- Soporte async/await

#### Alternativas Consideradas

1. **Django REST Framework**: Framework maduro y completo
2. **FastAPI**: Framework moderno con type hints
3. **Flask**: Framework minimalista y flexible
4. **Starlette**: Framework ASGI puro

#### Decisión

**FastAPI 0.115**

#### Razones

- ✅ **Performance**: Uno de los frameworks más rápidos disponibles
- ✅ **Type Safety**: Validación automática con Pydantic
- ✅ **Documentación**: OpenAPI/Swagger automático
- ✅ **Modern Python**: Soporte nativo para async/await y type hints
- ✅ **Ecosystem**: Gran ecosistema y comunidad activa
- ✅ **Standards**: Basado en estándares (OpenAPI, JSON Schema)

#### Consecuencias

- ➕ Desarrollo más rápido con validación automática
- ➕ Documentación siempre actualizada
- ➕ Excelente DX (Developer Experience)
- ➕ Compatible con herramientas modernas de Python
- ➖ Framework relativamente nuevo (menos maduro que Django)

---

## 3. Base de Datos

### Decision: PostgreSQL + SQLAlchemy 2.0

**Fecha**: Inicio del proyecto
**Estado**: ✅ Implementado
**Stakeholders**: Equipo técnico, Arquitecto de datos

#### Contexto

Necesitábamos:

- Base de datos relacional robusta
- ORM con soporte para async
- Migrations automáticas
- Soporte para tipos JSON

#### Alternativas Consideradas

1. **PostgreSQL + SQLAlchemy**: Combinación robusta y madura
2. **MongoDB + Motor**: Base de datos NoSQL
3. **SQLite**: Base de datos embebida para desarrollo
4. **MySQL + SQLAlchemy**: Alternativa relacional popular

#### Decisión

**PostgreSQL 15 + SQLAlchemy 2.0 + Alembic**

#### Razones

- ✅ **Robustez**: PostgreSQL es extremadamente confiable
- ✅ **Features**: Soporte JSON, arrays, tipos personalizados
- ✅ **Performance**: Excelente rendimiento y optimización
- ✅ **SQLAlchemy 2.0**: Nueva API más moderna y type-safe
- ✅ **Migrations**: Alembic para control de versiones de schema
- ✅ **Ecosystem**: Amplio soporte de herramientas

#### Configuración Implementada

```python
# Async engine para mejor performance
engine = create_async_engine(DATABASE_URL)

# Repository pattern para abstracción
class BaseRepository[T]:
    def __init__(self, db: Session, model_class: type[T]):
        self.db = db
        self.model_class = model_class
```

#### Consecuencias

- ➕ Base de datos empresarial robusta
- ➕ Excelente soporte para transacciones complejas
- ➕ Migrations automáticas y versionadas
- ➕ Type safety mejorado con SQLAlchemy 2.0
- ➖ Configuración inicial más compleja que SQLite
- ➖ Requiere servidor de base de datos separado

---

## 4. Autenticación y Seguridad

### Decision: JWT + bcrypt + OAuth2

**Fecha**: Semana 2
**Estado**: ✅ Implementado
**Stakeholders**: Equipo de desarrollo, Security team

#### Contexto

Necesitábamos un sistema de autenticación que sea:

- Stateless (sin sesiones)
- Seguro para APIs
- Compatible con estándares web
- Escalable

#### Alternativas Consideradas

1. **Session-based**: Autenticación tradicional con cookies
2. **JWT**: Tokens autocontenidos
3. **OAuth2 + External Provider**: Delegación a terceros (Google, GitHub)
4. **API Keys**: Autenticación por clave fija

#### Decisión

**JWT (JSON Web Tokens) + bcrypt + OAuth2 Password Flow**

#### Implementación

```python
# Hashing seguro de passwords
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# JWT con expiración
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

#### Razones

- ✅ **Stateless**: No requiere almacenamiento de sesiones
- ✅ **Scalable**: Fácil distribución entre servicios
- ✅ **Standard**: OAuth2 es estándar de la industria
- ✅ **Security**: bcrypt es resistente a rainbow tables
- ✅ **Flexibility**: Fácil integración con frontend SPA

#### Configuración de Seguridad

- **Hash Algorithm**: bcrypt con salt automático
- **JWT Algorithm**: HS256
- **Token Expiration**: 30 minutos por defecto
- **Password Policy**: Mínimo 8 caracteres (configurable)

#### Consecuencias

- ➕ Sistema de autenticación moderno y escalable
- ➕ Compatible con aplicaciones SPA y móviles
- ➕ No requiere almacenamiento de estado en servidor
- ➖ Tokens no se pueden revocar hasta que expiren
- ➖ Requiere gestión cuidadosa de claves secretas

---

## 5. Testing

### Decision: pytest + Coverage + Fixtures

**Fecha**: Semana 1
**Estado**: ✅ Implementado
**Stakeholders**: Equipo de desarrollo, QA

#### Contexto

Necesitábamos estrategia de testing que incluya:

- Tests unitarios rápidos
- Tests de integración completos
- Cobertura de código medible
- Fixtures reutilizables

#### Alternativas Consideradas

1. **unittest**: Framework estándar de Python
2. **pytest**: Framework moderno con fixtures
3. **nose2**: Sucesor de nose
4. **Robot Framework**: Testing de aceptación

#### Decisión

**pytest + pytest-cov + pytest-asyncio**

#### Estructura Implementada

```
tests/
├── conftest.py           # Fixtures globales
├── unit/                 # Tests unitarios
│   ├── test_auth_service.py
│   ├── test_repositories.py
│   └── test_domain_models.py
├── integration/          # Tests de integración
│   ├── test_auth_endpoints.py
│   ├── test_task_endpoints.py
│   └── test_task_list_endpoints.py
└── test_database.py     # Tests de DB
```

#### Configuración de Coverage

- **Threshold**: Mínimo 75% de cobertura
- **Target**: Mantener >89% de cobertura
- **Exclusions**: Migrations, configuración, **init**.py

#### Fixtures Clave

```python
@pytest.fixture
async def test_db():
    """Database fixture for testing"""

@pytest.fixture
def test_user():
    """Create test user"""

@pytest.fixture
def auth_headers():
    """JWT headers for authenticated requests"""
```

#### Razones

- ✅ **Sintaxis Clara**: Tests más legibles con assert simple
- ✅ **Fixtures Potentes**: Reutilización y composición fácil
- ✅ **Plugins**: Gran ecosistema de plugins
- ✅ **Async Support**: Excelente soporte para código async
- ✅ **Reporting**: Reportes detallados de cobertura

#### Consecuencias

- ➕ Tests más expresivos y mantenibles
- ➕ Cobertura alta y medible (>89%)
- ➕ CI/CD integrado con reportes automáticos
- ➕ Separación clara entre unit e integration tests
- ➖ Curva de aprendizaje para fixtures avanzadas

---

## 6. Calidad de Código

### Decision: Multi-tool Linting Strategy

**Fecha**: Semana 3
**Estado**: ✅ Implementado
**Stakeholders**: Equipo de desarrollo

#### Contexto

Necesitábamos mantener código consistente y de alta calidad con:

- Formateo automático
- Detección de errores
- Estándares de código
- Type checking

#### Alternativas Consideradas

1. **Solo flake8**: Linting básico
2. **Solo black**: Solo formateo
3. **Pylint**: Linting completo pero lento
4. **Multi-tool approach**: Combinación de herramientas especializadas

#### Decisión

**flake8 + black + isort + ruff + mypy**

#### Configuración por Herramienta

**flake8** (`.flake8`):

```ini
[flake8]
max-line-length = 90
max-complexity = 10
ignore = E203, E501, W503, W504, F401, E402
```

**black** (`pyproject.toml`):

```toml
[tool.black]
line-length = 90
target-version = ['py39', 'py310', 'py311', 'py312']
```

**ruff** (`pyproject.toml`):

```toml
[tool.ruff]
line-length = 90
select = ["E", "W", "F", "I", "C90", "UP"]
```

#### Comandos Make

```bash
make check-style  # Verificar sin cambios
make format      # Formatear automáticamente
make lint-fix    # Arreglar automáticamente
```

#### Razones

- ✅ **Especialización**: Cada herramienta hace una cosa muy bien
- ✅ **Speed**: ruff es extremadamente rápido
- ✅ **Automation**: Formateo automático sin discusiones
- ✅ **Modern**: Tipos modernos (list vs List, dict vs Dict)
- ✅ **CI Integration**: Fácil integración en pipelines

#### Estándares Adoptados

- **Line Length**: 90 caracteres (balance legibilidad/pantalla)
- **Import Organization**: isort con perfil black
- **Type Hints**: Obligatorios en funciones públicas
- **Docstrings**: Google style para funciones complejas

#### Consecuencias

- ➕ Código consistente en todo el equipo
- ➕ Menos tiempo en code reviews discutiendo estilo
- ➕ Detección temprana de errores potenciales
- ➕ Modernización automática de código Python
- ➖ Setup inicial complejo
- ➖ Múltiples herramientas que mantener

---

## 7. Containerización

### Decision: Docker Multi-Stage + Docker Compose

**Fecha**: Semana 2
**Estado**: ✅ Implementado
**Stakeholders**: DevOps, Equipo de desarrollo

#### Contexto

Necesitábamos:

- Entorno consistente entre desarrollo y producción
- Despliegue fácil y reproducible
- Separación entre entorno dev y prod
- Gestión de dependencias del sistema

#### Alternativas Consideradas

1. **Docker simple**: Un solo Dockerfile
2. **Docker multi-stage**: Optimización de imágenes
3. **Kubernetes**: Orquestación completa
4. **Virtual Machines**: VMs tradicionales

#### Decisión

**Docker Multi-Stage + Docker Compose**

#### Implementación

**Dockerfile.dev** (Desarrollo):

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements/ requirements/
RUN pip install -r requirements/dev.txt
COPY . .
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Dockerfile** (Producción - Multi-stage):

```dockerfile
# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt

# Production stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY app/ app/
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose Services

- **Backend**: FastAPI application
- **Database**: PostgreSQL 15
- **Volumes**: Persistent data + code sync (dev)

#### Razones

- ✅ **Consistency**: Mismo entorno en todos lados
- ✅ **Isolation**: Dependencias aisladas del host
- ✅ **Optimization**: Multi-stage reduce tamaño de imagen final
- ✅ **Development**: Hot reload en desarrollo
- ✅ **Portability**: Funciona igual en cualquier SO

#### Configuración de Entornos

- **Development**: Volume mounts para hot reload
- **Production**: Imagen optimizada sin herramientas dev
- **Testing**: Base de datos en memoria para tests

#### Consecuencias

- ➕ Despliegue consistente y reproducible
- ➕ Onboarding más fácil para nuevos desarrolladores
- ➕ Aislamiento completo de dependencias
- ➕ Fácil escalabilidad horizontal
- ➖ Overhead de recursos comparado con instalación nativa
- ➖ Curva de aprendizaje para desarrolladores sin experiencia Docker

---

## 8. Gestión de Dependencias

### Decision: pip-tools para Dependency Management

**Fecha**: Semana 1
**Estado**: ✅ Implementado
**Stakeholders**: Equipo de desarrollo

#### Contexto

Necesitábamos gestión determinística de dependencias con:

- Versiones exactas para reproducibilidad
- Separación entre dependencias de desarrollo y producción
- Resolución automática de conflictos
- Seguridad y actualizaciones controladas

#### Alternativas Consideradas

1. **requirements.txt simple**: Gestión manual
2. **Pipenv**: Pipfile + Pipfile.lock
3. **Poetry**: pyproject.toml moderno
4. **pip-tools**: Compilación de requirements

#### Decisión

**pip-tools con estructura jerárquica**

#### Estructura Implementada

```
requirements/
├── base.in          # Dependencias core
├── base.txt         # Compilado de base.in
├── dev.in           # Dependencias desarrollo
├── dev.txt          # Compilado de dev.in
├── prod.in          # Dependencias producción
└── prod.txt         # Compilado de prod.in
```

#### Flujo de Trabajo

```bash
# Editar base.in, dev.in, prod.in manualmente
# Compilar dependencias
pip-compile requirements/base.in
pip-compile requirements/dev.in
pip-compile requirements/prod.in

# Makefile automation
make update-deps
```

#### Ejemplo base.in

```
fastapi>=0.115.0,<0.116.0
sqlalchemy>=2.0.0,<3.0.0
alembic>=1.16.0,<2.0.0
pydantic>=2.0.0,<3.0.0
uvicorn[standard]>=0.30.0
```

#### Razones

- ✅ **Deterministic**: Versiones exactas en .txt
- ✅ **Separation**: Clara separación dev/prod
- ✅ **Compatibility**: Compatible con pip estándar
- ✅ **Security**: Hash checking automático
- ✅ **Simplicity**: Más simple que Poetry/Pipenv

#### Políticas de Versionado

- **Major versions**: Pinned (evitar breaking changes)
- **Minor versions**: Allowed (features nuevos)
- **Patch versions**: Automático (security fixes)

#### Consecuencias

- ➕ Builds reproducibles entre entornos
- ➕ Separación clara de dependencias
- ➕ Fácil debugging de conflictos
- ➕ Compatible con cualquier deployment
- ➖ Proceso manual para actualizar dependencias
- ➖ Archivos .txt pueden volverse grandes

---

## 9. Configuración y Variables de Entorno

### Decision: Pydantic Settings + .env Files

**Fecha**: Inicio del proyecto
**Estado**: ✅ Implementado
**Stakeholders**: DevOps, Desarrollo

#### Contexto

Necesitábamos gestión de configuración que sea:

- Type-safe y validada
- Fácil de cambiar entre entornos
- Segura (no secrets en código)
- Compatible con 12-factor app

#### Alternativas Consideradas

1. **os.environ direct**: Acceso directo a variables
2. **python-decouple**: Librería simple para configs
3. **Pydantic Settings**: Validación con types
4. **Config files**: YAML/JSON para configuración

#### Decisión

**Pydantic Settings + .env files + .env-example**

#### Implementación

```python
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Database
    database_url: str = Field(..., env="DATABASE_URL")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # App
    app_name: str = Field("Task Management API", env="APP_NAME")
    debug: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

#### Estructura de Archivos

- **`.env`**: Variables locales (ignorado en git)
- **`.env-example`**: Template para nuevos desarrolladores
- **`settings.py`**: Configuración centralizada con validación

#### Variables por Entorno

**Development**:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=true
```

**Production**:

```env
DATABASE_URL=postgresql+psycopg2://user:pass@prod-db:5432/tareas_db
SECRET_KEY=super-secure-random-key-256-bits
DEBUG=false
```

#### Razones

- ✅ **Type Safety**: Validación automática de tipos
- ✅ **Documentation**: Self-documenting con Field descriptions
- ✅ **Validation**: Errores claros si falta configuración
- ✅ **12-Factor**: Siguiendo mejores prácticas
- ✅ **Security**: Secrets fuera del código

#### Gestión de Secrets

- **Development**: .env local
- **Production**: Variables de entorno del sistema
- **CI/CD**: Secrets del proveedor (GitHub Actions, etc.)

#### Consecuencias

- ➕ Configuración type-safe y validada
- ➕ Fácil onboarding con .env-example
- ➕ Errores claros de configuración
- ➕ Compatible con containers y cloud
- ➖ Dependencia adicional (Pydantic)
- ➖ Requiere disciplina en gestión de secrets

---

## 10. Notificaciones

### Decision: Mock Email Service con Interface

**Fecha**: Semana 2
**Estado**: ✅ Implementado
**Stakeholders**: Producto, Desarrollo

#### Contexto

Necesitábamos sistema de notificaciones que:

- Notifique cambios importantes
- Sea fácil de testear
- Permita evolución futura
- No requiera setup complejo inicial

#### Alternativas Consideradas

1. **Email real**: SMTP desde el inicio
2. **Mock service**: Simulación para desarrollo
3. **Queue system**: Redis/Celery para async
4. **Third-party**: SendGrid, Mailgun, etc.

#### Decisión

**Mock Email Service con Interface para evolución futura**

#### Implementación

```python
class NotificationService:
    @staticmethod
    def send_task_assignment_notification(task: Task, assigned_user: User) -> bool:
        """Send notification when a task is assigned to a user."""
        try:
            # Mock email content
            subject = f"New Task Assigned: {task.title}"
            body = f"Hello {assigned_user.name}, you have been assigned a new task..."

            # Log instead of sending real email
            logger.info(f"MOCK EMAIL SENT - To: {assigned_user.email}, Subject: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False
```

#### Eventos que Disparan Notificaciones

- ✅ **Task Assignment**: Usuario asignado a tarea
- ✅ **Task Unassignment**: Usuario removido de tarea
- ✅ **Status Change**: Cambio de estado de tarea

#### Interface para Futuro

```python
# Future implementation would replace mock with:
# - SMTP email service
# - Push notifications
# - Slack/Teams integration
# - SMS notifications
```

#### Razones

- ✅ **Simplicity**: No requiere infraestructura adicional
- ✅ **Testability**: Fácil verificar en tests
- ✅ **Evolution**: Interface preparada para implementación real
- ✅ **Logging**: Visibilidad completa de notificaciones
- ✅ **MVP Ready**: Funcional para demostración

#### Testing Strategy

```python
def test_task_assignment_notification(test_task, test_user, caplog):
    result = NotificationService.send_task_assignment_notification(test_task, test_user)
    assert result is True
    assert "MOCK EMAIL SENT" in caplog.text
```

#### Evolución Planificada

1. **Phase 1**: Mock service (actual)
2. **Phase 2**: SMTP real con templates
3. **Phase 3**: Queue system para async processing
4. **Phase 4**: Multiple channels (email, push, slack)

#### Consecuencias

- ➕ Funcionalidad inmediata sin dependencies
- ➕ Fácil testing y debugging
- ➕ Foundation para implementación real
- ➕ No bloquea desarrollo de otras features
- ➖ No notificaciones reales en MVP
- ➖ Requiere implementación futura para producción

---

## Resumen de Decisiones

| Área                 | Decisión                       | Estado | Impacto                         |
| -------------------- | ------------------------------ | ------ | ------------------------------- |
| **Arquitectura**     | Clean Architecture             | ✅     | Alto - Base de todo el proyecto |
| **Framework**        | FastAPI                        | ✅     | Alto - Core de la aplicación    |
| **Base de Datos**    | PostgreSQL + SQLAlchemy        | ✅     | Alto - Persistencia             |
| **Autenticación**    | JWT + bcrypt                   | ✅     | Alto - Seguridad                |
| **Testing**          | pytest + Coverage              | ✅     | Alto - Calidad                  |
| **Code Quality**     | Multi-tool (flake8+black+ruff) | ✅     | Medio - Mantenibilidad          |
| **Containerización** | Docker + Compose               | ✅     | Alto - Deployment               |
| **Dependencies**     | pip-tools                      | ✅     | Medio - Gestión                 |
| **Configuration**    | Pydantic Settings              | ✅     | Medio - Ops                     |
| **Notifications**    | Mock Service                   | ✅     | Bajo - Feature                  |

## Próximas Decisiones

### En Consideración

1. **API Versioning**: Estrategia para versionar endpoints
2. **Caching**: Redis para cache de consultas frecuentes
3. **Rate Limiting**: Protección contra abuse
4. **Real Notifications**: Implementación de email real
5. **File Uploads**: Manejo de archivos adjuntos en tareas
6. **Audit Log**: Tracking de cambios para compliance

### Criterios para Futuras Decisiones

- **Performance**: Impacto en latencia y throughput
- **Security**: Consideraciones de seguridad
- **Maintainability**: Facilidad de mantenimiento
- **Team Velocity**: Impacto en velocidad de desarrollo
- **Cost**: Impacto en costos de infraestructura
- **User Experience**: Impacto en la experiencia del usuario

---

_Este documento debe actualizarse con cada decisión técnica importante. Incluir fecha, contexto, alternativas y razones para mantener la trazabilidad del proyecto._
