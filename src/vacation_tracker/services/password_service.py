import hashlib   # встроенный модуль для хеширования
import os        # нужен для случайной соли

def hash_password(password):
    salt = os.urandom(16).hex()   # случайная соль, у каждого пользователя своя
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt + "$" + hashed    # в базе будет храниться "соль$хеш"

def check_password(password, stored):
    salt, hashed = stored.split("$")   # делим строку из базы на соль и хеш
    # считаем хеш введённого пароля с той же солью и сравниваем
    return hashlib.sha256((salt + password).encode()).hexdigest() == hashed