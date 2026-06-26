"""
╔══════════════════════════════════════════════════════════════╗
║         PIPELINE ETL CON CIFRADO DE DATOS                    ║
║         Extract → Transform → Load + Encrypt/Decrypt         ║
╚══════════════════════════════════════════════════════════════╝

Arquitectura del proyecto:
  1. EXTRACT   - Genera/lee datos de clientes (simulando una fuente real)
  2. TRANSFORM - Limpia, valida y transforma los datos
  3. ENCRYPT   - Cifra campos sensibles con AES-128 (Fernet)
  4. LOAD      - Guarda los datos procesados en CSV/JSON
  5. DECRYPT   - Demuestra cómo recuperar los datos originales
"""

import os
import json
import csv
import hashlib
import logging
import base64
from datetime import datetime
from pathlib import Path

import pandas as pd
from faker import Faker
from colorama import Fore, Style, init
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ─────────────────────────────────────────────
#  Inicialización
# ─────────────────────────────────────────────
init(autoreset=True)
fake = Faker("es_MX")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Crear carpetas necesarias si no existen
for folder in ["logs", "data", "output"]:
    (BASE_DIR / folder).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=BASE_DIR / "logs" / "etl_run.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
OUTPUT_DIR = BASE_DIR / "output"

KEY_FILE = BASE_DIR / "secret.key"


# ══════════════════════════════════════════════
#  MÓDULO DE CIFRADO
# ══════════════════════════════════════════════
class CifradoManager:
    """
    Gestiona el cifrado y descifrado usando Fernet (AES-128-CBC + HMAC-SHA256).
    
    La clave puede generarse aleatoriamente o derivarse de una contraseña
    usando PBKDF2 con 480,000 iteraciones (recomendación NIST 2024).
    """

    def __init__(self, password: str = None):
        self.clave = self._obtener_o_crear_clave(password)
        self.fernet = Fernet(self.clave)
        self._log("🔐 CifradoManager inicializado correctamente")

    def _obtener_o_crear_clave(self, password: str) -> bytes:
        """Genera una clave desde contraseña (PBKDF2) o crea una aleatoria."""
        if password:
            # Derivar clave determinista desde contraseña
            salt = b"etl_proyecto_salt_2024"  # En producción: salt aleatorio guardado
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480_000,
            )
            clave_bytes = kdf.derive(password.encode())
            return base64.urlsafe_b64encode(clave_bytes)
        else:
            # Generar clave aleatoria y guardarla
            if KEY_FILE.exists():
                return KEY_FILE.read_bytes()
            clave = Fernet.generate_key()
            KEY_FILE.write_bytes(clave)
            return clave

    def cifrar(self, texto: str) -> str:
        """Cifra un string y retorna el texto cifrado en base64."""
        if not texto or str(texto).strip() == "":
            return ""
        return self.fernet.encrypt(str(texto).encode()).decode()

    def descifrar(self, texto_cifrado: str) -> str:
        """Descifra un string previamente cifrado."""
        if not texto_cifrado:
            return ""
        try:
            return self.fernet.decrypt(texto_cifrado.encode()).decode()
        except Exception:
            return "[ERROR: No se pudo descifrar]"

    def hash_irreversible(self, texto: str) -> str:
        """SHA-256 para campos que NO deben recuperarse (ej: contraseñas)."""
        return hashlib.sha256(str(texto).encode()).hexdigest()

    def _log(self, msg):
        logging.info(msg)


