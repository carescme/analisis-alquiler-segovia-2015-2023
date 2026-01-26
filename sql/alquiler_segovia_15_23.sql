-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-01-2026 a las 11:18:40
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `alquiler_segovia_15_23`
--
CREATE DATABASE IF NOT EXISTS `alquiler_segovia_15_23` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `alquiler_segovia_15_23`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alquiler`
--

DROP TABLE IF EXISTS `alquiler`;
CREATE TABLE IF NOT EXISTS `alquiler` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cumun` int(11) NOT NULL,
  `anio` int(11) NOT NULL,
  `precio_m2_mediana` decimal(10,2) DEFAULT NULL,
  `alquiler_mensual_mediana` decimal(10,2) DEFAULT NULL,
  `superficie_mediana` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cumun` (`cumun`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `municipios`
--

DROP TABLE IF EXISTS `municipios`;
CREATE TABLE IF NOT EXISTS `municipios` (
  `cumun` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  PRIMARY KEY (`cumun`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `renta`
--

DROP TABLE IF EXISTS `renta`;
CREATE TABLE IF NOT EXISTS `renta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cumun` int(11) NOT NULL,
  `anio` int(11) NOT NULL,
  `indicador_tipo` varchar(255) DEFAULT NULL,
  `valor_euros` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cumun` (`cumun`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alquiler`
--
ALTER TABLE `alquiler`
  ADD CONSTRAINT `alquiler_ibfk_1` FOREIGN KEY (`cumun`) REFERENCES `municipios` (`cumun`) ON DELETE CASCADE;

--
-- Filtros para la tabla `renta`
--
ALTER TABLE `renta`
  ADD CONSTRAINT `renta_ibfk_1` FOREIGN KEY (`cumun`) REFERENCES `municipios` (`cumun`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
