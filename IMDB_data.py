import pymysql
import json
from functools import partial
import tmdbsimple as tmdb

def run_db_query(connection, query, args=None):
    with connection.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)

with open('config_tests.json', 'r') as f:
    config = json.load(f)

connection = pymysql.connect(
    host=config['HOST'],
    user=config['USER'],
    password=config['PASS'],
    database='imdb'
)

db = partial(run_db_query, connection)

tmdb.API_KEY = config['API_KEY']

#Tabela genero
genres = tmdb.Genres()
response = genres.movie_list()
for i in response["genres"]:
    db("START TRANSACTION;")
    try:
        db("CALL adiciona_genero(%s, %s);", (i["id"], i["name"]))
        db("COMMIT;")
    except Exception as e:
        print(e);
        db('ROLLBACK');



def add_filme(info):
    db("START TRANSACTION;")
    try:
        db("CALL adiciona_filme(%s, %s, %s, %s, %s, %s, DATE(%s), %s, %s, %s, %s);",
           (info["id"], info["title"], info["budget"], info["revenue"], info["runtime"], info["status"],
            str(info["release_date"]), info["original_language"], info["vote_count"], info["vote_average"], info["popularity"]))
        db("COMMIT;")
    except Exception as e:
        print(e);
        db('ROLLBACK');
        
def add_keyword(keywords):
    for key in keywords["keywords"]:
        db("START TRANSACTION;")
        try:
            db("CALL adiciona_keyword(%s, %s);", (key["id"], key["name"]))
            db("COMMIT;")
        except Exception as e:
            print(e);
            db('ROLLBACK');

def add_filme_keyword(info, keywords):
    for key in keywords["keywords"]:
        db("START TRANSACTION;")
        try:
            db("CALL adiciona_filme_keyword(%s, %s);", (info["id"], key["id"]))
            db("COMMIT;")
        except Exception as e:
            print(e);
            db('ROLLBACK');

def add_filme_genero(info):
    for genre in info["genres"]:
        db("START TRANSACTION;")
        try:
            db("CALL adiciona_filme_genero(%s, %s);", (info["id"], genre["id"]))
            db("COMMIT;")
        except Exception as e:
            print(e);
            db('ROLLBACK');

def main_funct(i):
    movie = tmdb.Movies(i["id"])
    info = movie.info()
    add_filme(info)
    keywords = movie.keywords()
    add_keyword(keywords)
    add_filme_keyword(info, keywords)
    add_filme_genero(info)

def add_recomendacoes(id_filme1, id_filme2):
    db("START TRANSACTION;")
    try:
        db("CALL adiciona_recomendacoes(%s, %s);", (id_filme1, id_filme2))
        db("COMMIT;")
    except Exception as e:
        print(e);
        db('ROLLBACK');

#Adicionando alguns filmes por genero

with connection.cursor() as cursor:
    cursor.execute("SELECT id_genero FROM genero;")
    genres_ids = cursor.fetchall()

for genre in genres_ids:
    discover = tmdb.Discover()
    response = discover.movie(with_genres = genre)
    for i in discover.results:
        with connection.cursor() as cursor:
            cursor.execute("SELECT title FROM filme WHERE id_filme = %s;", i['id'])
            film_title = cursor.fetchone()
        if(film_title is None):
            main_funct(i)

#Loop infinito para pegar mais filmes

with connection.cursor() as cursor:
    cursor.execute("SELECT id_filme FROM filme;")
    filmes_ids = cursor.fetchall()

ids_filmes = []
for i in filmes_ids:
    ids_filmes.append(i[0])

for filme in ids_filmes:
    movie = tmdb.Movies(filme)
    response = movie.recommendations()
    for i in movie.results:
        with connection.cursor() as cursor:
            cursor.execute("SELECT title FROM filme WHERE id_filme = %s;", i['id'])
            film_title = cursor.fetchone()
        if(film_title is None):
            ids_filmes.append(i["id"])
            main_funct(i)
            add_recomendacoes(filme, i["id"])