# ══════════════════════════════════════════════
#  FASE 1: EXTRACT (Extracción)
# ══════════════════════════════════════════════
class Extractor:
    """
    Simula la extracción de datos desde una fuente (BD, API, CSV).
    En este ejemplo genera datos sintéticos realistas con Faker.
    """

    def __init__(self, n_registros: int = 50):
        self.n = n_registros

    def extraer(self) -> pd.DataFrame:
        banner("FASE 1: EXTRACCIÓN DE DATOS", Fore.CYAN)
        print(f"  → Generando {self.n} registros de clientes simulados...\n")

        registros = []
        for i in range(self.n):
            registros.append({
                "id": i + 1,
                "nombre": fake.name(),
                "email": fake.email(),
                "telefono": fake.phone_number(),
                "direccion": fake.address().replace("\n", ", "),
                "tarjeta_credito": fake.credit_card_number(),
                "salario": round(fake.random.uniform(8000, 120000), 2),
                "fecha_registro": fake.date_between(start_date="-5y").isoformat(),
                "pais": fake.country(),
                "activo": fake.boolean(chance_of_getting_true=80),
                # Datos con errores intencionales para demostrar limpieza
                "edad": fake.random.choice([
                    fake.random_int(18, 75),
                    -1,       # valor inválido
                    None,     # nulo
                    999,      # outlier
                ]),
                "codigo_postal": fake.postcode(),
            })

        df = pd.DataFrame(registros)

        # Guardar datos crudos
        raw_path = DATA_DIR / "clientes_raw.csv"
        df.to_csv(raw_path, index=False)
        print(f"  ✅ Datos extraídos: {len(df)} registros")
        print(f"  💾 Guardados en: {raw_path}\n")
        logging.info(f"EXTRACT: {len(df)} registros extraídos")
        return df


# ══════════════════════════════════════════════
#  FASE 2: TRANSFORM (Transformación)
# ══════════════════════════════════════════════
class Transformador:
    """
    Limpia, valida y enriquece los datos antes del cifrado y carga.
    
    Operaciones:
      • Eliminar duplicados
      • Corregir tipos de datos
      • Validar rangos (edad, salario)
      • Imputar nulos
      • Normalizar texto (email en minúsculas, etc.)
      • Añadir columnas calculadas
    """

    def transformar(self, df: pd.DataFrame) -> pd.DataFrame:
        banner("FASE 2: TRANSFORMACIÓN Y LIMPIEZA", Fore.YELLOW)
        df_original = len(df)

        # 2.1 Eliminar duplicados
        df = df.drop_duplicates(subset=["email"])
        print(f"  🔄 Duplicados eliminados: {df_original - len(df)}")

        # 2.2 Limpiar y validar edades
        edades_invalidas = df["edad"].isna() | (df["edad"] < 0) | (df["edad"] > 120)
        df.loc[edades_invalidas, "edad"] = df["edad"].median()
        df["edad"] = df["edad"].astype(int)
        print(f"  🔄 Edades inválidas corregidas: {edades_invalidas.sum()}")

        # 2.3 Normalizar emails
        df["email"] = df["email"].str.lower().str.strip()

        # 2.4 Formatear teléfonos (solo dígitos)
        df["telefono"] = df["telefono"].str.replace(r"\D", "", regex=True)

        # 2.5 Validar salarios
        df.loc[df["salario"] < 0, "salario"] = 0

        # 2.6 Columnas calculadas
        df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])
        df["antiguedad_dias"] = (datetime.now() - df["fecha_registro"]).dt.days
        df["segmento"] = pd.cut(
            df["salario"],
            bins=[0, 20000, 50000, 100000, float("inf")],
            labels=["Básico", "Estándar", "Premium", "VIP"],
        )

        # 2.7 Flag de datos completos
        df["datos_completos"] = df[["nombre", "email", "telefono"]].notna().all(axis=1)

        print(f"  ✅ Registros finales limpios: {len(df)}")
        print(f"  ✅ Columnas añadidas: antiguedad_dias, segmento, datos_completos\n")
        logging.info(f"TRANSFORM: {len(df)} registros limpios")
        return df


