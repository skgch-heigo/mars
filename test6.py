from requests import put, get, post, delete

print(get('http://127.0.0.1:8080/api/users').json())

print(get('http://127.0.0.1:8080/api/users/2').json())

print(get('http://127.0.0.1:8080/api/users/168').json())
# нет такого id

print(post('http://127.0.0.1:8080/api/users',
           json={'surname': "Wilson"}).json())
# недостаточно данных

print(post('http://127.0.0.1:8080/api/users',
           json={'surname': "Wilson", 'name': "Lawrence", 'age': 26, 'position': "Detective",
                 'speciality': "Detective work", 'address': "Redcoat Street, 34", 'email': "law_w2@google.com",
                 "hashed_password": "pbkdf2:sha256:260000$aOEnFf8I5YHrGR1l$b3bdfe8e608703631552d07" +
                                    "1bdbab0f8f5665c224f1d4df295de0135b441eb3f"}).json())

print(delete('http://127.0.0.1:8080/api/users/4').json())

print(delete('http://127.0.0.1:8080/api/users/999').json())
# нет такого id

print(put('http://127.0.0.1:8080/api/users/3',
          json={'age': 26}).json())
