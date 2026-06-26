

**ETL** significa **Extract, Transform, Load** (Extraer, Transformar, Cargar).
Es el proceso estándar para mover y procesar datos entre sistemas.

```
[FUENTE DE DATOS]
    ↓  EXTRACT   → Leer datos desde CSV, API, Base de Datos...
    ↓  TRANSFORM → Limpiar, validar, enriquecer...
    ↓  ENCRYPT   → Cifrar campos sensibles (PII)
    ↓  LOAD      → Guardar en destino final
```

---

## Estructura del Proyecto

```
etl_project/
│
├── etl_pipeline.py       ← Pipeline principal (4 fases)
├── secret.key            ← Clave de cifrado (generada automáticamente)
│
├── data/
│   └── clientes_raw.csv  ← Datos extraídos sin procesar
│
├── output/
│   ├── clientes_cifrados.csv  ← Datos finales cifrados
│   ├── clientes_cifrados.json ← Mismo contenido en JSON
│   └── resumen_etl.json       ← Métricas del pipeline
│
└── logs/
    └── etl_run.log       ← Registro de cada ejecución
```

---

## Cómo ejecutar

```bash
# Instalar dependencias
pip install cryptography pandas faker colorama

# Ejecutar el pipeline
python etl_pipeline.py
```

---
