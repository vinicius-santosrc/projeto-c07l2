-- 1. DDL - BANCO DE DADOS E TABELAS
DROP DATABASE IF EXISTS STEAM_DB;
CREATE DATABASE STEAM_DB;
USE STEAM_DB;

CREATE TABLE usuario (
  id_usuario     INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nome           VARCHAR(100) NOT NULL,
  email          VARCHAR(120) NOT NULL UNIQUE,
  senha          VARCHAR(255) NOT NULL,
  data_cadastro  DATE NOT NULL
);

CREATE TABLE perfil (
  id_perfil   INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nickname    VARCHAR(50) NOT NULL,
  foto        VARCHAR(255),
  biografia   VARCHAR(255),
  id_usuario  INT NOT NULL UNIQUE,
  FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE desenvolvedora (
  id_desenvolvedora  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nome               VARCHAR(100) NOT NULL,
  pais               VARCHAR(60),
  site               VARCHAR(150)
);

CREATE TABLE categoria (
  id_categoria  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nome          VARCHAR(50) NOT NULL,
  descricao     VARCHAR(150)
);

CREATE TABLE jogo (
  id_jogo                   INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  titulo                    VARCHAR(100) NOT NULL,
  descricao                 VARCHAR(255),
  preco                     DECIMAL(10,2) NOT NULL,
  data_lancamento           DATE,
  classificacao_indicativa  VARCHAR(10),
  id_desenvolvedora         INT NOT NULL,
  id_categoria              INT NOT NULL,
  FOREIGN KEY (id_desenvolvedora) REFERENCES desenvolvedora (id_desenvolvedora)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE compra (
  id_usuario       INT NOT NULL,
  id_jogo          INT NOT NULL,
  data_compra      DATETIME NOT NULL,
  valor_pago       DECIMAL(10,2) NOT NULL,
  forma_pagamento  VARCHAR(30),
  PRIMARY KEY (id_usuario, id_jogo),
  FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_jogo) REFERENCES jogo (id_jogo)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

SHOW TABLES;

-- 2. DML - INSERÇÃO DE DADOS (mínimo de 5 registros por tabela)
INSERT INTO usuario (nome, email, senha, data_cadastro) VALUES
  ('Ana Souza',      'ana.souza@email.com',      SHA2('ana@123', 256),    '2022-03-10'),
  ('Bruno Lima',     'bruno.lima@email.com',     SHA2('bruno@123', 256),  '2022-07-21'),
  ('Carla Mendes',   'carla.mendes@email.com',   SHA2('carla@123', 256),  '2023-01-15'),
  ('Diego Rocha',    'diego.rocha@email.com',    SHA2('diego@123', 256),  '2023-05-02'),
  ('Elisa Ferreira', 'elisa.ferreira@email.com', SHA2('elisa@123', 256),  '2024-02-28'),
  ('Felipe Alves',   'felipe.alves@email.com',   SHA2('felipe@123', 256), '2024-09-09');

INSERT INTO perfil (nickname, foto, biografia, id_usuario) VALUES
  ('AnaGamer',     'fotos/ana.png',    'Fã de RPGs e jogos de história.',       1),
  ('BruxoBruno',   'fotos/bruno.png',  'Colecionador de jogos indie.',          2),
  ('CarlaPlays',   NULL,               'Streamer nas horas vagas.',             3),
  ('DiegoSpeed',   'fotos/diego.png',  NULL,                                    4),
  ('ElisaQuebra',  'fotos/elisa.png',  'Apaixonada por quebra-cabeças.',        5),
  ('FelipeNoob',   NULL,               'Começando agora no mundo dos games.',   6);

INSERT INTO desenvolvedora (nome, pais, site) VALUES
  ('CD Projekt RED',   'Polônia',   'https://www.cdprojektred.com'),
  ('Supergiant Games', 'EUA',       'https://www.supergiantgames.com'),
  ('ConcernedApe',     'EUA',       'https://www.stardewvalley.net'),
  ('Valve',            'EUA',       'https://www.valvesoftware.com'),
  ('Team Cherry',      'Austrália', 'https://www.teamcherry.com.au'),
  ('Re-Logic',         'EUA',       'https://re-logic.com'),
  ('Maddy Makes Games','Canadá',    'https://www.celestegame.com');

INSERT INTO categoria (nome, descricao) VALUES
  ('RPG',           'Jogos de interpretação de papéis com foco em história e evolução.'),
  ('Ação',          'Jogos com combate e reflexos em tempo real.'),
  ('Simulação',     'Jogos que simulam atividades do dia a dia.'),
  ('Quebra-cabeça', 'Jogos baseados em lógica e resolução de problemas.'),
  ('Aventura',      'Jogos de exploração e descoberta.'),
  ('Plataforma',    'Jogos de pulos e obstáculos em cenários 2D/3D.');

INSERT INTO jogo (titulo, descricao, preco, data_lancamento, classificacao_indicativa, id_desenvolvedora, id_categoria) VALUES
  ('The Witcher 3: Wild Hunt', 'RPG de mundo aberto sobre um caçador de monstros.',         79.99, '2015-05-19', '18', 1, 1),
  ('Cyberpunk 2077',           'RPG de ação em uma metrópole futurista.',                  199.90, '2020-12-10', '18', 1, 1),
  ('Hades',                    'Roguelike de ação ambientado na mitologia grega.',          73.99, '2020-09-17', '16', 2, 2),
  ('Stardew Valley',           'Simulador de fazenda com vida social e exploração.',        24.99, '2016-02-26', 'L',  3, 3),
  ('Portal 2',                 'Quebra-cabeças em primeira pessoa com portais.',            36.99, '2011-04-19', '10', 4, 4),
  ('Left 4 Dead 2',            'Tiro cooperativo contra hordas de zumbis.',                 36.99, '2009-11-17', '18', 4, 2),
  ('Half-Life: Alyx',          'Aventura em realidade virtual no universo Half-Life.',     114.99, '2020-03-23', '16', 4, 5),
  ('Hollow Knight',            'Aventura 2D de exploração em um reino subterrâneo.',        46.99, '2017-02-24', '10', 5, 5),
  ('Terraria',                 'Aventura sandbox de escavar, construir e lutar.',           19.99, '2011-05-16', '12', 6, 5),
  ('Celeste',                  'Plataforma desafiador sobre escalar uma montanha.',         36.99, '2018-01-25', '10', 7, 6),
  ('Portal',                   'Primeiro quebra-cabeças com a arma de portais.',            36.99, '2007-10-10', '10', 4, 4);

INSERT INTO compra (id_usuario, id_jogo, data_compra, valor_pago, forma_pagamento) VALUES
  (1, 1,  '2023-02-01 14:30:00',  79.99, 'Cartão de Crédito'),
  (1, 2,  '2023-02-15 20:10:00', 159.92, 'PIX'),
  (1, 3,  '2023-06-20 09:45:00',  73.99, 'Cartão de Crédito'),
  (2, 4,  '2022-08-01 18:00:00',  24.99, 'PIX'),
  (2, 8,  '2022-12-24 22:15:00',  35.24, 'Boleto'),
  (2, 10, '2023-03-05 11:20:00',  36.99, 'PIX'),
  (3, 3,  '2023-04-10 16:00:00',  73.99, 'Cartão de Débito'),
  (3, 5,  '2023-04-10 16:05:00',  36.99, 'Cartão de Débito'),
  (4, 6,  '2023-06-12 21:40:00',  36.99, 'PIX'),
  (4, 9,  '2023-07-01 08:30:00',  19.99, 'PIX'),
  (5, 5,  '2024-03-15 13:00:00',  36.99, 'Cartão de Crédito'),
  (5, 7,  '2024-04-02 19:50:00', 114.99, 'Cartão de Crédito'),
  (5, 10, '2024-04-02 19:55:00',  36.99, 'Cartão de Crédito');

-- 3. FUNCTION, PROCEDURE, TRIGGER e VIEW
DELIMITER $$

DROP FUNCTION IF EXISTS fn_preco_com_desconto$$

CREATE FUNCTION fn_preco_com_desconto(p_preco DECIMAL(10,2), p_percentual DECIMAL(5,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN ROUND(p_preco * (1 - p_percentual / 100), 2);
END $$

DROP PROCEDURE IF EXISTS sp_registrar_compra$$

CREATE PROCEDURE sp_registrar_compra(
    IN p_id_usuario      INT,
    IN p_id_jogo         INT,
    IN p_forma_pagamento VARCHAR(30)
)
BEGIN
    DECLARE v_preco      DECIMAL(10,2);
    DECLARE v_usuario    INT;
    DECLARE v_ja_possui  INT;

    SET v_preco     = (SELECT preco FROM jogo WHERE id_jogo = p_id_jogo);
    SET v_usuario   = (SELECT COUNT(*) FROM usuario WHERE id_usuario = p_id_usuario);
    SET v_ja_possui = (SELECT COUNT(*) FROM compra
                        WHERE id_usuario = p_id_usuario AND id_jogo = p_id_jogo);

    IF v_usuario = 0 THEN
        SELECT 'Usuário não encontrado!' AS Resultado;
    ELSEIF v_preco IS NULL THEN
        SELECT 'Jogo não encontrado!' AS Resultado;
    ELSEIF v_ja_possui > 0 THEN
        SELECT 'O usuário já possui este jogo!' AS Resultado;
    ELSE
        INSERT INTO compra (id_usuario, id_jogo, data_compra, valor_pago, forma_pagamento)
        VALUES (p_id_usuario, p_id_jogo, NOW(), v_preco, p_forma_pagamento);

        SELECT 'Compra registrada com sucesso!' AS Resultado;
    END IF;
END $$

DROP TRIGGER IF EXISTS trg_compra_valor_check$$

CREATE TRIGGER trg_compra_valor_check BEFORE INSERT
ON compra
FOR EACH ROW
BEGIN
    IF NEW.valor_pago < 0 THEN
        SET NEW.valor_pago = 0;
    END IF;
END $$

DELIMITER ;

CREATE VIEW vw_biblioteca_usuario AS
SELECT
    u.nome            AS Usuario,
    p.nickname        AS Nickname,
    j.titulo          AS Jogo,
    c.nome            AS Categoria,
    d.nome            AS Desenvolvedora,
    co.data_compra    AS DataCompra,
    co.valor_pago     AS ValorPago
FROM usuario u
JOIN perfil p          ON p.id_usuario = u.id_usuario
JOIN compra co         ON co.id_usuario = u.id_usuario
JOIN jogo j            ON j.id_jogo = co.id_jogo
JOIN categoria c       ON c.id_categoria = j.id_categoria
JOIN desenvolvedora d  ON d.id_desenvolvedora = j.id_desenvolvedora;

-- 4. DML (UPDATE / DELETE) e TCL (TRANSACTION)
SET SQL_SAFE_UPDATES = 0;

UPDATE jogo SET preco = fn_preco_com_desconto(preco, 20) WHERE id_jogo = 2;

UPDATE perfil SET biografia = 'Fã de RPGs, jogos de história e Cyberpunk.' WHERE id_usuario = 1;

CALL sp_registrar_compra(6, 4, 'PIX');

DELETE FROM compra WHERE id_usuario = 6 AND id_jogo = 4;

START TRANSACTION;
SAVEPOINT antes_do_desconto;

UPDATE jogo SET preco = fn_preco_com_desconto(preco, 50) WHERE id_jogo = 7;

ROLLBACK TO antes_do_desconto;

UPDATE jogo SET preco = fn_preco_com_desconto(preco, 10) WHERE id_jogo = 7;
COMMIT;

START TRANSACTION;
INSERT INTO compra (id_usuario, id_jogo, data_compra, valor_pago, forma_pagamento)
VALUES (6, 9, NOW(), -10.00, 'PIX');
SELECT id_usuario, id_jogo, valor_pago FROM compra WHERE id_usuario = 6;
ROLLBACK;

-- 5. CONSULTAS COM JOIN

-- 5.1) 1:1
SELECT u.nome, u.email, p.nickname, p.biografia
FROM usuario u
INNER JOIN perfil p ON u.id_usuario = p.id_usuario
ORDER BY u.nome ASC;

-- 5.2) 1:N
SELECT j.titulo, j.preco, d.nome AS desenvolvedora, d.pais
FROM jogo j
INNER JOIN desenvolvedora d ON j.id_desenvolvedora = d.id_desenvolvedora
ORDER BY d.nome ASC;

-- 5.3) 1:N
SELECT d.nome AS desenvolvedora,
       COUNT(j.id_jogo) AS total_jogos,
       ROUND(AVG(j.preco), 2) AS preco_medio
FROM desenvolvedora d
INNER JOIN jogo j ON d.id_desenvolvedora = j.id_desenvolvedora
GROUP BY d.id_desenvolvedora, d.nome
ORDER BY total_jogos DESC;

-- 5.4) 1:N
SELECT j.titulo, j.preco, c.nome AS categoria
FROM jogo j
INNER JOIN categoria c ON j.id_categoria = c.id_categoria
WHERE c.nome = 'Aventura' AND j.preco BETWEEN 15 AND 50
ORDER BY j.preco DESC;

