/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.12-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Parcial_1_db
-- ------------------------------------------------------
-- Server version	11.4.12-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `Bitacora`
--

DROP TABLE IF EXISTS `Bitacora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Bitacora` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `exitoso` binary(1) NOT NULL,
  `id_operacion` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  UNIQUE KEY `id_operacion` (`id_operacion`),
  UNIQUE KEY `hora` (`hora`),
  CONSTRAINT `Bitacora_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id`),
  CONSTRAINT `Bitacora_ibfk_2` FOREIGN KEY (`id_operacion`) REFERENCES `Operaciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Bitacora`
--

LOCK TABLES `Bitacora` WRITE;
/*!40000 ALTER TABLE `Bitacora` DISABLE KEYS */;
INSERT INTO `Bitacora` VALUES
(1,1,'1',1,'2026-06-01','08:15:00'),
(2,2,'1',3,'2026-06-01','09:42:00'),
(3,3,'0',5,'2026-06-02','10:05:00'),
(4,4,'1',4,'2026-06-02','11:30:00'),
(5,5,'1',8,'2026-06-03','13:20:00'),
(6,6,'1',6,'2026-06-04','14:55:00'),
(7,7,'1',10,'2026-06-05','15:10:00'),
(8,8,'0',9,'2026-06-08','16:45:00'),
(9,9,'1',2,'2026-06-09','17:30:00'),
(10,10,'1',7,'2026-06-10','18:05:00');
/*!40000 ALTER TABLE `Bitacora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Formas_de_Pago`
--

DROP TABLE IF EXISTS `Formas_de_Pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Formas_de_Pago` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `form_pay` varchar(100) NOT NULL,
  `activo` binary(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `form_pay` (`form_pay`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Formas_de_Pago`
--

LOCK TABLES `Formas_de_Pago` WRITE;
/*!40000 ALTER TABLE `Formas_de_Pago` DISABLE KEYS */;
INSERT INTO `Formas_de_Pago` VALUES
(1,'Efectivo','1'),
(2,'Tarjeta de Credito','1'),
(3,'Tarjeta de Debito','1'),
(4,'Transferencia Bancaria','1'),
(5,'Yappy','1'),
(6,'ACH','1'),
(7,'PayPal','1'),
(8,'Cheque','1'),
(9,'Criptomoneda','0'),
(10,'Nequi','0');
/*!40000 ALTER TABLE `Formas_de_Pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `LogView`
--

DROP TABLE IF EXISTS `LogView`;
/*!50001 DROP VIEW IF EXISTS `LogView`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `LogView` AS SELECT
 NULL AS `id_bitacora`,
 NULL AS `id_usuario`,
 NULL AS `usuario`,
 NULL AS `usuario_activo`,
 NULL AS `operacion`,
 NULL AS `requiere_password`,
 NULL AS `exitoso`,
 NULL AS `fecha`,
 NULL AS `hora` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `NoPassView`
--

DROP TABLE IF EXISTS `NoPassView`;
/*!50001 DROP VIEW IF EXISTS `NoPassView`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `NoPassView` AS SELECT
 NULL AS `id`,
 NULL AS `nombre`,
 NULL AS `apellido`,
 NULL AS `correo`,
 NULL AS `rol`,
 NULL AS `activo` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Operaciones`
--

DROP TABLE IF EXISTS `Operaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Operaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `soli_password` binary(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `descripcion` (`descripcion`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Operaciones`
--

LOCK TABLES `Operaciones` WRITE;
/*!40000 ALTER TABLE `Operaciones` DISABLE KEYS */;
INSERT INTO `Operaciones` VALUES
(1,'Inicio de sesion','1'),
(2,'Cierre de sesion','0'),
(3,'Registro de pago','1'),
(4,'Consulta de servicios','0'),
(5,'Cambio de contrasena','1'),
(6,'Creacion de usuario','1'),
(7,'Desactivacion de usuario','1'),
(8,'Actualizacion de perfil','0'),
(9,'Anulacion de pago','1'),
(10,'Exportacion de reportes','1');
/*!40000 ALTER TABLE `Operaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pagos`
--

DROP TABLE IF EXISTS `Pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pagos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `fecha_pago` date NOT NULL,
  `pendiente` binary(1) NOT NULL,
  `id_fop` int(11) NOT NULL,
  `num_ref` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `num_ref` (`num_ref`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_servicio` (`id_servicio`),
  KEY `id_fop` (`id_fop`),
  CONSTRAINT `Pagos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id`),
  CONSTRAINT `Pagos_ibfk_2` FOREIGN KEY (`id_servicio`) REFERENCES `Servicios` (`id`),
  CONSTRAINT `Pagos_ibfk_3` FOREIGN KEY (`id_fop`) REFERENCES `Formas_de_Pago` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pagos`
--

LOCK TABLES `Pagos` WRITE;
/*!40000 ALTER TABLE `Pagos` DISABLE KEYS */;
INSERT INTO `Pagos` VALUES
(1,2,1,'2026-06-01','0',2,'REF-2026-0001'),
(2,3,2,'2026-06-01','0',5,'REF-2026-0002'),
(3,5,4,'2026-06-02','0',1,'REF-2026-0003'),
(4,2,6,'2026-06-02','1',2,'REF-2026-0004'),
(5,8,3,'2026-06-03','0',4,'REF-2026-0005'),
(6,9,5,'2026-06-04','1',3,'REF-2026-0006'),
(7,3,7,'2026-06-05','0',6,'REF-2026-0007'),
(8,10,8,'2026-06-08','0',4,'REF-2026-0008'),
(9,5,9,'2026-06-09','1',7,'REF-2026-0009'),
(10,7,2,'2026-06-10','0',8,'REF-2026-0010');
/*!40000 ALTER TABLE `Pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `PagosDetView`
--

DROP TABLE IF EXISTS `PagosDetView`;
/*!50001 DROP VIEW IF EXISTS `PagosDetView`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `PagosDetView` AS SELECT
 NULL AS `id_pago`,
 NULL AS `id_usuario`,
 NULL AS `cliente`,
 NULL AS `rol_usuario`,
 NULL AS `servicio`,
 NULL AS `precio_servicio`,
 NULL AS `forma_pago`,
 NULL AS `fecha_pago`,
 NULL AS `pendiente`,
 NULL AS `num_ref` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Roles`
--

DROP TABLE IF EXISTS `Roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `activo` binary(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `descripcion` (`descripcion`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Roles`
--

LOCK TABLES `Roles` WRITE;
/*!40000 ALTER TABLE `Roles` DISABLE KEYS */;
INSERT INTO `Roles` VALUES
(1,'Administrador','1'),
(2,'Cliente','1'),
(3,'Soporte Tecnico','1'),
(4,'Supervisor','1'),
(5,'Contador','1'),
(6,'Vendedor','1'),
(7,'Auditor','1'),
(8,'Gerente','1'),
(9,'Recepcionista','0'),
(10,'Practicante','0');
/*!40000 ALTER TABLE `Roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Servicios`
--

DROP TABLE IF EXISTS `Servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Servicios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_service` varchar(100) NOT NULL,
  `activo` binary(1) NOT NULL,
  `Precio` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_service` (`name_service`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Servicios`
--

LOCK TABLES `Servicios` WRITE;
/*!40000 ALTER TABLE `Servicios` DISABLE KEYS */;
INSERT INTO `Servicios` VALUES
(1,'Internet Residencial 100MB','1',29.99),
(2,'Internet Residencial 300MB','1',44.99),
(3,'Internet Empresarial 500MB','1',89.99),
(4,'Television por Cable','1',24.5),
(5,'Telefonia Fija','1',12.75),
(6,'Streaming Premium','1',9.99),
(7,'Hosting Web Basico','1',15),
(8,'Soporte Tecnico Premium','1',35),
(9,'IP Estatica','1',18.5),
(10,'Internet Satelital','0',75);
/*!40000 ALTER TABLE `Servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuarios`
--

DROP TABLE IF EXISTS `Usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `activo` binary(1) NOT NULL,
  `correo` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  UNIQUE KEY `apellido` (`apellido`),
  UNIQUE KEY `pass` (`pass`),
  UNIQUE KEY `correo` (`correo`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `Usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `Roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuarios`
--

LOCK TABLES `Usuarios` WRITE;
/*!40000 ALTER TABLE `Usuarios` DISABLE KEYS */;
INSERT INTO `Usuarios` VALUES
(1,'Carlos','Mendoza','$2b$12$LJ3m4N5o6P7q8R9s0T1u2eXa',1,'1','carlos.mendoza@example.com'),
(2,'Maria','Gonzalez','$2b$12$Aa1Bb2Cc3Dd4Ee5Ff6Gg7hKm',2,'1','maria.gonzalez@example.com'),
(3,'Jose','Rodriguez','$2b$12$Hh8Ii9Jj0Kk1Ll2Mm3Nn4pQr',2,'1','jose.rodriguez@example.com'),
(4,'Ana','Castillo','$2b$12$Oo5Pp6Qq7Rr8Ss9Tt0Uu1vWx',3,'1','ana.castillo@example.com'),
(5,'Luis','Herrera','$2b$12$Vv2Ww3Xx4Yy5Zz6Aa7Bb8cDe',2,'1','luis.herrera@example.com'),
(6,'Carmen','Vasquez','$2b$12$Cc9Dd0Ee1Ff2Gg3Hh4Ii5jKl',4,'1','carmen.vasquez@example.com'),
(7,'Roberto','Pineda','$2b$12$Jj6Kk7Ll8Mm9Nn0Oo1Pp2qRs',5,'1','roberto.pineda@example.com'),
(8,'Sofia','Morales','$2b$12$Qq3Rr4Ss5Tt6Uu7Vv8Ww9xYz',6,'1','sofia.morales@example.com'),
(9,'Diego','Santos','$2b$12$Xx0Yy1Zz2Aa3Bb4Cc5Dd6eFg',2,'0','diego.santos@example.com'),
(10,'Patricia','Jimenez','$2b$12$Ee7Ff8Gg9Hh0Ii1Jj2Kk3lMn',8,'1','patricia.jimenez@example.com'),
(101,'Juan','Pérez','$2b$12$EjemploHashBcrypt',2,'0','juan.nuevo@email.com');
/*!40000 ALTER TABLE `Usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `LogView`
--

/*!50001 DROP VIEW IF EXISTS `LogView`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_uca1400_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`parcial_user`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `LogView` AS select `b`.`id` AS `id_bitacora`,`u`.`id` AS `id_usuario`,concat(`u`.`nombre`,' ',`u`.`apellido`) AS `usuario`,`u`.`activo` AS `usuario_activo`,`o`.`descripcion` AS `operacion`,`o`.`soli_password` AS `requiere_password`,`b`.`exitoso` AS `exitoso`,`b`.`fecha` AS `fecha`,`b`.`hora` AS `hora` from ((`Bitacora` `b` join `Usuarios` `u` on(`b`.`id_usuario` = `u`.`id`)) join `Operaciones` `o` on(`b`.`id_operacion` = `o`.`id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `NoPassView`
--

/*!50001 DROP VIEW IF EXISTS `NoPassView`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_uca1400_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`parcial_user`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `NoPassView` AS select `u`.`id` AS `id`,`u`.`nombre` AS `nombre`,`u`.`apellido` AS `apellido`,`u`.`correo` AS `correo`,`r`.`descripcion` AS `rol`,`u`.`activo` AS `activo` from (`Usuarios` `u` join `Roles` `r` on(`u`.`id_rol` = `r`.`id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `PagosDetView`
--

/*!50001 DROP VIEW IF EXISTS `PagosDetView`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_uca1400_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`parcial_user`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `PagosDetView` AS select `p`.`id` AS `id_pago`,`u`.`id` AS `id_usuario`,concat(`u`.`nombre`,' ',`u`.`apellido`) AS `cliente`,`r`.`descripcion` AS `rol_usuario`,`s`.`name_service` AS `servicio`,`s`.`Precio` AS `precio_servicio`,`fp`.`form_pay` AS `forma_pago`,`p`.`fecha_pago` AS `fecha_pago`,`p`.`pendiente` AS `pendiente`,`p`.`num_ref` AS `num_ref` from ((((`Pagos` `p` join `Usuarios` `u` on(`p`.`id_usuario` = `u`.`id`)) join `Servicios` `s` on(`p`.`id_servicio` = `s`.`id`)) join `Formas_de_Pago` `fp` on(`p`.`id_fop` = `fp`.`id`)) join `Roles` `r` on(`u`.`id_rol` = `r`.`id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-06-25  2:55:47
