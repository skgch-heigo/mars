from requests import post, get


print(post('http://127.0.0.1:8080/api/jobs').json())
# нет json


print(post('http://127.0.0.1:8080/api/jobs',
           json={'job': 'Testing API'}).json())
# не все данные


print(post('http://127.0.0.1:8080/api/jobs',
           json={'job': 'Testing API',
                 "team_leader": "2",
                 "work_size": 120,
                 "collaborators": "1, 2",
                 "is_finished": False,
                 "author": 2, "id": 1}).json())
# такой id уже есть


print(post('http://127.0.0.1:8080/api/jobs',
           json={'job': 'Testing API',
                 "team_leader": "2",
                 "work_size": 120,
                 "collaborators": "1, 2",
                 "is_finished": False,
                 "author": 2}).json())

print(get('http://127.0.0.1:8080/api/jobs').json())
