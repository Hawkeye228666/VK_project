from flask import Flask, request, jsonify
import tarantool
import zlib
import hashlib
import os
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

tarantool_host = os.getenv('TARANTOOL_HOST', '127.0.0.1')
tarantool_port = os.getenv('TARANTOOL_PORT', '3301')

connection = tarantool.Connection(
    host=tarantool_host,
    port=tarantool_port,
    user='sampleuser',
    password='123456'
)

SECRET_KEY = 'vk_project'
kv_store = connection.space('kv_store')

executor = ThreadPoolExecutor(max_workers=10)


def generate_token(data):
    s = data['username'] + data['password']
    compressed_data = zlib.compress(s.encode())
    hash_func = getattr(hashlib, 'sha256')()
    hash_func.update(compressed_data)
    token = hash_func.hexdigest()
    return token


def verify_token(token):
    result = kv_store.select(token)
    if result:
        return True
    else:
        return False


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token[7:]  # Assuming "Bearer " prefix
        if not token:
            return "You need a special token in order to access the DataBase", 403

        if not verify_token(token):
            return "Invalid token, your access has been denied", 403

        return f(*args, **kwargs)

    return decorated


def fetch_data_from_db(keys):
    results = {}
    for key in keys:
        response = kv_store.select(key)
        res = str(response)
        results[key] = res.replace("- ", "").replace("[", "").replace("]", "").replace("'", "").split(', ')[1]
    return results


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    token = generate_token(data)
    if verify_token(token):
        return f"Вы уже получали токен! Но на всякий случай напомню его Вам: {token}"

    else:
        kv_store.insert((token,))
    return jsonify({"token": token})


@app.route('/api/read', methods=['POST'])
@token_required
def read_data():
    data = request.json
    keys = data['keys']
    token = request.headers.get('Authorization')
    token = token[7:]
    for key in keys:
        response = kv_store.select(key)
        res = str(response)
        check = res.replace("- ", "").replace("[", "").replace("]", "").replace("'", "").split(', ')[2]
        print(check)
        if check != token:
            return "Это не ваша информация"

    future = executor.submit(fetch_data_from_db, keys)
    results = future.result()

    return jsonify({"data": results})


@app.route('/api/write', methods=['POST'])
@token_required
def write_data():
    data = request.json
    dictionary = list(data.get('data').items())
    for key in dictionary:
        if kv_store.select(key[0][0]):
            return "Такие данные уже есть в бд"
    token = request.headers.get('Authorization')
    token = token[7:]
    dictionary_with_token = [(key, value, token) for key, value in dictionary]

    def insert_data(item):
        kv_store.insert(item)

    futures = [executor.submit(insert_data, item) for item in dictionary_with_token]
    for future in futures:
        future.result()

    return jsonify({"status": 'success'})


@app.route('/')
def main():
    token = generate_token({'username': 'admin', 'password': 'presale'})
    if not kv_store.select():
        kv_store.insert((token,))
    return "Возьмите на стажировку(пожалуйста)"


if __name__ == '__main__':
    app.run(port='8001', debug=True)
