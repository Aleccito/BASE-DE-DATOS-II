-- =====================================================================
-- TALLER2 - Sistema de Gestion de Expedientes Vehiculares
-- Script de creacion de base de datos para MySQL 8+
--
-- Entidades identificadas a partir del diagrama entidad-relacion:
--   ASEGURADORAS, USUARIO, JUZGADOS, VEHICULOS, MODELOS, MARCAS, EXPEDIENTES
--
-- NOTA SOBRE INCONSISTENCIAS DETECTADAS EN EL DIAGRAMA ORIGINAL:
--   1) La tabla MODELOS tenia su PK etiquetada como "id_juzgado" (copiado
--      por error de otra entidad). Se corrigio a "id_modelo".
--   2) La tabla MARCAS tenia su PK etiquetada como "id_modelo" (copiado
--      por error de otra entidad). Se corrigio a "id_marca".
--   3) La FK de VEHICULOS hacia MODELOS aparecia como "id_modelos" (plural).
--      Se normalizo a "id_modelo" para mantener consistencia con la PK.
--   4) La columna "año" de VEHICULOS se renombro a "anio" para evitar
--      problemas de codificacion/portabilidad en identificadores SQL/Python.
--   5) El diagrama no define atributos de autenticacion en USUARIO
--      (correo/contraseña). Se agregaron "correo" y "password_hash" como
--      campos necesarios para implementar el login JWT solicitado.
--   6) No se especifican tipos de dato, longitudes ni obligatoriedad en el
--      diagrama; se infirieron tipos razonables (VARCHAR, DATE, etc.) y se
--      agregaron columnas de auditoria (fecha_creacion) por buena practica.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS taller2_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE taller2_db;

SET FOREIGN_KEY_CHECKS = 0;

-- ---------------------------------------------------------------------
-- Tabla: aseguradoras
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS aseguradoras;
CREATE TABLE aseguradoras (
    id_aseguradora  INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(150) NOT NULL,
    fecha_creacion  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_aseguradoras_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: juzgados
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS juzgados;
CREATE TABLE juzgados (
    id_juzgado          INT AUTO_INCREMENT PRIMARY KEY,
    region              VARCHAR(100) NOT NULL,
    numero_de_juzgado   VARCHAR(50)  NOT NULL,
    ubicacion           VARCHAR(200) NOT NULL,
    fecha_creacion      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_juzgados_region_numero UNIQUE (region, numero_de_juzgado)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: marcas
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS marcas;
CREATE TABLE marcas (
    id_marca        INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    fecha_creacion  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_marcas_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: modelos
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS modelos;
CREATE TABLE modelos (
    id_modelo       INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    fecha_creacion  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_modelos_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: usuario
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
    id_usuario      INT AUTO_INCREMENT PRIMARY KEY,
    id_aseguradora  INT NULL,
    nombre          VARCHAR(100) NOT NULL,
    apellido        VARCHAR(100) NOT NULL,
    identificacion  VARCHAR(50)  NOT NULL,
    correo          VARCHAR(150) NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    rol             VARCHAR(20)  NOT NULL DEFAULT 'usuario',
    fecha_creacion  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_usuario_identificacion UNIQUE (identificacion),
    CONSTRAINT uq_usuario_correo UNIQUE (correo),
    CONSTRAINT fk_usuario_aseguradora
        FOREIGN KEY (id_aseguradora) REFERENCES aseguradoras (id_aseguradora)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: vehiculos
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS vehiculos;
CREATE TABLE vehiculos (
    id_vehiculo     INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario      INT NOT NULL,
    id_modelo       INT NOT NULL,
    id_marca        INT NOT NULL,
    matricula       VARCHAR(20) NOT NULL,
    chasis          VARCHAR(50) NOT NULL,
    anio            INT NOT NULL,
    tipo            VARCHAR(50) NOT NULL,
    color           VARCHAR(30) NOT NULL,
    fecha_creacion  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_vehiculos_matricula UNIQUE (matricula),
    CONSTRAINT uq_vehiculos_chasis UNIQUE (chasis),
    CONSTRAINT chk_vehiculos_anio CHECK (anio BETWEEN 1900 AND 2100),
    CONSTRAINT fk_vehiculos_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_vehiculos_modelo
        FOREIGN KEY (id_modelo) REFERENCES modelos (id_modelo)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_vehiculos_marca
        FOREIGN KEY (id_marca) REFERENCES marcas (id_marca)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Tabla: expedientes
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS expedientes;
CREATE TABLE expedientes (
    id_expediente   INT AUTO_INCREMENT PRIMARY KEY,
    id_aseguradora  INT NOT NULL,
    id_juzgado      INT NOT NULL,
    id_usuario      INT NOT NULL,
    id_vehiculo     INT NOT NULL,
    estado          VARCHAR(30) NOT NULL DEFAULT 'abierto',
    fecha           DATE NOT NULL,
    fecha_creacion  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_expedientes_estado
        CHECK (estado IN ('abierto','en_proceso','cerrado','archivado')),
    CONSTRAINT fk_expedientes_aseguradora
        FOREIGN KEY (id_aseguradora) REFERENCES aseguradoras (id_aseguradora)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_expedientes_juzgado
        FOREIGN KEY (id_juzgado) REFERENCES juzgados (id_juzgado)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_expedientes_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_expedientes_vehiculo
        FOREIGN KEY (id_vehiculo) REFERENCES vehiculos (id_vehiculo)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Indices adicionales para busquedas frecuentes
-- ---------------------------------------------------------------------
CREATE INDEX idx_usuario_aseguradora ON usuario (id_aseguradora);
CREATE INDEX idx_vehiculos_usuario ON vehiculos (id_usuario);
CREATE INDEX idx_vehiculos_modelo ON vehiculos (id_modelo);
CREATE INDEX idx_vehiculos_marca ON vehiculos (id_marca);
CREATE INDEX idx_expedientes_aseguradora ON expedientes (id_aseguradora);
CREATE INDEX idx_expedientes_juzgado ON expedientes (id_juzgado);
CREATE INDEX idx_expedientes_usuario ON expedientes (id_usuario);
CREATE INDEX idx_expedientes_vehiculo ON expedientes (id_vehiculo);
CREATE INDEX idx_expedientes_estado ON expedientes (estado);

SET FOREIGN_KEY_CHECKS = 1;
