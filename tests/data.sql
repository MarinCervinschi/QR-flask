-- Insert test users
INSERT INTO users (username, password) VALUES ('test', 'scrypt:32768:8:1$zDTU2CWuivDwFAfb$a8e74f1bdaf2bccdf3b5021aadddfa2f7e38210d418167330e90af07914c55d820245975e991b91dc9db66b99110bece037f524d139921608e4276f5f6be5e10');

-- Insert test links
INSERT INTO dynamic_links (internal, external) VALUES ('test_link1', 'http://example.com/1');
INSERT INTO dynamic_links (internal, external) VALUES ('test_link2', 'http://example.com/2');