CREATE DATABASE  IF NOT EXISTS `llmeet` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `llmeet`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 120.76.53.217    Database: llmeet
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `meeting`
--

DROP TABLE IF EXISTS `meeting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meeting` (
  `meeting_id` varchar(19) NOT NULL COMMENT '19位带横线随机生成ID（示例：0041-gsxw-zx2f-vlpb）',
  `title` varchar(255) NOT NULL COMMENT '会议标题',
  `description` text COMMENT '会议描述',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `creator_id` varchar(50) NOT NULL COMMENT '创建者ID（关联user表）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `status` varchar(20) NOT NULL DEFAULT 'planned' COMMENT '状态：planned/ongoing/completed',
  PRIMARY KEY (`meeting_id`),
  KEY `meeting_ibfk_1_idx` (`creator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会议主表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meeting`
--

LOCK TABLES `meeting` WRITE;
/*!40000 ALTER TABLE `meeting` DISABLE KEYS */;
INSERT INTO `meeting` VALUES ('101146660','AI meeting','AI','2025-07-11 19:17:24','2025-07-11 19:47:24','qixiaojian','2025-07-11 19:17:29','ready'),('153938217','123','123','2025-07-11 07:36:24','2025-07-11 08:06:24','qixiaojian','2025-07-11 15:37:01','ready');
/*!40000 ALTER TABLE `meeting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `minutes`
--

DROP TABLE IF EXISTS `minutes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `minutes` (
  `minutes_id` int NOT NULL AUTO_INCREMENT COMMENT '纪要自增ID',
  `meeting_id` varchar(19) NOT NULL COMMENT '关联的会议UUID',
  `segments` json DEFAULT NULL COMMENT '纪要内容',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `language` varchar(5) DEFAULT 'en',
  PRIMARY KEY (`minutes_id`),
  UNIQUE KEY `meeting_id_UNIQUE` (`meeting_id`),
  KEY `idx_meeting_id` (`meeting_id`),
  CONSTRAINT `minutes_ibfk_1` FOREIGN KEY (`meeting_id`) REFERENCES `meeting` (`meeting_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会议纪要表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `minutes`
--

LOCK TABLES `minutes` WRITE;
/*!40000 ALTER TABLE `minutes` DISABLE KEYS */;
INSERT INTO `minutes` VALUES (2,'101146660','[{\"end\": 3.44, \"text\": \"卷基神經網絡是一種乾坤神經網絡\", \"start\": 0.0, \"speaker\": \"SPK00\"}, {\"end\": 6.640000000000001, \"text\": \"它的神經圓和人工神經圓可以相應於\", \"start\": 3.44, \"speaker\": \"SPK00\"}, {\"end\": 11.68, \"text\": \"一部分內的周圍單元,對於大型圖像處理有出色表現\", \"start\": 6.640000000000001, \"speaker\": \"SPK00\"}, {\"end\": 15.8, \"text\": \"卷基神經網絡由一個或多的卷基層和頂端的全聯通層\", \"start\": 11.68, \"speaker\": \"SPK00\"}, {\"end\": 20.2, \"text\": \"利用經典的神經網絡組成,同時也包括關聯權重和遲化層\", \"start\": 15.8, \"speaker\": \"SPK00\"}, {\"end\": 24.8, \"text\": \"這一結構使得卷基神經網絡能夠利用輸入數據的二維結構\", \"start\": 20.2, \"speaker\": \"SPK00\"}, {\"end\": 28.2, \"text\": \"與其他深度學習結構相比,卷基神經網絡\", \"start\": 24.8, \"speaker\": \"SPK00\"}, {\"end\": 31.2, \"text\": \"在圖像和語音識別方面能夠給出更好的結果\", \"start\": 28.2, \"speaker\": \"SPK00\"}, {\"end\": 34.6, \"text\": \"這一模型也可以使用反向傳播算法進行訓練\", \"start\": 31.2, \"speaker\": \"SPK00\"}, {\"end\": 37.0, \"text\": \"相比較其他深度潛會神經網絡\", \"start\": 34.6, \"speaker\": \"SPK00\"}, {\"end\": 39.4, \"text\": \"卷基神經網絡需要考量的參數更少\", \"start\": 37.0, \"speaker\": \"SPK00\"}, {\"end\": 41.8, \"text\": \"使之成為一種頗具吸引力的深度學習結構\", \"start\": 39.4, \"speaker\": \"SPK00\"}, {\"end\": 45.8, \"text\": \"卷基神經網絡的靈感,來源於動物視覺皮層組織的神經連接方式\", \"start\": 41.8, \"speaker\": \"SPK00\"}, {\"end\": 48.6, \"text\": \"單個神經圓,只對有限區域內的四肌作出反應\", \"start\": 45.8, \"speaker\": \"SPK00\"}, {\"end\": 51.8, \"text\": \"不同神經圓的感知區域相互重疊,總而覆蓋整個視野\", \"start\": 48.6, \"speaker\": \"SPK00\"}]','2025-07-12 04:25:13','zh');
/*!40000 ALTER TABLE `minutes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `user_meeting_id` int DEFAULT NULL,
  `minutes_path` text,
  PRIMARY KEY (`record_id`),
  KEY `record_ibfk_1_idx` (`user_meeting_id`),
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`user_meeting_id`) REFERENCES `user_meeting` (`user_meeting_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
INSERT INTO `records` VALUES (9,11,'recordings/101146660/final_qixiaojian_20250711_202259.mp4');
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(50) NOT NULL,
  `user_id` int DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb3 NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `timezone` varchar(64) DEFAULT 'UTC',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('qixiaojian',NULL,'qixiaojian00310@163.com','$2b$12$dheolxYnWvZavJ0S6YshW.E54zgSOvtgpEkCKkZo8nu.Eyqs4K2AG','2025-07-09 08:32:42','Asia/Shanghai');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_meeting`
--

DROP TABLE IF EXISTS `user_meeting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_meeting` (
  `user_meeting_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户ID',
  `meeting_id` varchar(19) NOT NULL COMMENT '会议UUID',
  `joined_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  PRIMARY KEY (`user_meeting_id`),
  UNIQUE KEY `unique_user_meeting` (`username`,`meeting_id`),
  KEY `idx_meeting_id` (`meeting_id`),
  KEY `user_meeting_ibfk_1_idx` (`username`),
  CONSTRAINT `user_meeting_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`),
  CONSTRAINT `user_meeting_ibfk_2` FOREIGN KEY (`meeting_id`) REFERENCES `meeting` (`meeting_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户会议关系表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_meeting`
--

LOCK TABLES `user_meeting` WRITE;
/*!40000 ALTER TABLE `user_meeting` DISABLE KEYS */;
INSERT INTO `user_meeting` VALUES (4,'qixiaojian','153938217','2025-07-11 15:37:01'),(11,'qixiaojian','101146660','2025-07-11 19:17:29');
/*!40000 ALTER TABLE `user_meeting` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-12  4:34:26