-- 5.5) N:M
SELECT p.nickname, j.titulo, co.valor_pago, co.forma_pagamento
FROM usuario u
INNER JOIN perfil p  ON u.id_usuario = p.id_usuario
INNER JOIN compra co ON u.id_usuario = co.id_usuario
INNER JOIN jogo j    ON co.id_jogo = j.id_jogo
ORDER BY p.nickname ASC;

-- 5.6) N:M
SELECT u.nome, COUNT(co.id_jogo) AS total_jogos, SUM(co.valor_pago) AS total_gasto
FROM usuario u
INNER JOIN compra co ON u.id_usuario = co.id_usuario
GROUP BY u.id_usuario, u.nome
HAVING COUNT(co.id_jogo) > 2;

-- 5.7) N:M
SELECT j.titulo, COUNT(co.id_usuario) AS vendas, SUM(co.valor_pago) AS faturamento
FROM jogo j
INNER JOIN compra co ON j.id_jogo = co.id_jogo
GROUP BY j.id_jogo, j.titulo
ORDER BY vendas DESC, faturamento DESC
LIMIT 3;

-- 5.8) N:M
SELECT u.nome, j.titulo, co.valor_pago, co.data_compra
FROM usuario u
INNER JOIN compra co ON u.id_usuario = co.id_usuario
INNER JOIN jogo j    ON co.id_jogo = j.id_jogo
WHERE co.forma_pagamento = 'PIX'
  AND co.data_compra BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY co.data_compra ASC;

