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
  `video_summarization` text,
  PRIMARY KEY (`minutes_id`),
  UNIQUE KEY `meeting_id_UNIQUE` (`meeting_id`),
  KEY `idx_meeting_id` (`meeting_id`),
  CONSTRAINT `minutes_ibfk_1` FOREIGN KEY (`meeting_id`) REFERENCES `meeting` (`meeting_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会议纪要表';
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户会议关系表';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-18 11:17:51
