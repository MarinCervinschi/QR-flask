CREATE DATABASE IF NOT EXISTS qr_db;

USE qr_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS dynamic_links (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internal VARCHAR(255) UNIQUE NOT NULL,
  external TEXT NOT NULL
);

-- insert admin user
INSERT INTO users (username, password) VALUES ('admin', 'admin');

-- insert test link
INSERT INTO dynamic_links (internal, external) VALUES ('test_link', 'https://google.com');