-- 6. TESTES DA FUNCTION E DA VIEW
SELECT titulo, preco, fn_preco_com_desconto(preco, 15) AS preco_promocional
FROM jogo;

SELECT * FROM vw_biblioteca_usuario WHERE Usuario = 'Ana Souza';

-- 7. DCL - USUÁRIOS, ROLES, GRANT e REVOKE
DROP USER IF EXISTS 'usr_analista'@'localhost';
DROP USER IF EXISTS 'usr_atendente'@'localhost';
DROP ROLE IF EXISTS 'role_steam_consulta';
DROP ROLE IF EXISTS 'role_steam_operador';

CREATE ROLE 'role_steam_consulta';
GRANT SELECT ON STEAM_DB.* TO 'role_steam_consulta';

CREATE ROLE 'role_steam_operador';
GRANT INSERT, UPDATE ON STEAM_DB.compra TO 'role_steam_operador';

CREATE USER 'usr_analista'@'localhost'  IDENTIFIED BY 'Analista@123';
CREATE USER 'usr_atendente'@'localhost' IDENTIFIED BY 'Atendente@123';

GRANT 'role_steam_consulta' TO 'usr_analista'@'localhost';
GRANT 'role_steam_consulta' TO 'usr_atendente'@'localhost';
GRANT 'role_steam_operador' TO 'usr_atendente'@'localhost';

SET DEFAULT ROLE 'role_steam_consulta' TO 'usr_analista'@'localhost';
SET DEFAULT ROLE ALL TO 'usr_atendente'@'localhost';

REVOKE UPDATE ON STEAM_DB.compra FROM 'role_steam_operador';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'usr_atendente'@'localhost';