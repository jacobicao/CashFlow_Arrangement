-- MySQL dump 10.13  Distrib 5.7.20, for osx10.9 (x86_64)
--
-- Host: localhost    Database: credit_card_system
-- ------------------------------------------------------
-- Server version	5.6.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `card`
--

DROP TABLE IF EXISTS `card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `card` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `name` char(30) DEFAULT NULL,
  `A_day` int(11) DEFAULT NULL,
  `P_day` int(11) DEFAULT NULL,
  `num` float DEFAULT NULL,
  PRIMARY KEY (`cid`),
  KEY `uid` (`uid`),
  CONSTRAINT `card_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card`
--

LOCK TABLES `card` WRITE;
/*!40000 ALTER TABLE `card` DISABLE KEYS */;
INSERT INTO `card` VALUES (37,1,'BOC_J',3,23,20000),(38,1,'PINGAN_J',5,23,28000),(39,1,'ABC_J',7,1,50000),(40,1,'ZS_Q',14,2,22000),(41,1,'ZX_J',16,4,50000),(42,1,'ICBC_J',17,6,30000),(43,1,'PINGAN_Q',17,4,38000),(44,1,'XINGYE_J',18,7,18000),(45,1,'SPD_J',22,11,11000),(46,1,'JIANSHE_Q',24,10,45000),(47,1,'BOC_Q',27,16,30000),(48,1,'HOME',25,28,2700000);
/*!40000 ALTER TABLE `card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `debt`
--

DROP TABLE IF EXISTS `debt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `debt` (
  `uid` int(11) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `num` float DEFAULT NULL,
  `P_time` date DEFAULT NULL,
  PRIMARY KEY (`did`),
  KEY `uid` (`uid`),
  KEY `cid` (`cid`),
  CONSTRAINT `debt_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`),
  CONSTRAINT `debt_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `card` (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `debt`
--

LOCK TABLES `debt` WRITE;
/*!40000 ALTER TABLE `debt` DISABLE KEYS */;
INSERT INTO `debt` VALUES (1,47,1,24000,'2018-03-02'),(1,37,2,8900,'2018-03-04'),(1,37,3,5300,'2018-04-05'),(1,39,4,40000,'2018-04-08'),(1,38,5,25000,'2018-04-08'),(1,48,6,13300,'2018-04-20'),(1,48,7,13300,'2018-05-20'),(1,48,8,13300,'2018-06-20'),(1,48,9,13300,'2018-07-20'),(1,48,10,13300,'2018-08-20'),(1,48,11,13300,'2018-09-20'),(1,48,12,13300,'2018-10-20'),(1,48,13,13300,'2018-11-20'),(1,48,14,13300,'2018-12-20');
/*!40000 ALTER TABLE `debt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `income`
--

DROP TABLE IF EXISTS `income`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `income` (
  `uid` int(11) DEFAULT NULL,
  `iid` int(11) NOT NULL AUTO_INCREMENT,
  `num` float DEFAULT NULL,
  `P_time` date DEFAULT NULL,
  PRIMARY KEY (`iid`),
  KEY `uid` (`uid`),
  CONSTRAINT `income_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `income`
--

LOCK TABLES `income` WRITE;
/*!40000 ALTER TABLE `income` DISABLE KEYS */;
INSERT INTO `income` VALUES (1,1,4200,'2018-04-15'),(1,2,25000,'2018-05-15'),(1,3,25000,'2018-06-15'),(1,4,25000,'2018-07-15'),(1,5,25000,'2018-08-15'),(1,6,25000,'2018-09-15'),(1,7,25000,'2018-10-15'),(1,8,25000,'2018-11-15'),(1,9,25000,'2018-12-15');
/*!40000 ALTER TABLE `income` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(30) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Vicky');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-19 23:55:50
