-- Local Service Finder Database Backup
-- Generated on: 2025-11-06 22:30:23
-- Database: lsf_db

CREATE DATABASE IF NOT EXISTS `lsf_db`;
USE `lsf_db`;


-- Table structure for `contact_messages`
DROP TABLE IF EXISTS `contact_messages`;
CREATE TABLE `contact_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `subject` varchar(200) DEFAULT NULL,
  `message` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `contact_messages`
INSERT INTO `contact_messages` (`id`, `name`, `email`, `subject`, `message`, `created_at`) VALUES
(1, 'Shambhu Sharma', 'shambhu@gmail.com', 'Testing', 'Testing the funcanality of contact us page', '2025-11-03 08:47:31'),
(2, 'Abhishek Phago', 'phago@gmail.com', 'TEsting', 'testing message function', '2025-11-05 06:46:31');


-- Table structure for `provider_licenses`
DROP TABLE IF EXISTS `provider_licenses`;
CREATE TABLE `provider_licenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider_id` int DEFAULT NULL,
  `license_file` varchar(255) NOT NULL,
  `license_type` varchar(100) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `provider_id` (`provider_id`),
  CONSTRAINT `provider_licenses_ibfk_1` FOREIGN KEY (`provider_id`) REFERENCES `providers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Table structure for `providers`
DROP TABLE IF EXISTS `providers`;
CREATE TABLE `providers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `service_type` varchar(100) NOT NULL,
  `business_name` varchar(150) DEFAULT NULL,
  `description` text,
  `location` varchar(200) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `reviews_count` int DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `license_document` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `providers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `providers`
INSERT INTO `providers` (`id`, `user_id`, `service_type`, `business_name`, `description`, `location`, `rating`, `reviews_count`, `photo`, `is_approved`, `status`, `created_at`, `license_document`) VALUES
(1, 3, 'Electrician', 'Abhishek Electric', 'I provide best services in that area.', 'Biratnagar-03', 3.5, 2, '526029000_1275849847477136_6834623697450886638_n.jpg', 1, 'approved', '2025-11-03 06:48:41', 'Screenshot_2023-09-05_093456.png'),
(2, 8, 'Electrician', 'Iswor Electric and services', 'Quality Services with minimal cost', 'Biratnagar-4', 3.0, 1, 'WIN_20230527_10_04_38_Pro.jpg', 1, 'approved', '2025-11-04 14:21:28', 'Screenshot_1.png');


-- Table structure for `ratings`
DROP TABLE IF EXISTS `ratings`;
CREATE TABLE `ratings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `rating` int NOT NULL,
  `review` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `provider_id` (`provider_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`provider_id`) REFERENCES `providers` (`id`),
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `ratings`
INSERT INTO `ratings` (`id`, `provider_id`, `user_id`, `rating`, `review`, `created_at`) VALUES
(1, 1, 2, 3, '', '2025-11-03 09:56:53'),
(2, 2, 2, 3, '', '2025-11-04 14:49:38'),
(3, 1, 9, 4, '', '2025-11-05 06:46:48');


-- Table structure for `services`
DROP TABLE IF EXISTS `services`;
CREATE TABLE `services` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `icon` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `services`
INSERT INTO `services` (`id`, `name`, `description`, `icon`, `image`, `created_at`) VALUES
(1, 'Plumbing', 'Professional plumbing services', 'fa-wrench', NULL, '2025-11-03 06:37:40'),
(2, 'Electrician', 'Licensed electrical services', 'fa-bolt', NULL, '2025-11-03 06:37:40'),
(3, 'Mechanic', 'Auto repair and maintenance', 'fa-car', NULL, '2025-11-03 06:37:40'),
(4, 'Cleaning', 'Home and office cleaning', 'fa-broom', NULL, '2025-11-03 06:37:40'),
(6, 'Gardening', 'Garden maintenance and landscaping', 'fa-leaf', NULL, '2025-11-03 06:37:40'),
(7, 'Painting', 'Interior and exterior painting', 'fa-paint-roller', NULL, '2025-11-03 06:37:40'),
(8, 'Carpentry', 'Custom woodwork and repairs', 'fa-hammer', NULL, '2025-11-03 06:37:40'),
(9, 'Pest Control', 'Pest elimination services', 'fa-bug', NULL, '2025-11-03 06:37:40'),
(10, 'Moving', 'Relocation and moving services', 'fa-truck', NULL, '2025-11-03 06:37:40'),
(12, 'Catering', 'Event catering services', 'fa-utensils', NULL, '2025-11-03 06:37:40'),
(13, 'Photographer', 'Photos and videos for events.', 'fa-camera', NULL, '2025-11-04 10:02:16');


-- Table structure for `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `users`
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `full_name`, `phone`, `user_type`, `created_at`) VALUES
(1, 'dineshnepal11', 'dineshnepal@gmail.com', 'scrypt:32768:8:1$9p6bayFlBmj1aYej$7842133b14182cc22e173df90996add822c2c6a3bba707fac9e55751e32231cb3ba142c7d3a1e545be2cc5985263add9c6a86173d5070f2c63f014e52724d6ea', 'System Administrator', '0000000000', 'admin', '2025-11-03 06:37:40'),
(2, 'sitbht@1', 'sit.bht@gmail.com', 'scrypt:32768:8:1$PaqbCnnIaekgiaL3$0c0335ac145d7d4a0e406d5997c57976048f83ed1454febbf8a1c05c192525212ca8af1a4158fc1aa6b9daa6c789823db7b4fb095951ab05cc2a03dd14cfbbbf', 'Sittal Bhattarai', '9861107729', 'customer', '2025-11-03 06:41:18'),
(3, 'abhishek@1', 'abhisheknepal@gmail.com', 'scrypt:32768:8:1$MmFLJfxc8ljvm0hR$1f4d2969b2f82cd145b43113f3f300bc03291a5472ef25acb236f71bec6003d268e3f2011628ed9f6bdcd383306e77a8e08ce055a09d745c6ff775eaa5cb3e55', 'Abhishek Nepal', '9862306186', 'provider', '2025-11-03 06:44:50'),
(8, 'iswordahal1', 'iswordahal@gmail.com', 'scrypt:32768:8:1$0kkitOCQVwxIaaR7$edce4112babc9418cbf8862b16211f61b18a9cd37b5a4000f10b3dbcc307d21e5de4b1c395e40d5fb1defa0313ce3f22ec9b676b9513e932da806d5f586ab717', 'Iswor Dahal', '9800909535', 'provider', '2025-11-04 14:17:23'),
(9, 'abhishek@123', 'phago@gmail.com', 'scrypt:32768:8:1$VG0z2Ftl9VceSSie$eb9a36f15ed4313383c6fc6e9440c198d30fd9d11ed7b78224d97da0556dc047c327cc92fec241443816e2676c842c72f908029b3fd56336dfd7767b37990ca7', 'Abhishek Wanem Phago', '9845263257', 'customer', '2025-11-05 06:45:16');

