from urllib import response
import pymongo
import json

with open("db_operations/db_config.json", "r") as fp:
    db_config = json.load(fp)

def get_db_connection():
    try:
        client = pymongo.MongoClient("mongodb://" + db_config['database_ip'] + ':' + db_config['database_port'] + "/")
        print("Connected successfully!!!")
        db_conn = client[db_config['database_name']]
        return db_conn
    except (ConnectionError, KeyError) as e:
        return e    


def insert_movie_to_tbl(query: list) -> None:
    try:
        db_conn = get_db_connection()
        db_col = db_conn['movie']
        db_col.insert_many(query)
        return {
            "status": 200,
            "msg": "Insert to movie database successful"
        }
    except:
        return {
            "status": 400,
            "msg": "Insert to movie database failed"
        }


def insert_cast_to_tbl(query: list) -> dict:
    try:
        db_conn = get_db_connection()
        db_col = db_conn['cast']
        db_col.insert_many(query)
        return {
            "status": 200,
            "msg": "Insert to cast database successful"
        }
    except:
        return {
            "status": 400,
            "msg": "Insert to cast database failed"
        }


def insert_movie_cast_to_tbl(query: list) -> dict:
    try:
        db_conn = get_db_connection()
        db_col = db_conn['movie_cast']
        db_col.insert_many(query)
        return {
            "status": 200,
            "msg": "Insert to movie cast database successful"
        }
    except:
        return {
            "status": 400,
            "msg": "Insert to movie cast database failed"
        }


def get_movie_from_tbl(query: list) -> dict:
    try:
        db_conn = get_db_connection()
        db_col = db_conn['movie_cast']
        print(query)
        results = db_col.find({"cast": {"$all": query}})
        movies = []
        for result in results:
            movies.append(result['name'])
        print(movies)
        return {
            "status": 200,
            "msg": "Database search successful",
            "movies": movies
        }
    except:
        return {
            "status": 400,
            "msg": "Database search failed"
        }


if __name__ == "__main__":

    with open("movie_db.json", "r") as fp:
        movie_db = json.load(fp)

    movie_list = []
    for movie in movie_db:
        value = movie_db[movie]
        value['key'] = movie
        movie_list.append(value)
    result = insert_movie_to_tbl(movie_list)
    print(result)


    with open("cast_db.json", "r") as fp:
        cast_db = json.load(fp)

    cast_list = []
    for cast in cast_db:
        value = cast_db[cast]
        value['key'] = cast
        cast_list.append(value)
    result = insert_cast_to_tbl(cast_list)
    print(result)


    with open("movie_cast_db.json", "r") as fp:
        movie_cast_db = json.load(fp)

    movie_cast_list = []
    for movie_cast in movie_cast_db:
        value = movie_cast_db[movie_cast]
        value['key'] = movie_cast
        movie_cast_list.append(value)
    result = insert_movie_cast_to_tbl(movie_cast_list)
    print(result)
