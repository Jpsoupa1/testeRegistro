CREATE DATABASE clientes;
USE clientes;

CREATE TABLE usuarios(
	id_user INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
	senha varchar(100)
    );
    

SELECT * FROM usuarios;