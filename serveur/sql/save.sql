-- MySQL dump 10.13  Distrib 8.0.35, for Win64 (x86_64)
--
-- Host: localhost    Database: serveur
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(50) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom_utilisateur` (`nom_utilisateur`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'toto','31f7a65e315586ac198bd798b6629ce4903d0899476d5741a9f32e2e521b6a66'),(2,'titi','cce66316b4c1c59df94a35afb80cecd82d1a8d91b554022557e115f5c275f515');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bannis`
--

DROP TABLE IF EXISTS `bannis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bannis` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `duree` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bannis`
--

LOCK TABLES `bannis` WRITE;
/*!40000 ALTER TABLE `bannis` DISABLE KEYS */;
INSERT INTO `bannis` VALUES (1,'tete','2023-12-04 20:08:20',60),(2,'tete','2023-12-04 20:10:09',60),(3,'toto','2023-12-04 20:39:44',60),(4,'toto','2023-12-04 20:43:30',60),(5,'toto','2023-12-04 20:44:01',120);
/*!40000 ALTER TABLE `bannis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historique`
--

DROP TABLE IF EXISTS `historique`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historique` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender` varchar(50) NOT NULL,
  `message` text NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=270 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historique`
--

LOCK TABLES `historique` WRITE;
/*!40000 ALTER TABLE `historique` DISABLE KEYS */;
INSERT INTO `historique` VALUES (1,'tata','test','2023-12-02 20:33:16'),(2,'tete','test','2023-12-02 20:33:18'),(3,'Serveur','tata a quitté la discussion.','2023-12-02 20:33:22'),(4,'Serveur','tata a été kick.','2023-12-02 20:33:45'),(5,'cherine','salut !','2023-12-02 20:40:55'),(6,'toto','yo','2023-12-02 20:40:58'),(7,'Serveur','toto a été kick.','2023-12-02 20:41:01'),(8,'Serveur','zack a quitté la discussion.','2023-12-10 07:28:39'),(9,'tete','salut','2023-12-10 07:28:54'),(10,'toto','salut','2023-12-10 07:28:57'),(11,'tete','ça va bien mon gars sur','2023-12-10 07:29:06'),(12,'Serveur','tete a été kick.','2023-12-10 07:29:20'),(13,'tete','salut','2023-12-10 16:56:54'),(14,'tete','yo','2023-12-10 16:57:01'),(15,'Serveur','toto a quitté la discussion.','2023-12-10 16:57:07'),(16,'toto','hey','2023-12-10 16:57:55'),(17,'toto','Salut !','2023-12-10 16:58:00'),(18,'toto','Hey loser','2023-12-10 16:58:59'),(19,'Serveur','toto a quitté la discussion.','2023-12-10 16:59:05'),(20,'Serveur','toto a quitté la discussion.','2023-12-10 16:59:19'),(21,'toto','jdfgdhfg','2023-12-10 16:59:43'),(22,'Serveur','toto a quitté la discussion.','2023-12-10 16:59:57'),(23,'toto','Salut !','2023-12-10 17:13:35'),(24,'Serveur','toto a quitté la discussion.','2023-12-10 17:13:52'),(25,'Serveur','toto a quitté la discussion.','2023-12-10 17:21:54'),(26,'tete','salut','2023-12-10 17:22:19'),(27,'Serveur','toto a quitté la discussion.','2023-12-10 17:22:27'),(28,'Serveur','toto a quitté la discussion.','2023-12-10 17:26:15'),(29,'toto','Salut','2023-12-10 17:27:06'),(30,'tete','yo','2023-12-10 17:27:09'),(31,'tete','Hehe','2023-12-10 17:27:16'),(32,'toto','hehe','2023-12-10 17:27:22'),(33,'Serveur','tete a quitté la discussion.','2023-12-10 17:27:43'),(34,'tete','Salut !','2023-12-10 17:28:40'),(35,'toto','dfghfgh','2023-12-10 17:28:50'),(36,'Serveur','tete a quitté la discussion.','2023-12-10 17:32:32'),(37,'Serveur','Le serveur ferme dans 3','2023-12-13 22:10:53'),(38,'Serveur','Le serveur ferme dans 2','2023-12-13 22:10:54'),(39,'Serveur','Le serveur ferme dans 1','2023-12-13 22:10:55'),(40,'tete','Hello !','2023-12-18 20:19:19'),(41,'toto','Hiiii','2023-12-18 20:19:29'),(42,'Serveur','tete a quitté la discussion.','2023-12-18 20:20:05'),(43,'tete','dffd','2023-12-18 21:12:18'),(44,'tete','dfdf','2023-12-18 21:12:20'),(45,'toto','HOLAAAAA','2023-12-18 21:12:32'),(46,'tete','HEyyyy wassup','2023-12-18 21:12:47'),(47,'Serveur','toto a quitté la discussion.','2023-12-18 21:12:59'),(48,'tete','hey','2023-12-18 21:19:07'),(49,'tete','hey','2023-12-18 21:19:07'),(50,'toto','Hi','2023-12-18 21:19:13'),(51,'toto','Hi','2023-12-18 21:19:13'),(52,'tete','wassup','2023-12-18 21:19:18'),(53,'tete','wassup','2023-12-18 21:19:18'),(54,'Serveur','tete a quitté la discussion.','2023-12-18 21:19:34'),(55,'toto','Heyyy wassup','2023-12-18 21:20:54'),(56,'toto','Heyyy wassup','2023-12-18 21:20:54'),(57,'tete','HOLAAA','2023-12-18 21:21:00'),(58,'tete','HOLAAA','2023-12-18 21:21:00'),(59,'toto','Bonjourno','2023-12-18 21:21:08'),(60,'toto','Bonjourno','2023-12-18 21:21:08'),(61,'toto','Enfin bref','2023-12-18 21:23:31'),(62,'toto','Enfin bref','2023-12-18 21:23:31'),(63,'toto','MAIS REPONNNND','2023-12-18 21:23:37'),(64,'toto','MAIS REPONNNND','2023-12-18 21:23:37'),(65,'toto','lmghjhxg','2023-12-18 21:23:49'),(66,'toto','lmghjhxg','2023-12-18 21:23:49'),(67,'toto','gjghj','2023-12-18 21:23:52'),(68,'toto','gjghj','2023-12-18 21:23:52'),(69,'toto','ghjghj','2023-12-18 21:23:53'),(70,'toto','ghjghj','2023-12-18 21:23:53'),(71,'toto','ghjghj','2023-12-18 21:23:54'),(72,'toto','ghjghj','2023-12-18 21:23:54'),(73,'toto','ghjghjghj','2023-12-18 21:23:56'),(74,'toto','ghjghjghj','2023-12-18 21:23:56'),(75,'toto','gjhgjhgjhgjgjh','2023-12-18 21:23:58'),(76,'toto','gjhgjhgjhgjgjh','2023-12-18 21:23:58'),(77,'toto','ghjghjghjghj','2023-12-18 21:24:00'),(78,'toto','ghjghjghjghj','2023-12-18 21:24:00'),(79,'toto','dfghfgshfgh','2023-12-18 21:24:20'),(80,'toto','dfghfgshfgh','2023-12-18 21:24:20'),(81,'toto','gf','2023-12-18 21:24:21'),(82,'toto','gf','2023-12-18 21:24:21'),(83,'toto','f','2023-12-18 21:24:22'),(84,'toto','f','2023-12-18 21:24:22'),(85,'toto','f','2023-12-18 21:24:24'),(86,'toto','f','2023-12-18 21:24:24'),(87,'toto','f','2023-12-18 21:24:25'),(88,'toto','f','2023-12-18 21:24:25'),(89,'toto','f','2023-12-18 21:24:26'),(90,'toto','f','2023-12-18 21:24:26'),(91,'toto','f','2023-12-18 21:24:27'),(92,'toto','f','2023-12-18 21:24:27'),(93,'toto','f','2023-12-18 21:24:28'),(94,'toto','f','2023-12-18 21:24:28'),(95,'toto','ff','2023-12-18 21:24:30'),(96,'toto','ff','2023-12-18 21:24:30'),(97,'toto','fff','2023-12-18 21:24:32'),(98,'toto','fff','2023-12-18 21:24:32'),(99,'toto','fff','2023-12-18 21:24:33'),(100,'toto','fff','2023-12-18 21:24:33'),(101,'toto','ffffff','2023-12-18 21:24:36'),(102,'toto','ffffff','2023-12-18 21:24:36'),(103,'toto','LE ROULEAU MARCHE YOUHOOO','2023-12-18 21:24:52'),(104,'toto','LE ROULEAU MARCHE YOUHOOO','2023-12-18 21:24:52'),(105,'Serveur','toto a quitté la discussion.','2023-12-18 21:25:11'),(106,'tete','hey babe','2023-12-18 21:35:00'),(107,'toto','Hii','2023-12-18 21:35:10'),(108,'toto','Hii','2023-12-18 21:35:10'),(109,'tete','ca va?','2023-12-18 21:35:20'),(110,'tete','ca va?','2023-12-18 21:35:20'),(111,'toto','ça va bien et toi ?','2023-12-18 21:35:28'),(112,'toto','ça va bien et toi ?','2023-12-18 21:35:28'),(113,'tete','oui , je suis fiere de toi ...','2023-12-18 21:35:41'),(114,'tete','oui , je suis fiere de toi ...','2023-12-18 21:35:41'),(115,'toto','Je sais, moi aussi :))','2023-12-18 21:35:52'),(116,'toto','Je sais, moi aussi :))','2023-12-18 21:35:52'),(117,'Serveur','toto a quitté la discussion.','2023-12-18 21:36:12'),(118,'toto123','hey !','2023-12-23 18:47:58'),(119,'toto','Heyyy','2023-12-23 18:48:15'),(120,'toto','Heyyy','2023-12-23 18:48:15'),(121,'toto123','je crois que je parle à un loser','2023-12-23 18:48:26'),(122,'toto123','je crois que je parle à un loser','2023-12-23 18:48:26'),(123,'toto','HEY','2023-12-23 18:48:31'),(124,'toto','HEY','2023-12-23 18:48:31'),(125,'toto123','troll','2023-12-23 18:48:38'),(126,'toto123','troll','2023-12-23 18:48:38'),(127,'Serveur','toto a été kick.','2023-12-23 18:48:52'),(128,'toto','yay','2023-12-24 08:26:31'),(129,'tete','hi','2023-12-24 08:37:04'),(130,'toto','Hello','2023-12-24 08:37:13'),(131,'tete','wassup','2023-12-24 08:37:21'),(132,'Serveur','toto a quitté la discussion.','2023-12-24 08:38:07'),(133,'tete','hey','2023-12-24 09:46:15'),(134,'Serveur','toto a quitté la discussion.','2023-12-24 09:46:24'),(135,'toto','Hey kloetito','2023-12-24 17:20:00'),(136,'kloetito','HELLOOOO','2023-12-24 17:20:08'),(137,'Serveur','toto a quitté la discussion.','2023-12-24 17:20:28'),(138,'Serveur','Le serveur ferme dans 3','2023-12-26 07:27:39'),(139,'Serveur','Le serveur ferme dans 2','2023-12-26 07:27:40'),(140,'Serveur','Le serveur ferme dans 1','2023-12-26 07:27:41'),(141,'Serveur','Le serveur ferme dans 3','2023-12-26 07:28:29'),(142,'Serveur','Le serveur ferme dans 2','2023-12-26 07:28:30'),(143,'Serveur','Le serveur ferme dans 1','2023-12-26 07:28:31'),(144,'1','q5rN0rt81mwgr87FzuCv7QSdZTyb1mLt','2023-12-26 07:28:32'),(145,'Serveur','Le serveur ferme dans 3','2023-12-26 07:30:30'),(146,'Serveur','Le serveur ferme dans 2','2023-12-26 07:30:31'),(147,'Serveur','Le serveur ferme dans 1','2023-12-26 07:30:32'),(148,'1','q5rN0rt81mwgr87FzuCv7QSdZTyb1mLt','2023-12-26 07:30:33'),(149,'Serveur','Le serveur ferme dans 3','2023-12-26 07:31:29'),(150,'Serveur','Le serveur ferme dans 2','2023-12-26 07:31:30'),(151,'Serveur','Le serveur ferme dans 1','2023-12-26 07:31:31'),(152,'1','q5rN0rt81mwgr87FzuCv7QSdZTyb1mLt','2023-12-26 07:31:32'),(153,'Serveur','Le serveur ferme dans 3','2023-12-26 07:34:34'),(154,'Serveur','Le serveur ferme dans 2','2023-12-26 07:34:35'),(155,'Serveur','Le serveur ferme dans 1','2023-12-26 07:34:36'),(156,'1','q5rN0rt81mwgr87FzuCv7QSdZTyb1mLt','2023-12-26 07:34:37'),(157,'Serveur','Le serveur ferme dans 3','2023-12-26 07:39:23'),(158,'Serveur','Le serveur ferme dans 2','2023-12-26 07:39:24'),(159,'Serveur','Le serveur ferme dans 1','2023-12-26 07:39:25'),(160,'Serveur','Le serveur ferme dans 3','2023-12-26 07:40:43'),(161,'Serveur','Le serveur ferme dans 2','2023-12-26 07:40:44'),(162,'Serveur','Le serveur ferme dans 1','2023-12-26 07:40:45'),(163,'Serveur','Le serveur ferme dans 3','2023-12-26 07:43:19'),(164,'Serveur','Le serveur ferme dans 2','2023-12-26 07:43:20'),(165,'Serveur','Le serveur ferme dans 1','2023-12-26 07:43:21'),(166,'Serveur','Le serveur ferme dans 3','2023-12-26 07:44:54'),(167,'Serveur','Le serveur ferme dans 2','2023-12-26 07:44:55'),(168,'Serveur','Le serveur ferme dans 1','2023-12-26 07:44:56'),(169,'az','hey i\'m az','2023-12-26 10:23:32'),(170,'toto','hi az','2023-12-26 10:23:44'),(171,'Serveur','toto a quitté la discussion.','2023-12-26 10:23:45'),(172,'tete','toto, tete','2023-12-26 10:32:33'),(173,'Serveur','tete a quitté la discussion.','2023-12-26 10:32:38'),(174,'az','hey','2023-12-27 17:51:12'),(175,'az','hey','2023-12-27 17:51:12'),(176,'toto','toto, tete, az','2023-12-27 17:51:19'),(177,'toto','toto, tete, az','2023-12-27 17:51:19'),(178,'Serveur','toto a quitté la discussion.','2023-12-27 17:51:44'),(179,'Serveur','toto a quitté la discussion.','2023-12-27 17:51:44'),(180,'Serveur','tete a quitté la discussion.','2023-12-27 17:51:44'),(181,'toto','toto, tete, az','2023-12-27 18:01:47'),(182,'toto','toto, tete, az','2023-12-27 18:01:47'),(183,'toto',' toto, tete, az\n','2023-12-27 18:01:47'),(184,'toto',' toto, tete, az\n','2023-12-27 18:01:47'),(185,'Serveur','toto a quitté la discussion.','2023-12-27 18:01:50'),(186,'Serveur','toto a quitté la discussion.','2023-12-27 18:01:50'),(187,'Serveur','az a quitté la discussion.','2023-12-27 18:01:51'),(188,'az','toto, tete, az','2023-12-27 18:07:34'),(189,'az','toto, tete, az','2023-12-27 18:07:34'),(190,'az',' toto, tete, az\n','2023-12-27 18:07:34'),(191,'az',' toto, tete, az\n','2023-12-27 18:07:34'),(192,'az','toto, tete, az','2023-12-27 18:07:54'),(193,'az','toto, tete, az','2023-12-27 18:07:54'),(194,'az',' toto, tete, az\n','2023-12-27 18:07:54'),(195,'az',' toto, tete, az\n','2023-12-27 18:07:54'),(196,'Serveur','az a quitté la discussion.','2023-12-27 18:07:58'),(197,'Serveur','az a quitté la discussion.','2023-12-27 18:07:58'),(198,'Serveur','toto a quitté la discussion.','2023-12-27 18:08:03'),(199,'az','fhjfgoih','2023-12-27 18:19:33'),(200,'az','fhjfgoih','2023-12-27 18:19:33'),(201,'az','toto, tete, az','2023-12-27 18:19:36'),(202,'az','toto, tete, az','2023-12-27 18:19:36'),(203,'az',' toto, tete, az\n','2023-12-27 18:19:36'),(204,'az',' toto, tete, az\n','2023-12-27 18:19:36'),(205,'Serveur','az a quitté la discussion.','2023-12-27 18:20:35'),(206,'Serveur','az a quitté la discussion.','2023-12-27 18:20:36'),(207,'Serveur','tete a quitté la discussion.','2023-12-27 18:20:37'),(208,'tete','toto, az, tete','2023-12-27 18:24:07'),(209,'tete','toto, az, tete','2023-12-27 18:24:07'),(210,'tete',' toto, az, tete\n','2023-12-27 18:24:07'),(211,'tete',' toto, az, tete\n','2023-12-27 18:24:07'),(212,'Serveur','tete a quitté la discussion.','2023-12-27 18:24:27'),(213,'Serveur','tete a quitté la discussion.','2023-12-27 18:24:27'),(214,'Serveur','az a quitté la discussion.','2023-12-27 18:24:31'),(215,'tete','toto, tete','2023-12-27 18:27:04'),(216,'tete',' toto, tete\n','2023-12-27 18:27:05'),(217,'Serveur','tete a quitté la discussion.','2023-12-27 18:27:10'),(218,'tete','toto, tete','2023-12-27 19:27:15'),(219,'tete',' toto, tete\n','2023-12-27 19:27:15'),(220,'Serveur','tete a quitté la discussion.','2023-12-27 19:27:27'),(221,'toto','toto, tete, az','2023-12-27 19:31:58'),(222,'toto','toto, tete, az','2023-12-27 19:31:58'),(223,'toto',' toto, tete, az\n','2023-12-27 19:31:58'),(224,'toto',' toto, tete, az\n','2023-12-27 19:31:58'),(225,'Serveur','toto a quitté la discussion.','2023-12-27 19:33:27'),(226,'Serveur','toto a quitté la discussion.','2023-12-27 19:33:27'),(227,'Serveur','tete a quitté la discussion.','2023-12-27 19:33:28'),(228,'az','toto, tete, az','2023-12-27 19:34:25'),(229,'az','toto, tete, az','2023-12-27 19:34:25'),(230,'az',' toto, tete, az','2023-12-27 19:34:25'),(231,'az',' toto, tete, az','2023-12-27 19:34:25'),(232,'Serveur','az a quitté la discussion.','2023-12-27 19:34:58'),(233,'Serveur','az a quitté la discussion.','2023-12-27 19:34:58'),(234,'az','toto, tete, az','2023-12-27 19:35:08'),(235,'az','toto, tete, az','2023-12-27 19:35:08'),(236,'az',' toto, tete, az','2023-12-27 19:35:08'),(237,'az',' toto, tete, az','2023-12-27 19:35:08'),(238,'Serveur','tete a quitté la discussion.','2023-12-27 19:35:46'),(239,'Serveur','tete a quitté la discussion.','2023-12-27 19:35:46'),(240,'Serveur','toto a quitté la discussion.','2023-12-27 19:35:48'),(241,'toto','toto, tete','2023-12-27 19:37:13'),(242,'toto',' toto, tete','2023-12-27 19:37:14'),(243,'Serveur','tete a quitté la discussion.','2023-12-27 19:38:20'),(244,'az','toto, tete, az','2023-12-28 09:53:41'),(245,'az','toto, tete, az','2023-12-28 09:53:41'),(246,'az',' toto, tete, az','2023-12-28 09:53:41'),(247,'az',' toto, tete, az','2023-12-28 09:53:41'),(248,'az','8pVYSY6sOEV2LGYgasbtZqk3mM6PO8Hw tete, az','2023-12-28 09:53:43'),(249,'az','8pVYSY6sOEV2LGYgasbtZqk3mM6PO8Hw tete, az','2023-12-28 09:53:43'),(250,'az','8pVYSY6sOEV2LGYgasbtZqk3mM6PO8Hw toto, tete, az','2023-12-28 09:53:48'),(251,'az','8pVYSY6sOEV2LGYgasbtZqk3mM6PO8Hw toto, tete, az','2023-12-28 09:53:48'),(252,'Serveur','toto a quitté la discussion.','2023-12-28 09:54:04'),(253,'Serveur','toto a quitté la discussion.','2023-12-28 09:54:04'),(254,'Serveur','tete a quitté la discussion.','2023-12-28 09:54:05'),(255,'tete','toto, tete','2023-12-28 09:59:23'),(256,'tete',' toto, tete','2023-12-28 09:59:23'),(257,'tete','toto, tete','2023-12-28 10:01:59'),(258,'tete',' toto, tete','2023-12-28 10:01:59'),(259,'az','hey','2023-12-28 10:02:44'),(260,'az','hey','2023-12-28 10:02:44'),(261,'az','toto, tete, az','2023-12-28 10:02:57'),(262,'az','toto, tete, az','2023-12-28 10:02:57'),(263,'az',' toto, tete, az','2023-12-28 10:02:57'),(264,'az',' toto, tete, az','2023-12-28 10:02:57'),(265,'az','hey','2023-12-28 10:03:09'),(266,'az','je suis dans le canal hehe','2023-12-28 10:03:27'),(267,'Serveur','toto a quitté la discussion.','2023-12-28 10:05:58'),(268,'Serveur','toto a quitté la discussion.','2023-12-28 10:05:58'),(269,'Serveur','tete a quitté la discussion.','2023-12-28 10:05:59');
/*!40000 ALTER TABLE `historique` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilisateurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(50) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom_utilisateur` (`nom_utilisateur`)
) ENGINE=InnoDB AUTO_INCREMENT=15054 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilisateurs`
--

LOCK TABLES `utilisateurs` WRITE;
/*!40000 ALTER TABLE `utilisateurs` DISABLE KEYS */;
INSERT INTO `utilisateurs` VALUES (1,'john_doe','64751b0b2552c1f4654e975cbf56317a11fd74847222fb044cbc3217f68670c4'),(4,'toto','31f7a65e315586ac198bd798b6629ce4903d0899476d5741a9f32e2e521b6a66'),(5,'zack','toto'),(6,'titi','titi'),(9,'tata','d1c7c99c6e2e7b311f51dd9d19161a5832625fb21f35131fba6da62513f0c099'),(10,'tete','043d6c5097ea53ca880fbbfdb22451e80b07dda8901591a6574c99907a2e278e'),(11,'cherine','cce66316b4c1c59df94a35afb80cecd82d1a8d91b554022557e115f5c275f515'),(13,'ddd','730f75dafd73e047b86acb2dbd74e75dcb93272fa084a9082848f2341aa1abb6'),(14,'zacharie','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'),(15,'1234','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'),(16,'cherinu','28357a406414e2aedb7da37271a85b11e53acfb11a04a16504223756f7633301'),(17,'ykari','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'),(18,'azerty','f2d81a260dea8a100dd517984e53c56a7523d96942a834b9cdc249bd4e8c7aa9'),(19,'te','2d6c9a90dd38f6852515274cde41a8cd8e7e1a7a053835334ec7e29f61b918dd'),(22,'tg','e9ed69a6ea08507ea7f2d93985c23588cc4c5bd46b0f9997f1193238542ca395'),(15042,'as','f4bf9f7fcbedaba0392f108c59d8f4a38b3838efb64877380171b54475c2ade8'),(15047,'yh','dfa3bde638cb08d781f46d978f471fe535a642cb24d408bcc486a67c819cc4e4'),(15049,'123','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),(15051,'toto123','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),(15052,'kloetito','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'),(15053,'az','9c0ada37bf74aeefae949fdfc90db0cf6eaf90192eff67d65887771f0585e055');
/*!40000 ALTER TABLE `utilisateurs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-28 15:25:18
