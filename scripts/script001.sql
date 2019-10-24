DROP DATABASE IF EXISTS imdb;
CREATE DATABASE imdb;
USE imdb;

CREATE TABLE filme (
    id_filme INT NOT NULL,
    title VARCHAR(100),
    budget INT UNSIGNED,
    revenue INT UNSIGNED,
    runtime INT,
    status_f VARCHAR(80),
    release_date DATE,
    original_language VARCHAR(80),
    vote_count INT,
    vote_average INT,
    popularity INT,
    PRIMARY KEY (id_filme)
);

CREATE TABLE keyword (
    id_keyword INT NOT NULL,
    nome VARCHAR(80),
    PRIMARY KEY (id_keyword)
);

CREATE TABLE genero (
    id_genero INT NOT NULL,
    nome VARCHAR(80),
    PRIMARY KEY (id_genero)
);

CREATE TABLE filme_keyword (
    id_filme INT NOT NULL,
    id_keyword INT NOT NULL,
    PRIMARY KEY (id_filme, id_keyword),
    FOREIGN KEY (id_filme)
        REFERENCES filme (id_filme),
    FOREIGN KEY (id_keyword)
        REFERENCES keyword (id_keyword)
);

CREATE TABLE filme_genero (
    id_filme INT NOT NULL,
    id_genero INT NOT NULL,
    PRIMARY KEY (id_filme, id_genero),
    FOREIGN KEY (id_filme)
        REFERENCES filme (id_filme),
    FOREIGN KEY (id_genero)
        REFERENCES genero (id_genero)
);

CREATE TABLE recomendacoes (
    id_filme1 INT NOT NULL,
    id_filme2 INT NOT NULL,
    PRIMARY KEY (id_filme1, id_filme2),
    FOREIGN KEY (id_filme1)
        REFERENCES filme (id_filme),
    FOREIGN KEY (id_filme2)
        REFERENCES filme (id_filme)
);