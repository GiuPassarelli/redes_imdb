#PROCEDURES

USE imdb;

DROP PROCEDURE IF EXISTS adiciona_genero;
DELIMITER //
CREATE PROCEDURE adiciona_genero(IN novo_id INT, IN novo_nome VARCHAR(80))
BEGIN
    INSERT INTO genero (id_genero, nome) VALUES (novo_id, novo_nome);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS adiciona_filme;
DELIMITER //
CREATE PROCEDURE adiciona_filme(IN novo_id INT, IN novo_title VARCHAR(100), 
                                IN novo_budget INT UNSIGNED, IN novo_revenue INT UNSIGNED,
                                IN novo_runtime INT, IN novo_status VARCHAR(80),
                                IN novo_release DATE, IN novo_language VARCHAR(80),
                                IN novo_count INT, IN novo_avg INT, IN novo_pop INT)
BEGIN
    INSERT INTO filme (id_filme, title, budget, revenue, runtime, status_f, release_date, 
    original_language, vote_count, vote_average, popularity) 
    VALUES (novo_id, novo_title, novo_budget, novo_revenue, novo_runtime, novo_status, novo_release, 
    novo_language, novo_count, novo_avg, novo_pop);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS adiciona_keyword;
DELIMITER //
CREATE PROCEDURE adiciona_keyword(IN novo_id INT, IN novo_nome VARCHAR(80))
BEGIN
    INSERT INTO keyword (id_keyword, nome) VALUES (novo_id, novo_nome);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS adiciona_filme_keyword;
DELIMITER //
CREATE PROCEDURE adiciona_filme_keyword(IN novo_id_filme INT, IN novo_id_keyword INT)
BEGIN
    INSERT INTO filme_keyword (id_filme, id_keyword) VALUES (novo_id_filme, novo_id_keyword);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS adiciona_filme_genero;
DELIMITER //
CREATE PROCEDURE adiciona_filme_genero(IN novo_id_filme INT, IN novo_id_genero INT)
BEGIN
    INSERT INTO filme_genero (id_filme, id_genero) VALUES (novo_id_filme, novo_id_genero);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS adiciona_recomendacoes;
DELIMITER //
CREATE PROCEDURE adiciona_recomendacoes(IN novo_id_filme1 INT, IN novo_id_filme2 INT)
BEGIN
    INSERT INTO recomendacoes (id_filme1, id_filme2) VALUES (novo_id_filme1, novo_id_filme2);
END//
DELIMITER ;