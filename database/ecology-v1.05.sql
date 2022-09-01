-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: ecoplace
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `businesses`
--

DROP TABLE IF EXISTS `businesses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `businesses` (
  `business_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `contact` varchar(45) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `background_image` varchar(45) DEFAULT NULL,
  `main_category` varchar(45) DEFAULT NULL,
  `rating` int DEFAULT '0',
  `logo_image` varchar(45) DEFAULT NULL,
  `categories` varchar(200) DEFAULT NULL,
  `benefit` varchar(500) DEFAULT NULL,
  `url` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`business_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `businesses`
--

LOCK TABLES `businesses` WRITE;
/*!40000 ALTER TABLE `businesses` DISABLE KEYS */;
INSERT INTO `businesses` VALUES (1,'TheNut','contact@thenut.sg','We sell high quality nuts. Risus nullam eget felis eget nunc lobortis mattis. Nisi scelerisque eu ultrices vitae auctor eu augue ut. At varius vel pharetra vel turpis nunc. Nulla posuere sollicitudin aliquam ultrices sagittis. At erat pellentesque adipiscing commodo elit at imperdiet. Dolor sed viverra ipsum nunc aliquet bibendum. Nullam eget felis eget nunc lobortis mattis aliquam faucibus. Turpis nunc eget lorem dolor sed. Lacus viverra vitae congue eu. Sed faucibus turpis in eu mi bibendum.','thenut.jpg','Food & Beverage',4,'thenut_logo.png','Food & Beverage, Health Foods','Risus nullam eget felis eget nunc lobortis mattis. Nisi scelerisque eu ultrices vitae auctor eu augue ut. At varius vel pharetra vel turpis nunc. Nulla posuere sollicitudin aliquam ultrices sagittis. At erat pellentesque adipiscing commodo elit at imperdiet. Dolor sed viverra ipsum nunc aliquet bibendum. Nullam eget felis eget nunc lobortis mattis aliquam faucibus. Turpis nunc eget lorem dolor sed. Lacus viverra vitae congue eu. Sed faucibus turpis in eu mi bibendum.','https://www.thenut.sg'),(2,'SUPERBEE','contact@superbee.com','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. In pellentesque massa placerat duis. Feugiat scelerisque varius morbi enim nunc faucibus a pellentesque sit. Vitae turpis massa sed elementum. Habitasse platea dictumst vestibulum rhoncus est pellentesque elit.','superbee-product.png','Food & Beverage',5,'superbee-logo.png','Oral Care, Wraps','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nisl vel pretium lectus quam id leo in vitae turpis. Euismod elementum nisi quis eleifend quam adipiscing vitae. Vel orci porta non pulvinar neque laoreet. Fringilla phasellus faucibus scelerisque eleifend donec pretium.','https://superbee.me/'),(3,'THE BODY SHOP','loveyourbodyap@thebodyshop.com','Our story started in 1976. It began with our founder, Anita Roddick, opening a little green shop in Brighton with a belief in something revolutionary: that business could be a force for good. We’ve never been your average cosmetics company, with over 40 years of campaigning, change-making and smashing beauty industry standards – and we’re still going strong. Welcome to The Body Shop.','BodyShop.png','Self-care',3,'Bodyshop_Icon.png','Self-care, Skincare, Bodycare','With the incentify system of EcoGim, first time members will receive an exclusive 10% discount voucher ( in a single receipt ) of THE BODY SHOP products and/or services.  While you purchase the items, you’ll gain points based on how much of plastic and/or other items you have helped to save and you’re able to check out your progress with our latest EcoGim App  * Coming soon*','https://www.thebodyshop.com/en-sg/'),(4,'Brown Living','hello@brownliving.in','We are a team of earth advocates, aiming to promote a sustainable way of living. We want to inspire people to transform from mindless consumption into conscious decisions.  We curate and create thoughtful, sustainable and elegant everyday products. We refuse to take shortcuts, and we obsess over every single step in the journey of our products – from how they are made to how they end up on your doorstep','brown-living-background.png','General',5,'brown-living-logo.png','Self-care, Fashion, Home, Food & Beverage, Travel, Gifts','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. A pellentesque sit amet porttitor eget dolor morbi non. Vitae semper quis lectus nulla. Aliquet eget sit amet tellus cras adipiscing enim. Nec ultrices dui sapien eget mi proin sed libero enim.','https://brownliving.in/');
/*!40000 ALTER TABLE `businesses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carts` (
  `uid` int NOT NULL,
  `product` varchar(45) DEFAULT NULL,
  `product_count` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `stock` varchar(45) DEFAULT NULL,
  `business_id` varchar(45) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `image` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Macadamia Nuts','Macadamia nuts from the freshest source in the world','250','1',NULL,NULL),(2,'Almond Nuts','Almond Nuts from the second freshest source in the world','2523','1',NULL,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `role` varchar(45) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `session` varchar(45) DEFAULT NULL,
  `profile_image` varchar(50) DEFAULT NULL,
  `points` int DEFAULT '0',
  `trees_planted` int DEFAULT '0',
  `plastic_saved` int DEFAULT '0',
  `reused_packaging` int DEFAULT '0',
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'gabrielseet','gabeseet@gmail.com','admin','161ebd7d45089b3446ee4e0d86dbcf92','7f088254187fe10973348aa7b0e1d0c0',NULL,0,0,0,0),(2,'cody','codydywork@gmail.com','admin','161ebd7d45089b3446ee4e0d86dbcf92',NULL,NULL,0,0,0,0),(3,'aarav','aarav53vij@gmail.com','admin','161ebd7d45089b3446ee4e0d86dbcf92',NULL,NULL,0,0,0,0),(5,'johnlow','johnlow@gmail.com',NULL,'161ebd7d45089b3446ee4e0d86dbcf92',NULL,NULL,0,0,0,0),(6,'johncena1','johncena1@gmail.com',NULL,'161ebd7d45089b3446ee4e0d86dbcf92',NULL,NULL,0,0,0,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-01 21:41:43
