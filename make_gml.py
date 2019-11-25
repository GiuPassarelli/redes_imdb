import pymysql
import json
import os
import networkx as nx
import freeman as fm
from unidecode import unidecode
import pandas as pd
import numpy as np
import scipy.stats as stats

def run_db_query(connection, query, args=None):
    with connection.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)
            
with open('config_tests.json', 'r') as f:
    config = json.load(f)

conn = pymysql.connect(
    host=config['HOST'],
    user=config['USER'],
    password=config['PASS'],
    database='imdb'
)

id_genero = 10770

filename = 'dados/twomode1_' + str(id_genero) + '.gml'
with open(filename,'w',encoding='utf-8') as file:
    with conn.cursor() as cursor:
        file.write('graph [\n')
        file.write('  directed 1\n')
        
        movie_ids = []
        
        cursor.execute("SELECT id_filme, title FROM filme INNER JOIN filme_genero using (id_filme) WHERE id_genero = %s", id_genero)
        res = cursor.fetchall()

        for i in res:
            filme = i[1].replace("[", "")
            filme = filme.replace("]", "")
            filme = filme.replace('"', "")
            filme = filme.replace("'", "")
            file.write('  node [\n')
            file.write('    id "f_{}"\n'.format(i[0]))
            file.write('    type "filme"\n')
            file.write('    label "{}"\n'.format(unidecode(filme)))
            file.write('  ]\n')
            movie_ids.append(i[0])

        cursor.execute("SELECT id_keyword, nome FROM keyword")
        res = cursor.fetchall()

        for i in res:
            key = i[1].replace("[", "")
            key = key.replace("]", "")
            key = key.replace('"', "")
            key = key.replace("'", "")
            file.write('  node [\n')
            file.write('    id "k_{}"\n'.format(i[0]))
            file.write('    type "keyword"\n')
            file.write('    label "{}"\n'.format(unidecode(key)))
            file.write('  ]\n')

        for filme in movie_ids:
            cursor.execute("SELECT id_keyword FROM filme_keyword WHERE id_filme = %s", filme)
            keys = cursor.fetchall()
            
            for key in keys:
                file.write('  edge [\n')
                file.write('    source "f_{}"\n'.format(filme))
                file.write('    target "k_{}"\n'.format(key[0]))
                file.write('  ]\n')

        file.write(']\n')

with conn.cursor() as cursor:

    keys_movie = {}
    all_keys = []
    keys_used = []
    key_conn = []   #lista com a lista de conecções
    num_conn = []   #lista com numero de filmes iguais

    cursor.execute("SELECT id_filme, id_keyword FROM filme_keyword INNER JOIN filme_genero using (id_filme) WHERE id_genero = %s", id_genero)
    res = cursor.fetchall()

    for filme, key in res:
        if(key in keys_movie):
            keys_movie[key].append(filme)
        else:
            keys_movie[key] = [filme]
        if(key not in all_keys):
            all_keys.append(key)

    for key_value in range(len(all_keys)):
        for comparedk in range(key_value + 1, len(all_keys)):
            num_connections = 0

            if(all_keys[key_value] in keys_movie):
                for movie in keys_movie[all_keys[key_value]]:
                    if(all_keys[comparedk] in keys_movie):
                        if movie in keys_movie[all_keys[comparedk]]:
                            num_connections += 1

            if num_connections > 1:
                if (all_keys[key_value] not in keys_used):
                    keys_used.append(all_keys[key_value])
                if (all_keys[comparedk] not in keys_used):
                    keys_used.append(all_keys[comparedk])
                key_conn.append([all_keys[key_value], all_keys[comparedk]])
                num_conn.append(num_connections)

print("Moda onemode1: ", max(set(num_conn), key=num_conn.count))

filename = 'dados/onemode1_' + str(id_genero) + '.gml'
with open(filename,'w',encoding='utf-8') as file:
    with conn.cursor() as cursor:
        file.write('graph [\n')
        file.write('  directed 0\n')

        for i in keys_used:
            cursor.execute("SELECT nome FROM keyword WHERE id_keyword = %s", i)
            key_name = cursor.fetchone()
            file.write('  node [\n')
            file.write('    id "k_{}"\n'.format(i))
            file.write('    label "{}"\n'.format(unidecode(key_name[0])))
            file.write('  ]\n')

        for i in range(len(key_conn)):
            file.write('  edge [\n')
            file.write('    source "k_{}"\n'.format(key_conn[i][0]))
            file.write('    target "k_{}"\n'.format(key_conn[i][1]))
            file.write('  ]\n')

        file.write(']\n')

with conn.cursor() as cursor:
    movie_keys = {}
    all_movies = []
    movies_used = []
    movie_conn = []
    num_conn = []
    
    cursor.execute("SELECT id_filme, id_keyword FROM filme_keyword INNER JOIN filme_genero using (id_filme) WHERE id_genero = %s", id_genero)
    res = cursor.fetchall()

    for filme, key in res:
        if(filme in movie_keys):
            movie_keys[filme].append(key)
        else:
            movie_keys[filme] = [key]
        if(filme not in all_movies):
            all_movies.append(filme)
    
    for movie_value in range(len(all_movies)):
        for comparedm in range(movie_value + 1, len(all_movies)):
            num_connections = 0

            if(all_movies[movie_value] in movie_keys):
                for key in movie_keys[all_movies[movie_value]]:
                    if(all_movies[comparedm] in movie_keys):
                        if key in movie_keys[all_movies[comparedm]]:
                            num_connections += 1
            
            # checar a moda colocada nas arestas; 
            # medir quando o valor for 0
            if num_connections > 1:
                if (all_movies[movie_value] not in movies_used):
                    movies_used.append(all_movies[movie_value])
                if (all_movies[comparedm] not in movies_used):
                    movies_used.append(all_movies[comparedm])
                movie_conn.append([all_movies[movie_value], all_movies[comparedm]])
                num_conn.append(num_connections)

print("Moda onemode2: ", max(set(num_conn), key=num_conn.count))

filename = 'dados/onemode2_' + str(id_genero) + '.gml'
with open(filename,'w',encoding='utf-8') as file:
    with conn.cursor() as cursor:
        file.write('graph [\n')
        file.write('  directed 0\n')

        for i in movies_used:
            cursor.execute("SELECT title FROM filme WHERE id_filme = %s", i)
            movie_title = cursor.fetchone()
            filme = movie_title[0].replace("[", "")
            filme = filme.replace("]", "")
            filme = filme.replace('"', "")
            filme = filme.replace("'", "")
            file.write('  node [\n')
            file.write('    id "k_{}"\n'.format(i))
            file.write('    label "{}"\n'.format(unidecode(filme)))
            file.write('  ]\n')

        for i in range(len(movie_conn)):
            file.write('  edge [\n')
            file.write('    source "k_{}"\n'.format(movie_conn[i][0]))
            file.write('    target "k_{}"\n'.format(movie_conn[i][1]))
            file.write('  ]\n')

        file.write(']\n')