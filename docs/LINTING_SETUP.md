# Configuración de Linting y Formateo de Código

Este proyecto utiliza múltiples herramientas para mantener la calidad y consistencia del código Python.

## Herramientas Configuradas

### 1. **flake8** - Linter Principal
- **Archivo de configuración**: `.flake8`
- **Propósito**: Verificar estilo de código, complejidad y errores de sintaxis
- **Configuración actual**:
  - Longitud máxima de línea: 90 caracteres
  - Complejidad máxima: 10
  - Ignora errores específicos como E203, E501 (manejados por black)
  - Excluye directorios como migrations, __pycache__, venv

### 2. **black** - Formateador de Código
- **Archivo de configuración**: `pyproject.toml` (sección `[tool.black]`)
- **Propósito**: Formateo automático y consistente del código
- **Configuración actual**:
  - Longitud de línea: 90 caracteres
  - Compatible con Python 3.9-3.12
  - Excluye archivos de migración y entornos virtuales

### 3. **isort** - Organizador de Imports
- **Archivo de configuración**: `pyproject.toml` (sección `[tool.isort]`)
- **Propósito**: Organizar y ordenar las importaciones
- **Configuración actual**:
  - Profile compatible con black
  - Longitud de línea: 90 caracteres
  - Agrega comas finales e incluye comentarios

### 4. **ruff** - Linter Moderno y Rápido
- **Archivo de configuración**: `pyproject.toml` (sección `[tool.ruff]`)
- **Propósito**: Linting rápido con reglas modernas de Python
- **Configuración actual**:
  - Incluye reglas de pycodestyle, pyflakes, isort, mccabe, pyupgrade
  - Moderniza anotaciones de tipos (List → list, Dict → dict, etc.)
  - Compatible con Python 3.9+

### 5. **mypy** - Verificador de Tipos
- **Archivo de configuración**: `pyproject.toml` (sección `[tool.mypy]`)
- **Propósito**: Verificación estática de tipos
- **Configuración actual**:
  - Python 3.9+
  - Configuración balanceada entre strictness y usabilidad

## Comandos del Makefile

### Verificación de Estilo
```bash
make check-style  # Verifica el estilo sin hacer cambios
```

### Formateo Automático
```bash
make format       # Aplica formateo automático con black, isort y ruff
```

### Linting Completo
```bash
make lint         # Ejecuta todas las herramientas de linting
```

### Arreglo Automático
```bash
make lint-fix     # Intenta arreglar automáticamente los problemas
```

## Uso Individual de Herramientas

### flake8
```bash
flake8 app tests                    # Verificar estilo completo
flake8 app/api/                     # Verificar directorio específico
flake8 --statistics app tests       # Con estadísticas
```

### black
```bash
black app tests                     # Formatear código
black --check app tests             # Solo verificar sin cambios
black --diff app tests              # Mostrar diferencias
```

### isort
```bash
isort app tests                     # Organizar imports
isort --check-only app tests        # Solo verificar
isort --diff app tests              # Mostrar diferencias
```

### ruff
```bash
ruff check app tests                # Verificar con ruff
ruff check --fix app tests          # Arreglar automáticamente
ruff check --unsafe-fixes app tests # Incluir arreglos no seguros
```

## Integración con IDE

### VS Code
1. Instalar extensiones:
   - Python
   - Black Formatter
   - isort
   - Flake8
   - Ruff

2. Configuración recomendada en `.vscode/settings.json`:
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": false,
    "editor.formatOnSave": true,
    "python.sortImports.provider": "isort"
}
```

## Archivos de Configuración

### `.flake8`
```ini
[flake8]
max-line-length = 90
max-complexity = 10
ignore = E203, E501, W503, W504, F401, E402
exclude = .git, __pycache__, venv, migrations, alembic/versions
```

### `pyproject.toml` (secciones relevantes)
```toml
[tool.black]
line-length = 90
target-version = ['py39', 'py310', 'py311', 'py312']

[tool.isort]
profile = "black"
line_length = 90

[tool.ruff]
line-length = 90
target-version = "py39"
```

## Flujo de Trabajo Recomendado

1. **Antes de hacer commit**:
   ```bash
   make format      # Formatear código
   make check-style # Verificar que todo esté bien
   ```

2. **En CI/CD**:
   ```bash
   make check-style # Verificar estilo
   make test        # Ejecutar tests
   ```

3. **Para arreglar problemas automáticamente**:
   ```bash
   make lint-fix    # Intenta arreglar todos los problemas
   ```

## Reglas Ignoradas y Por Qué

- **E203**: Whitespace before ':' - Conflicto con black
- **E501**: Line too long - Manejado por black
- **W503/W504**: Line break before/after binary operator - Estilo personal
- **F401**: Imported but unused - Manejado por autoflake/ruff
- **E402**: Module level import not at top - Para casos específicos como imports condicionales

## Modernizaciones Aplicadas

- `typing.List` → `list`
- `typing.Dict` → `dict`
- `typing.Type` → `type`
- `Optional[X]` → `X | None` (donde es apropiado)
- `typing.Generator` → `collections.abc.Generator`

Estas modernizaciones hacen el código compatible con las mejores prácticas de Python 3.9+.
