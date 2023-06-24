CREATE DATABASE IF NOT EXISTS banco_de_ip;

USE banco_de_ip;

CREATE TABLE mensagens (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ip VARCHAR(45),
  regiao VARCHAR(100),
  cidade VARCHAR(100)
);
