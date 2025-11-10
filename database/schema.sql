-- Local Service Finder Database Schema
-- MySQL Database

CREATE DATABASE IF NOT EXISTS `lsf_db`;
USE `lsf_db`;

-- Table: users
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT 'customer',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: services
DROP TABLE IF EXISTS `services`;
CREATE TABLE `services` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `icon` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: providers
DROP TABLE IF EXISTS `providers`;
CREATE TABLE `providers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `service_type` varchar(100) NOT NULL,
  `business_name` varchar(150) DEFAULT NULL,
  `description` text,
  `location` varchar(200) DEFAULT NULL,
  `rating` float DEFAULT '1.0',
  `reviews_count` int DEFAULT '0',
  `photo` varchar(255) DEFAULT NULL,
  `license_document` varchar(255) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT '0',
  `status` varchar(20) DEFAULT 'pending',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `providers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: ratings
DROP TABLE IF EXISTS `ratings`;
CREATE TABLE `ratings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `rating` int NOT NULL,
  `review` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `provider_id` (`provider_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`provider_id`) REFERENCES `providers` (`id`),
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: contact_messages
DROP TABLE IF EXISTS `contact_messages`;
CREATE TABLE `contact_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `subject` varchar(200) DEFAULT NULL,
  `message` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert default admin (will be removed if custom admin is created)
INSERT INTO `users` (`username`, `email`, `password_hash`, `full_name`, `phone`, `user_type`, `is_active`)
VALUES ('admin', 'admin@lsf.com', 'scrypt:32768:8:1$PLACEHOLDER', 'System Administrator', '0000000000', 'admin', 1);

-- Insert sample services
INSERT INTO `services` (`name`, `description`, `icon`) VALUES
('Plumbing', 'Professional plumbing services', 'fa-wrench'),
('Electrician', 'Licensed electrical services', 'fa-bolt'),
('Mechanic', 'Auto repair and maintenance', 'fa-car'),
('Cleaning', 'Home and office cleaning', 'fa-broom'),
('Tutoring', 'Educational tutoring services', 'fa-book'),
('Gardening', 'Garden maintenance and landscaping', 'fa-leaf'),
('Painting', 'Interior and exterior painting', 'fa-paint-roller'),
('Carpentry', 'Custom woodwork and repairs', 'fa-hammer'),
('Pest Control', 'Pest elimination services', 'fa-bug'),
('Moving', 'Relocation and moving services', 'fa-truck'),
('Security', 'Security system installation', 'fa-shield-alt'),
('Catering', 'Event catering services', 'fa-utensils');