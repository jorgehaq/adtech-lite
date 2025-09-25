# AXI-Lite 📊

**Batch Analytics API with Django**  
Demo API para subir datasets CSV, procesarlos con Pandas y obtener métricas básicas.  

Pensado como **proyecto de portafolio**: ligero, entendible en 5 minutos, pero con patrones de producción (multi-tenant, JWT, migraciones, Docker, CI/CD).

---

## 🎯 Pitch rápido
- **Qué hace:** subes datasets CSV (hasta 200MB), obtienes métricas (`summary`, `correlation`).
- **Para qué sirve:** simula una API SaaS de analítica batch para múltiples clientes.
- **Stack:** Django + DRF + PostgreSQL + Redis + Docker.

---

## ✨ Features
- **Autenticación JWT**  
- **Multi-tenant básico** (middleware con `tenant_id`)  
- Endpoints REST:
  - `POST /datasets/` → subir dataset CSV  
  - `GET /datasets/{id}/analyze` → métricas (`summary`, `correlation`)  
- Healthcheck (`/health/`)  
- Tests con pytest para auth, datasets y análisis  

---

## 🐳 Correr en Local

```bash
# Levantar entorno local
make dev

# Resetear DB y aplicar migraciones
make reset-db

# API disponible en
http://localhost:8000/api/docs
```

Servicios:
- API → `http://localhost:8000`
- Postgres → `localhost:5432`
- Redis → `localhost:6379`

---

## 🧪 Tests

```bash
make test
```

Valida:
- Autenticación JWT
- Subida de datasets CSV
- Análisis con Pandas (`describe`, `corr`)
- Healthcheck

---

## 🚀 Deploy en GCP

```bash
make deploy
```

Infraestructura:
- Cloud Run (Django API)
- CloudSQL (Postgres)
- Redis Memorystore

---

## ⚖️ Tradeoffs

- Usé **Django** (ORM robusto, admin, auth) → ideal para batch/data APIs.
- Multi-tenant simple vía middleware → suficiente para demo.
- Analítica básica con Pandas → ligera, pero fácil de explicar.
- No usé Spark/BigQuery → demasiado complejo para este scope.

---

## 📌 Cómo contarlo en entrevista

> “AXI-Lite es un demo batch analytics API en Django. Puedes subir datasets CSV y obtener métricas (summary, correlation) con multi-tenant y JWT.  
> Corre local con Docker y se despliega en GCP con Postgres y Redis. Lo mantuve ligero pero production-ready con migraciones, pytest y Makefile.”

👉 Explicable en **5 minutos**, encaja perfecto con **Adtech-Lite** como complemento (batch vs realtime).