# ══════════════════════════════════════════════
#  FASE 3: CIFRADO DE CAMPOS SENSIBLES
# ══════════════════════════════════════════════
class CifradoETL:
    """
    Aplica el cifrado selectivo sobre campos PII (Personally Identifiable Info).
    
    Estrategia:
      • CIFRADO REVERSIBLE (Fernet): email, teléfono, dirección, tarjeta, salario
      • HASH IRREVERSIBLE (SHA-256): id interno (para lookup sin exponer datos)
      • SIN CIFRAR: id, segmento, fechas, flags de negocio
    """

    # Campos que se cifrarán (datos sensibles / PII)
    CAMPOS_SENSIBLES = ["nombre", "email", "telefono", "direccion", "tarjeta_credito", "salario"]

    def __init__(self, cifrado: CifradoManager):
        self.cifrado = cifrado

    def cifrar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        banner("FASE 3: CIFRADO DE DATOS SENSIBLES", Fore.MAGENTA)
        df_cifrado = df.copy()

        print("  Campos que se cifran (reversible):")
        for campo in self.CAMPOS_SENSIBLES:
            if campo in df_cifrado.columns:
                df_cifrado[campo] = df_cifrado[campo].apply(
                    lambda x: self.cifrado.cifrar(str(x)) if pd.notna(x) else ""
                )
                print(f"    🔒 {campo}")

        # Hash irreversible del email original (para búsquedas seguras)
        df_cifrado["email_hash"] = df[["email"]].apply(
            lambda row: self.cifrado.hash_irreversible(row["email"]), axis=1
        )
        print("  Campo con hash irreversible (SHA-256):")
        print("    🔏 email_hash\n")

        print("  ✅ Cifrado completado")
        print(f"  🔑 Clave guardada en: {KEY_FILE}\n")
        logging.info("ENCRYPT: Cifrado aplicado a campos sensibles")
        return df_cifrado

    def descifrar_dataframe(self, df_cifrado: pd.DataFrame) -> pd.DataFrame:
        """Operación inversa: recupera los datos originales."""
        df_claro = df_cifrado.copy()
        for campo in self.CAMPOS_SENSIBLES:
            if campo in df_claro.columns:
                df_claro[campo] = df_claro[campo].apply(self.cifrado.descifrar)
        return df_claro


# ══════════════════════════════════════════════
#  FASE 4: LOAD (Carga)
# ══════════════════════════════════════════════
class Cargador:
    """Persiste los datos procesados y cifrados en múltiples formatos."""

    def cargar(self, df: pd.DataFrame, nombre_base: str = "clientes_cifrados"):
        banner("FASE 4: CARGA DE DATOS", Fore.GREEN)

        # CSV
        csv_path = OUTPUT_DIR / f"{nombre_base}.csv"
        df.to_csv(csv_path, index=False)
        print(f"  💾 CSV guardado:  {csv_path}")

        # JSON (línea por línea - ideal para streaming)
        json_path = OUTPUT_DIR / f"{nombre_base}.json"
        df.to_json(json_path, orient="records", indent=2, force_ascii=False)
        print(f"  💾 JSON guardado: {json_path}")

        # Resumen estadístico
        resumen = {
            "timestamp": datetime.now().isoformat(),
            "total_registros": len(df),
            "campos_cifrados": CifradoETL.CAMPOS_SENSIBLES,
            "columnas": list(df.columns),
            "segmentos": df["segmento"].value_counts().to_dict() if "segmento" in df.columns else {},
        }
        resumen_path = OUTPUT_DIR / "resumen_etl.json"
        with open(resumen_path, "w", encoding="utf-8") as f:
            json.dump(resumen, f, indent=2, ensure_ascii=False, default=str)
        print(f"  💾 Resumen:       {resumen_path}")
        print(f"\n  ✅ Carga completada: {len(df)} registros\n")
        logging.info(f"LOAD: {len(df)} registros guardados en {csv_path}")


# ══════════════════════════════════════════════
#  UTILIDADES DE PRESENTACIÓN
# ══════════════════════════════════════════════
def banner(titulo: str, color=Fore.WHITE):
    print(color + f"\n{'═' * 60}")
    print(f"  {titulo}")
    print(f"{'═' * 60}" + Style.RESET_ALL)


