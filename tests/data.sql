-- Usa the `qr_db` database
USE qr_db;

-- Remove all data
DELETE FROM users;
DELETE FROM dynamic_links;

-- Insert test users
INSERT INTO users (username, password) VALUES ('test_user1', 'scrypt:32768:8:1$test1$1d840e3016be8c46d058d44105469baae7b853a3e7e62f9afcce91f6b5fd68d0402bab7a9502d860fe4cfe3092d925f90a159e959723a93854109d8014f89b27');
INSERT INTO users (username, password) VALUES ('test_user2', 'scrypt:32768:8:1$test2$1b338a31eaae838a4a691db89f6e8d1e81e9a8fc40911cbe7e214938021700a0fa74abca22bfef75c1b50cb0fa96b7bd1093c5fbc8970eeb5dff0326c117916b');

-- Insert test links
INSERT INTO dynamic_links (internal, external) VALUES ('test_link1', 'http://example.com/1');
INSERT INTO dynamic_links (internal, external) VALUES ('test_link2', 'http://example.com/2');