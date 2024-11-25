CREATE DATABASE IF NOT EXISTS qr_db;

USE qr_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  is_admin BOOLEAN DEFAULT FALSE
);

-- insert admin user
INSERT INTO users (username, password, is_admin) VALUES ('admin', 'admin', true);