def mostrar_muestra(df: pd.DataFrame, titulo: str, n: int = 3):
    print(f"\n{Fore.WHITE}  📊 {titulo} (primeros {n} registros):{Style.RESET_ALL}")
    cols_mostrar = ["id", "nombre", "email", "salario", "segmento"]
    cols_disponibles = [c for c in cols_mostrar if c in df.columns]
    muestra = df[cols_disponibles].head(n).to_string(index=False)
    for linea in muestra.split("\n"):
        print(f"    {linea}")


def mostrar_comparacion(df_claro: pd.DataFrame, df_cifrado: pd.DataFrame, campo: str = "email"):
    banner("COMPARACIÓN: ANTES Y DESPUÉS DEL CIFRADO", Fore.BLUE)
    for i in range(min(3, len(df_claro))):
        original = str(df_claro[campo].iloc[i])[:40]
        cifrado = str(df_cifrado[campo].iloc[i])[:40] + "..."
        print(f"  Original : {Fore.GREEN}{original}{Style.RESET_ALL}")
        print(f"  Cifrado  : {Fore.RED}{cifrado}{Style.RESET_ALL}")
        print(f"  {'─' * 55}")


# ══════════════════════════════════════════════
#  PIPELINE PRINCIPAL
# ══════════════════════════════════════════════
def ejecutar_pipeline(n_registros: int = 50, password: str = "MiClaveSegura2024"):
    """Orquesta las 4 fases del pipeline ETL con cifrado."""

    print(Fore.CYAN + Style.BRIGHT)
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         PIPELINE ETL CON CIFRADO DE DATOS                   ║")
    print("║         Python · Fernet AES-128 · PBKDF2 · SHA-256          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)

    inicio = datetime.now()

    # Inicializar componentes
    cifrado_mgr = CifradoManager(password=password)
    extractor = Extractor(n_registros)
    transformador = Transformador()
    cifrador = CifradoETL(cifrado_mgr)
    cargador = Cargador()

    # ── Fase 1: Extract ──
    df_raw = extractor.extraer()
    mostrar_muestra(df_raw, "Datos Crudos (sin limpiar)")

    # ── Fase 2: Transform ──
    df_limpio = transformador.transformar(df_raw)
    mostrar_muestra(df_limpio, "Datos Transformados (limpios)")

    # ── Comparación pre-cifrado ──
    mostrar_comparacion(df_limpio, cifrador.cifrar_dataframe(df_limpio.copy()))

    # ── Fase 3: Encrypt ──
    df_cifrado = cifrador.cifrar_dataframe(df_limpio)

    # ── Fase 4: Load ──
    cargador.cargar(df_cifrado)

    # ── Demostración de Descifrado ──
    banner("BONUS: DEMOSTRACIÓN DE DESCIFRADO", Fore.CYAN)
    df_recuperado = cifrador.descifrar_dataframe(df_cifrado)
    print("  Verificando que los datos se recuperan correctamente...\n")
    for campo in ["nombre", "email", "salario"]:
        orig = str(df_limpio[campo].iloc[0])[:35]
        recup = str(df_recuperado[campo].iloc[0])[:35]
        igual = "✅" if orig == recup else "❌"
        print(f"  {igual} {campo}: '{orig}' → recuperado: '{recup}'")

    # ── Resumen Final ──
    duracion = (datetime.now() - inicio).total_seconds()
    banner("PIPELINE COMPLETADO", Fore.GREEN)
    print(f"  ⏱  Duración total    : {duracion:.2f} segundos")
    print(f"  📦 Registros procesados: {len(df_cifrado)}")
    print(f"  🔒 Campos cifrados   : {len(CifradoETL.CAMPOS_SENSIBLES)}")
    print(f"  📁 Salida en         : {OUTPUT_DIR}/")
    print(f"  📋 Log en            : logs/etl_run.log\n")
    logging.info(f"PIPELINE COMPLETADO en {duracion:.2f}s | {len(df_cifrado)} registros")


if __name__ == "__main__":
    ejecutar_pipeline(n_registros=50, password="MiClaveSegura2024")
