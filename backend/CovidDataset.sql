-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: 127.0.0.1    Database: covid
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `final`
--

DROP TABLE IF EXISTS `final`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `final` (
  `id` int DEFAULT NULL,
  `Sector` text,
  `NumEmployees` double DEFAULT NULL,
  `NumBusinesses` int DEFAULT NULL,
  `RestrictionsIntensity` double DEFAULT NULL,
  `April_20` double DEFAULT NULL,
  `May_20` double DEFAULT NULL,
  `June_20` double DEFAULT NULL,
  `July_20` double DEFAULT NULL,
  `August_20` double DEFAULT NULL,
  `September_20` double DEFAULT NULL,
  `October_20` double DEFAULT NULL,
  `November_20` double DEFAULT NULL,
  `December_20` double DEFAULT NULL,
  `January_21` double DEFAULT NULL,
  `February_21` double DEFAULT NULL,
  `March_21` double DEFAULT NULL,
  `April_21` double DEFAULT NULL,
  `May_21` double DEFAULT NULL,
  `April_20_bus` double DEFAULT NULL,
  `May_20_bus` double DEFAULT NULL,
  `June_20_bus` double DEFAULT NULL,
  `July_20_bus` double DEFAULT NULL,
  `August_20_bus` double DEFAULT NULL,
  `September_20_bus` double DEFAULT NULL,
  `October_20_bus` double DEFAULT NULL,
  `November_20_bus` double DEFAULT NULL,
  `December_20_bus` double DEFAULT NULL,
  `January_21_bus` double DEFAULT NULL,
  `February_21_bus` double DEFAULT NULL,
  `March_21_bus` double DEFAULT NULL,
  `April_21_bus` double DEFAULT NULL,
  `May_21_bus` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `final`
--

LOCK TABLES `final` WRITE;
/*!40000 ALTER TABLE `final` DISABLE KEYS */;
INSERT INTO `final` VALUES (1,'Agriculture ',900,900,1,-3.7,-0.03,0.2,-0.83,-0.5,-0.1,-0.4,3.5,-2.3,-2.5,-2.6,0.4,-1.07,-1.2,0.25,0.125,0,0.125,0.125,0.125,0.125,0,0.2,0.2,0.2,0,0.2,0.2),(2,'Natural resources',900,900,1,-10.1,2.6,-1.06,5.2,-0.3,0.5,2.9,2.8,0.2,0.9,-1.09,0.4,1.5,2.1,0.25,0,0.2,0,0.125,0,0,0,0,0,0.2,0,0,0),(3,'Utilities',500,500,1,0.5,-0.5,0.6,-2.4,3.5,4.7,-0.5,-3.01,0.8,0.5,1.5,0.4,-0.9,-1.2,0,0.125,0,0.2,0,0,0.125,0.25,0,0,0,0,0.125,0.2),(4,'Construction',500,1,1,-25.6,4.9,7.5,1.75,0.1,0.2,0.7,1.6,0.2,1.8,0.5,0.1,-1.1,-0.8,0.25,0,0,0,0,0.2,0,0,0,0,0,0,0.2,0.125),(5,'Manufacturing',1755.5,46586,1,-18.3,6.08,5.2,1.7,1.6,4.1,-0.5,-0.03,0.7,-0.6,0.4,0.01,-0.1,-1.7,0.25,0,0,0,0,0,0.125,0.125,0,0.125,0,0,0.125,0.2),(6,'Wholesale and retail trade',2755.1,113838,0,-17,109.5,8.4,3.9,0.6,-0.3,1.7,0.5,0.1,-6.1,4.6,0.1,-3.3,-0.5,0.25,0,0,0,0,0.125,0,0,0,0.25,0,0,0.25,0.125),(7,'Transportation and warehousing',968.4,48703,1,-11.7,-0.04,5.6,0.9,0.8,1.7,-0.5,1.2,1.2,0.1,0.8,-0.04,-0.4,2,0.25,0.125,0,0,0,0,0.125,0,0,0,0,0.125,0.125,0),(8,'Finance, insurance, real estate, rental and leasing',1293.8,60732,1,-2.7,2.1,1,-0.6,-0.25,1.6,1.1,0.8,0.4,0.1,-0.3,0.03,0.8,-0.1,0.2,0,0,0.125,0.125,0,0,0,0,0,0.125,0,0,0.125),(9,'Professional, scientific and technical services',1644.6,110870,1,-5.3,-0.6,-0.15,2.4,1.06,1.4,2.4,0.6,1.5,0.4,0.8,0.02,0.9,0.7,0.25,0.125,0.125,0,0,0,0,0,0,0,0,0,0,0),(10,'Business, building and other support services',699,35821,1,-66.7,-3.8,8.7,-2.8,2.3,-0.09,1.4,0.5,-1.2,-0.5,0,0.1,-0.9,0.08,0.25,0.25,0,0.2,0,0.125,0,0,0.2,0.125,0,0,0.125,0),(11,'Educational services',500,8798,1,-10,1.7,1.35,1.5,2.4,5.8,0.7,0.3,0.3,-0.4,1.6,0.2,-2.9,0.04,0.25,0,0,0,0,0,0,0,0,0.125,0,0,0.2,0),(12,'Health care and social assistance',5222,96441,0,-5.7,0.03,4.9,0.9,0.3,0.9,0.8,0.08,0.3,0.7,0.3,0.05,-0.09,-0.3,0.25,0,0,0,0,0,0,0,0,0,0,0,0.125,0.125),(13,'Information, culture and recreation',691.8,22440,0.9975,-12.4,-0.7,8.6,3.2,0,7.3,-1.9,-2.8,-2.1,-1.9,-0.5,1.2,-2.5,0.4,0.25,0.125,0,0,0,0,0.2,0.2,0.2,0.2,0.125,0,0.2,0),(14,'Accommodation and food services',864.5,55537,1,-52,8.02,19.6,11.09,4.6,6.14,-4.3,-3,-5.8,-8.8,7.5,0.2,-6.9,-0.6,0.25,0,0,0,0,0,0.25,0.25,0.25,0.25,0,0,0.25,0.125),(15,'Other services (except public administration)',746.5,65064,0,-22.1,1.3,6.5,6.4,4.4,1.8,-0.2,-0.4,-3.6,-1.3,3.6,-0.07,-0.1,-3.9,0.25,0,0,0,0,0,0.125,0.125,0.25,0.2,0,0.125,0.125,0.25),(16,'Public administration',200,7779,1,-1.8,0.04,0.5,0.5,-0.2,1.7,0.5,0.4,1.3,0.8,-0.1,-0.06,2.4,0.4,0.2,0,0,0,0.125,0,0,0,0,0,0.125,0.125,0,0);
/*!40000 ALTER TABLE `final` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gdp`
--

DROP TABLE IF EXISTS `gdp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gdp` (
  `id` int DEFAULT NULL,
  `Sector` text,
  `RestrictionsIntensity` int DEFAULT NULL,
  `March_20` double DEFAULT NULL,
  `April_20` double DEFAULT NULL,
  `May_20` double DEFAULT NULL,
  `June_20` double DEFAULT NULL,
  `July_20` double DEFAULT NULL,
  `August_20` double DEFAULT NULL,
  `September_20` double DEFAULT NULL,
  `October_20` double DEFAULT NULL,
  `November_20` double DEFAULT NULL,
  `December_20` double DEFAULT NULL,
  `January_21` double DEFAULT NULL,
  `February_21` double DEFAULT NULL,
  `March_21` double DEFAULT NULL,
  `April_21` double DEFAULT NULL,
  `May_21` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gdp`
--

LOCK TABLES `gdp` WRITE;
/*!40000 ALTER TABLE `gdp` DISABLE KEYS */;
INSERT INTO `gdp` VALUES (1,'Agriculture',1,-0.3,-1.1,2.2,1.5,0.5,0.5,0.2,0.2,-0.5,-0.7,-1.2,-1,-1.3,-0.5,-0.9),(2,'Natural resources',1,-4.5,-10.1,0.8,-4.4,1,-2,4,0.8,3.8,4.5,1.6,-1.5,0.2,-1.4,-0.1),(3,'Utilities',1,-1,-1.6,0,1,1.9,-2.7,-1.7,1.3,-0.6,0.1,-0.7,0.9,-0.7,-1.7,2.1),(4,'Construction',1,-3.1,-18.5,13.2,7.3,-1.2,0.8,0.1,1,-0.3,1.4,1.2,1.4,1.9,2.2,-3.3),(5,'Manufacturing',1,-8.9,-20.4,10.5,11.7,4.3,1.7,0.6,0.1,2,-0.8,1.2,-1.7,1.1,-2,-0.4),(6,'Wholesale and retail trade',0,-18.3,-37.2,25.3,33.8,4.5,0.4,2.6,1.5,1.2,-3.7,-1,5.3,5.5,-7.3,-4.4),(7,'Transportation and warehousing',1,-13.3,-21,1.3,9.3,3.4,0,1.7,2.3,1.4,1.5,-0.1,-2.1,0.9,-1.1,-1),(8,'Finance, insurance, real estate, rental and leasing',0,-7.2,-2.4,0.3,2.5,2,2.2,0.9,2.1,1.6,0.3,0.2,0.5,-0.1,-1.2,0.1),(9,'Professional, scientific and technical services',1,-1.5,-3.2,1.4,2.7,2.1,0.5,0.5,-0.4,-0.1,0.9,0.3,0.2,0.1,0.1,-0.2),(10,'Business, building and other support services',1,-15.5,-4.3,-1.7,-0.1,-2,-2.4,-2.2,-0.3,-2.6,-2.4,-1.2,-0.4,-2.4,-3.2,-2.5),(11,'Educational services',1,-15.7,-14.7,2.7,10.6,1.8,4.1,2.1,1.3,1.1,1,0.5,-1.6,-0.8,0,-1.1),(12,'Health care and social assistance',1,-8.8,-9.3,7,2,4.3,2.4,0.7,0.2,0.2,0.5,0.4,0.4,1.5,-4.1,2.6),(13,'Information, culture and recreation',1,-13.4,-15.1,2.6,10,6.4,3.1,1.4,1.7,0.9,0.7,0.8,0.8,0.7,0.5,0.6),(14,'Accommodation and food services',1,-37,-44.6,18.7,27.9,17.5,8.7,-0.2,-7.5,0.5,-9.8,1.5,5.9,12.8,-10.4,-4.5),(15,'Other services (except public administration)',1,-13.6,-27.2,10.6,8.8,8.5,3.9,1.8,1,0.8,0.1,0.1,0.4,-0.2,0.7,-0.2),(16,'Public administration',1,-5.2,-2.5,0.4,1.9,1.9,0.7,1.1,0.9,0.1,0.6,0.2,0.3,1,0.2,-0.1);
/*!40000 ALTER TABLE `gdp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sample_covid_data`
--

DROP TABLE IF EXISTS `sample_covid_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sample_covid_data` (
  `id` int DEFAULT NULL,
  `Subsection` text,
  `BusinessType` text,
  `Quantity` int DEFAULT NULL,
  `AvgPop` int DEFAULT NULL,
  `OpCapacity` double DEFAULT NULL,
  `RelRisk` double DEFAULT NULL,
  `RelChange` double DEFAULT NULL,
  `SubsectionCount` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sample_covid_data`
--

LOCK TABLES `sample_covid_data` WRITE;
/*!40000 ALTER TABLE `sample_covid_data` DISABLE KEYS */;
INSERT INTO `sample_covid_data` VALUES (1,'Sports and Rec','Skating Rinks',54,50,0,0.2,0.01,16),(2,'Sports and Rec','Sports Complex',40,20,0,0.9,0.01,16),(3,'Sports and Rec','Gyms',250,200,0,0.8,0.01,16),(4,'Sports and Rec','Fitness Studios',220,200,0,0.8,0.01,16),(5,'Sports and Rec','Adventure Activities',40,150,0,0.4,0.01,16),(6,'Sports and Rec','Playgrounds',47,100,0,0.6,0.01,16),(7,'Sports and Rec','Swimming Pools',40,150,0,0.7,0.01,16),(8,'Sports and Rec','Golf',60,50,0,0.3,0.01,16),(9,'Sports and Rec','Baseball Diamonds',11,50,0,0.2,0.01,16),(10,'Sports and Rec','Soccer Fields/Clubs',26,60,0,0.6,0.01,16),(11,'Sports and Rec','Basketball Courts',50,80,0,0.7,0.01,16),(12,'Sports and Rec','Skate Parks',6,50,0,0.3,0.01,16),(13,'Sports and Rec','Motorsport Tracks',10,30,0,0.2,0.01,16),(14,'Sports and Rec','Marinas/Boat Clubs',70,5,0,0.2,0.01,16),(15,'Sports and Rec','Shooting Ranges',13,20,0,0.3,0.01,16),(16,'Sports and Rec','Tennis Courts',60,10,0,0.1,0.01,16),(17,'School','Elementary',475,400,0,0.7,0.08,5),(18,'School','Secondary',110,700,0,0.7,0.08,5),(19,'School','Camps for Children',24,50,0,0.7,0.08,5),(20,'School','Child Care Centers',1000,20,0,0.7,0.08,5),(21,'School','Tutoring',215,25,0,0.7,0.08,5),(22,'Social Gathering','House Party',15,30,0,0.8,0.31,7),(23,'Social Gathering','Play dates',30,10,0,0.5,0.31,7),(24,'Social Gathering','Guests visit',30,10,0,0.5,0.31,7),(25,'Social Gathering','Weddings/Receptions',250,150,0,0.7,0.31,7),(26,'Social Gathering','Funerals',52,25,0,0.7,0.31,7),(27,'Social Gathering','Outdoor Parties',20,30,0,0.65,0.31,7),(28,'Social Gathering','Convention Centers/Event spaces',50,25,0,0.8,0.31,7),(29,'Religious Gathering','Places of Worship',700,10,0,0.8,0.21,1),(30,'Shopping','Grocery and Big Box Stores',200,500,0,0.6,0.36,4),(31,'Shopping','Indoor Shopping Malls/Centers',50,500,0,0.5,0.36,4),(32,'Shopping','Outlet Malls',3,500,0,0.4,0.36,4),(33,'Shopping','Outdoor Plazas ',30,500,0,0.4,0.36,4),(34,'Restaurants','Takeout',450,30,0,0.1,0.43,6),(35,'Restaurants','Bars/Pubs',350,50,0,0.9,0.43,6),(36,'Restaurants','Buffet-Style Food Services',90,50,0,0.9,0.43,6),(37,'Restaurants','Dine-In Restaurants',400,50,0,0.75,0.43,6),(38,'Restaurants','Cafes',300,100,0,0.75,0.43,6),(39,'Restaurants','Patio Restaurants',200,50,0,0.4,0.43,6),(40,'Entertainment','Amusement Parks',5,250,0,0.8,0.23,15),(41,'Entertainment','Tours and Guide Services',38,20,0,0.4,0.23,15),(42,'Entertainment','Water Parks',7,150,0,0.65,0.23,15),(43,'Entertainment','Movie Theatres',49,200,0,0.7,0.23,15),(44,'Entertainment','Fairs/Festivals',2,20,0,0.8,0.23,15),(45,'Entertainment','Concerts/Live Shows',35,10,0,0.9,0.23,15),(46,'Entertainment','Gaming Establishments / Arcades',60,30,0,0.7,0.23,15),(47,'Entertainment','Escape Rooms',30,40,0,0.7,0.23,15),(48,'Entertainment','Casinos',4,150,0,0.6,0.23,15),(49,'Entertainment','Bingo halls',10,20,0,0.7,0.23,15),(50,'Entertainment','Clubs',60,100,0,1,0.23,15),(51,'Entertainment','Film/TV Production',9,35,0,0.4,0.23,15),(52,'Entertainment','Drive-In/Drive-Thru venues',7,100,0,0.2,0.23,15),(53,'Entertainment','Karaoke Bars',30,30,0,0.9,0.23,15),(54,'University/College','Campus',19,5000,0,0.4,0.08,2),(55,'University/College','Residences',21,500,0,0.6,0.08,2),(56,'Health Care','Counselling Services',240,10,0,0.4,0.1,5),(57,'Health Care','Walk-in clinics',120,60,0,0.4,0.1,5),(58,'Health Care','Pharmacy',350,50,0,0.4,0.1,5),(59,'Health Care','Hospitals',35,300,0,0.4,0.1,5),(60,'Health Care','Specialized doctors',1000,5,0,0.4,0.1,5),(61,'Self Care','Saunas/Steam Rooms',20,10,0,0.8,0.1,11),(62,'Self Care','Beauty Salons',230,30,0,0.6,0.1,11),(63,'Self Care','Hair Salons',330,30,0,0.6,0.1,11),(64,'Self Care','Nail Salons',300,30,0,0.6,0.1,11),(65,'Self Care','Non-Medical Diet Centers',35,10,0,0.4,0.1,11),(66,'Self Care','Piercing Services',60,10,0,0.4,0.1,11),(67,'Self Care','Tattoo Services',150,10,0,0.4,0.1,11),(68,'Self Care','Tanning Salons',70,10,0,0.5,0.1,11),(69,'Self Care','Oxygen Bars',6,5,0,0.2,0.1,11),(70,'Self Care','Floating Pools',10,5,0,0.2,0.1,11),(71,'Self Care','Sensory Deprevation Centers',4,5,0,0.2,0.1,11),(72,'Economic','Real-Estate Open Houses',450,1,0,0.3,0.1,5),(73,'Economic','Brokerages',150,10,0,0.4,0.1,5),(74,'Economic','Vehicle Dealerships',200,5,0,0.5,0.1,5),(75,'Economic','Banks',286,25,0,0.4,0.1,5),(76,'Economic','Government services',15,30,0,0.4,0.1,5),(77,'Personal Services','House-sitting/Pet-sitting',35,1,0,0.1,0.1,8),(78,'Personal Services','Event planning services',300,3,0,0.4,0.1,8),(79,'Personal Services','Personal Fitness Trainer',250,5,0,0.8,0.1,8),(80,'Personal Services','Shoe Services',150,10,0,0.3,0.1,8),(81,'Personal Services','Security Services',230,5,0,0.8,0.1,8),(82,'Personal Services','Check Room Services',5,5,0,0.8,0.1,8),(83,'Personal Services','Photography Services',450,5,0,0.4,0.1,8),(84,'Personal Services','Domestic/Housekeeping Services',250,5,0,0.5,0.1,8),(85,'Nature','National/Provincial/Municipal Parks',15,50,0,0.2,0.1,5),(86,'Nature','Camp Grounds',5,20,0,0.3,0.1,5),(87,'Nature','Beaches',10,70,0,0.5,0.1,5),(88,'Nature','Ponds, Lakes',12,30,0,0.1,0.1,5),(89,'Nature','Hiking Trails',7,50,0,0.25,0.1,5),(90,'Community Services','Libraries',102,20,0,0.3,0.1,4),(91,'Community Services','Retirement Homes',37,250,0,1,0.1,4),(92,'Community Services','Community Centers',166,50,0,0.7,0.1,4),(93,'Community Services','Construction',300,15,0,0.2,0.1,4),(94,'Attractions and Heritage','Museums/Galleries',67,10,0,0.35,0.1,7),(95,'Attractions and Heritage','Aquariums',1,50,0,0.35,0.1,7),(96,'Attractions and Heritage','Hotels',140,200,0,0.4,0.1,7),(97,'Attractions and Heritage','Zoos',3,60,0,0.2,0.1,7),(98,'Attractions and Heritage','Historical Sites',56,25,0,0.35,0.1,7),(99,'Attractions and Heritage','Gardens',13,50,0,0.2,0.1,7),(100,'Attractions and Heritage','Famous landmarks',190,25,0,0.35,0.1,7),(101,'Animal Services','Veterinary Services',27,20,0,0.4,0.1,3),(102,'Animal Services','Pet Grooming Services',239,10,0,0.4,0.1,3),(103,'Animal Services','Pet Training Services',31,10,0,0.4,0.1,3);
/*!40000 ALTER TABLE `sample_covid_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-22 23:34:11
