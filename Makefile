# Makefile para gestión de entornos
.PHONY: help install-dev install-prod dev prod test clean migrations migrate migrate-down migrate-history migrate-current migrate-create

help: ## Mostrar esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-dev: ## Instalar dependencias de desarrollo
	pip install -r requirements/dev.txt

install-prod: ## Instalar dependencias de producción
	pip install -r requirements/prod.txt

update-deps: ## Actualizar archivos de dependencias compilados
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/prod.in

dev: ## Ejecutar entorno de desarrollo con Docker
	docker-compose -f docker-compose.dev.yml up --build -d

prod: ## Ejecutar entorno de producción con Docker
	docker-compose -f docker-compose.prod.yml up --build -d

test: ## Ejecutar tests con cobertura
	python -m pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=75

test-unit: ## Ejecutar solo tests unitarios
	python -m pytest tests/unit/ -v

test-integration: ## Ejecutar solo tests de integración
	python -m pytest tests/integration/ -v

test-coverage: ## Ejecutar tests y generar reporte de cobertura
	python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

lint: ## Ejecutar linting completo
	@echo "Running flake8..."
	flake8 app tests
	@echo "Running ruff..."
	ruff check app tests
	@echo "Running black check..."
	black --check app tests
	@echo "Running isort check..."
	isort --check-only app tests

format: ## Formatear código automáticamente
	@echo "Running black..."
	black app tests
	@echo "Running isort..."
	isort app tests
	@echo "Running ruff fix..."
	ruff check --fix app tests

lint-fix: ## Ejecutar linting y arreglar automáticamente lo posible
	@echo "Running autoflake..."
	autoflake --in-place --remove-all-unused-imports --recursive app tests
	@echo "Running black..."
	black app tests
	@echo "Running isort..."
	isort app tests
	@echo "Running ruff fix..."
	ruff check --fix app tests

check-style: ## Verificar estilo de código sin hacer cambios
	@echo "Checking code style..."
	flake8 app tests
	black --check app tests
	isort --check-only app tests
	ruff check app tests

clean: ## Limpiar containers y volúmenes
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	docker system prune -f

migrations: ## Crear migración automática
	@echo "Creando migración automática..."
	powershell -Command "$$env:DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db'; alembic revision --autogenerate -m 'Auto migration'"

migrate: ## Aplicar migraciones pendientes
	@echo "Aplicando migraciones..."
	powershell -Command "$$env:DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db'; alembic upgrade head"

migrate-down: ## Hacer rollback de una migración
	@echo "Haciendo rollback de migración..."
	powershell -Command "$$env:DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db'; alembic downgrade -1"

migrate-history: ## Ver historial de migraciones
	powershell -Command "$$env:DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db'; alembic history"

migrate-current: ## Ver migración actual
	powershell -Command "$$env:DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db'; alembic current"

migrate-create: ## Crear migración manual (usar: make migrate-create MESSAGE="nombre")
	@echo "Creando migración manual: $(MESSAGE)"
	powershell -Command "$$env:DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5433/tareas_db'; alembic revision -m '$(MESSAGE)'"

run-local: ## Ejecutar servidor local sin Docker
	uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
