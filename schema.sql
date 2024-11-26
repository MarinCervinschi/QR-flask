CREATE DATABASE IF NOT EXISTS qr_db;

USE qr_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS dynamic_links;
CREATE TABLE dynamic_links (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internal VARCHAR(255) UNIQUE NOT NULL,
  external TEXT NOT NULL
);
-- insert admin user
INSERT INTO users (username, password) VALUES ('isa', 'scrypt:32768:8:1$Tl4A3uPdq5MZwhXo$1d840e3016be8c46d058d44105469baae7b853a3e7e62f9afcce91f6b5fd68d0402bab7a9502d860fe4cfe3092d925f90a159e959723a93854109d8014f89b27');
INSERT INTO users (username, password) VALUES ('marin', 'scrypt:32768:8:1$oLWzlj70mmIONXpS$1b338a31eaae838a4a691db89f6e8d1e81e9a8fc40911cbe7e214938021700a0fa74abca22bfef75c1b50cb0fa96b7bd1093c5fbc8970eeb5dff0326c117916b');

-- insert test link
INSERT INTO dynamic_links (internal, external) VALUES ('test_link', 'https://google.com');