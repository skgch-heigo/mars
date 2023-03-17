from requests import put, get, post, delete

print(get('http://127.0.0.1:8080/api/v2/users').json())

print(get('http://127.0.0.1:8080/api/v2/users/2',
          json={'job': 'Testing API'}).json())

print(post('http://127.0.0.1:8080/api/v2/users',
           json={'surname': "Wilson", 'name': "Lawrence", 'age': 26, 'position': "Detective",
                 'speciality': "Detective work", 'address': "Redcoat Street, 34", 'email': "law_w@google.com",
                 "hashed_password": "pbkdf2:sha256:260000$aOEnFf8I5YHrGR1l$b3bdfe8e608703631552d07" +
                                    "1bdbab0f8f5665c224f1d4df295de0135b441eb3f"}).json())
