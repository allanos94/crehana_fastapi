# Pre-commit Setup Guide

Este proyecto utiliza **pre-commit** para ejecutar automáticamente verificaciones de calidad de código antes de cada commit, asegurando que todo el código cumple con los estándares establecidos.

## 🚀 Qué es Pre-commit

Pre-commit es una herramienta que ejecuta automáticamente una serie de hooks (verificaciones) antes de que se complete un commit. Si alguna verificación falla, el commit se cancela y se muestran los errores que deben corregirse.

## ✅ Verificaciones Configuradas

### 🎨 **Formateo de Código**
- **black**: Formateo automático de código Python
- **isort**: Organización automática de imports

### 🔍 **Linting y Calidad**
- **flake8**: Verificación de estilo PEP8 y errores comunes
- **ruff**: Linting moderno y rápido con reglas adicionales

### 🛠️ **Verificaciones Generales**
- **end-of-file-fixer**: Asegura que los archivos terminen con nueva línea
- **trailing-whitespace**: Elimina espacios en blanco al final de líneas
- **check-yaml**: Valida sintaxis de archivos YAML
- **check-toml**: Valida sintaxis de archivos TOML
- **check-json**: Valida sintaxis de archivos JSON
- **check-added-large-files**: Previene commits de archivos muy grandes
- **check-merge-conflict**: Detecta marcadores de conflicto de merge
- **debug-statements**: Detecta declaraciones de debug olvidadas
- **check-docstring-first**: Verifica que docstrings estén en la posición correcta

## 📦 Instalación y Configuración

### 1. Pre-commit ya está instalado
Pre-commit ya está incluido en `requirements/dev.txt`, así que si has instalado las dependencias de desarrollo, ya lo tienes.

### 2. Activar Pre-commit
```bash
# Instalar los hooks de git
pre-commit install

# Verificar que está instalado
pre-commit --version
```

### 3. Ejecutar en todos los archivos (primera vez)
```bash
# Ejecutar pre-commit en todos los archivos existentes
pre-commit run --all-files
```

## 🔧 Uso Diario

### Commits Normales
Una vez configurado, pre-commit se ejecuta automáticamente en cada commit:

```bash
git add .
git commit -m "feat: add new feature"
# Pre-commit se ejecuta automáticamente aquí
```

### Ejemplo de Salida
```bash
black....................................................................Passed
isort....................................................................Passed
flake8...................................................................Passed
ruff (legacy alias)......................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
check yaml...............................................................Passed
check toml...............................................................Passed
check json...........................................(no files to check)Skipped
check for added large files..............................................Passed
check for merge conflicts................................................Passed
debug statements (python)................................................Passed
check docstring is first.................................................Passed
```

### Si hay errores:
```bash
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted app/services/example.py
All done! ✨ 🍰 ✨
1 file reformatted.
```

En este caso:
1. Pre-commit ha corregido automáticamente el formato
2. Necesitas agregar los cambios y hacer commit de nuevo:
```bash
git add app/services/example.py
git commit -m "feat: add new feature"
```

## 🚀 Comandos Útiles

### Ejecutar hooks específicos
```bash
# Solo black
pre-commit run black

# Solo flake8
pre-commit run flake8

# Solo en archivos específicos
pre-commit run --files app/services/example.py
```

### Saltar pre-commit (NO recomendado)
```bash
# Solo usar en emergencias
git commit -m "emergency fix" --no-verify
```

### Actualizar hooks
```bash
# Actualizar a las últimas versiones
pre-commit autoupdate

# Ver qué se actualizó
git diff .pre-commit-config.yaml
```

### Limpiar caché
```bash
# Si hay problemas con los hooks
pre-commit clean
pre-commit install
```

## 📋 Configuración Actual

El archivo `.pre-commit-config.yaml` contiene nuestra configuración actual:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        language_version: python3
        args: [--line-length=90]

  - repo: https://github.com/pycqa/isort
    rev: 6.0.1
    hooks:
      - id: isort
        args: [--profile=black, --line-length=90]

  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings, flake8-bugbear]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  # + otros hooks generales...
```

## 🎯 Beneficios

### ✅ **Para el Desarrollador**
- **Formato automático**: No más discusiones sobre estilo
- **Detección temprana**: Errores encontrados antes del commit
- **Consistencia**: Todo el código sigue los mismos estándares
- **Productividad**: Menos tiempo en code reviews

### ✅ **Para el Equipo**
- **Calidad uniforme**: Todo el código tiene la misma calidad
- **Menos conflictos**: Formato consistente reduce merge conflicts
- **Code reviews más rápidos**: Se enfocan en lógica, no en estilo
- **Onboarding fácil**: Nuevos desarrolladores siguen estándares automáticamente

### ✅ **Para el Proyecto**
- **Mantenibilidad**: Código más fácil de leer y mantener
- **Estabilidad**: Menos bugs por errores de estilo
- **Profesionalismo**: Código que se ve profesional y bien cuidado

## ⚠️ Consideraciones Importantes

### Primera ejecución
La primera vez que ejecutes pre-commit puede tomar varios minutos porque necesita descargar e instalar las herramientas.

### Commits que modifican archivos
Si pre-commit modifica archivos (por ejemplo, formateando código), el commit se cancela para que puedas revisar los cambios. Solo necesitas agregar los archivos modificados y hacer commit de nuevo.

### Rendimiento
Pre-commit solo verifica archivos que han cambiado en el commit, por lo que es rápido en el uso diario.

### Hooks opcionales
Algunos hooks como `mypy` y `bandit` están comentados porque pueden ser lentos o generar falsos positivos. Puedes habilitarlos si los necesitas:

```yaml
# Descomentar para habilitar type checking
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.11.0
  hooks:
    - id: mypy
```

## 🔧 Solución de Problemas

### "pre-commit command not found"
```bash
# Instalar pre-commit
pip install pre-commit

# O si usas requirements/dev.txt
pip install -r requirements/dev.txt
```

### "Hook failed"
```bash
# Ver detalles del error
pre-commit run --all-files --verbose

# Limpiar y reinstalar
pre-commit uninstall
pre-commit clean
pre-commit install
```

### "Files were modified"
Esto es normal. Pre-commit corrigió automáticamente los archivos. Solo necesitas:
```bash
git add <archivos_modificados>
git commit -m "tu mensaje"
```

### Saltar temporalmente un hook
```bash
# Saltar un hook específico
SKIP=flake8 git commit -m "mensaje"

# Saltar todos los hooks (emergencia)
git commit -m "mensaje" --no-verify
```

## 📚 Recursos Adicionales

- [Pre-commit Documentation](https://pre-commit.com/)
- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

---

**¡Pre-commit está configurado y listo para usar! Cada commit ahora será automáticamente verificado y mejorado.** 🚀
