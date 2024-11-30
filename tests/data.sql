-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS test_db;

-- Switch to the test database
USE test_db;

-- Drop and recreate the users table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- Drop and recreate the dynamic_links table
DROP TABLE IF EXISTS dynamic_links;
CREATE TABLE dynamic_links (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internal VARCHAR(255) UNIQUE NOT NULL,
  external VARCHAR(255) NOT NULL
);

-- Insert test users
DELETE FROM users;
INSERT INTO users (username, password) VALUES 
('test', 'scrypt:32768:8:1$zDTU2CWuivDwFAfb$a8e74f1bdaf2bccdf3b5021aadddfa2f7e38210d418167330e90af07914c55d820245975e991b91dc9db66b99110bece037f524d139921608e4276f5f6be5e10'),
('admin', 'scrypt:32768:8:1$gHkd43zYkfiCWVzH$a79e12345df99cb2cdcc0321a8d0af123e54322bc7c229df02934875b12345d1cd4567abc89123af234234587b123f524e1399847a5f6ab');

-- Insert test dynamic links
DELETE FROM dynamic_links;
INSERT INTO dynamic_links (internal, external) VALUES 
('internal1', 'http://example1.com'),
('internal2', 'http://example2.com');