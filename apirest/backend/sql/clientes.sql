DROP TABLE IF EXISTS  clientes;

CREATE TABLE clientes(
    id_cliente INTEGER   PRIMARY KEY AUTOINCREMENT,
    nombre     VARCHAR   NOT NULL,
    email      VARCHAR   NOT NULL
);

INSERT INTO clientes(nombre,email) VALUES ("Juan","juan@gmail.com");
INSERT INTO clientes(nombre,email) VALUES ("Roberto","roberto@gmail.com");
INSERT INTO clientes(nombre,email) VALUES ("Pepe","pepe@gmail.com");

.headers ON

SELECT * FROM clientes;