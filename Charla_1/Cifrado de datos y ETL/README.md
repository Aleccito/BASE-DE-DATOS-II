# 🔐 Pipeline ETL con Cifrado de Datos

## ¿Qué es ETL?

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

## 🏗 Estructura del Proyecto

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

## 🔒 Estrategia de Cifrado

| Campo            | Método        | Recuperable | Por qué |
|------------------|---------------|-------------|---------|
| nombre           | Fernet AES-128 | ✅ Sí       | Necesario para contactar al cliente |
| email            | Fernet AES-128 | ✅ Sí       | Para enviar comunicaciones |
| teléfono         | Fernet AES-128 | ✅ Sí       | Contacto |
| tarjeta_crédito  | Fernet AES-128 | ✅ Sí       | Datos financieros |
| salario          | Fernet AES-128 | ✅ Sí       | Dato confidencial |
| email_hash       | SHA-256        | ❌ No       | Para búsquedas sin exponer email real |
| id, segmento...  | Sin cifrar     | —           | Datos no sensibles |

### ¿Qué es Fernet?
- Implementa **AES-128-CBC** (cifrado de bloque)
- Añade **HMAC-SHA256** para verificar integridad
- Genera un token que incluye: IV aleatorio + texto cifrado + firma

### ¿Qué es PBKDF2?
- Deriva una clave criptográfica desde una contraseña humana
- Usa **480,000 iteraciones** para ser resistente a ataques de fuerza bruta
- Estándar recomendado por NIST (2024)

---

## 🚀 Cómo ejecutar

```bash
# Instalar dependencias
pip install cryptography pandas faker colorama

# Ejecutar el pipeline
python etl_pipeline.py
```

---

## 🛡 Cumplimiento Regulatorio

Este diseño ayuda a cumplir con:
- **GDPR** (Europa): Protección de datos personales
- **CCPA** (California): Privacidad del consumidor  
- **PCI-DSS**: Seguridad de datos de tarjetas de crédito
- **LGPD** (Brasil): Lei Geral de Proteção de Dados
