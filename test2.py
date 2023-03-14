from requests import post

print(post('http://127.0.0.1:8080/api/jobs').json())

print(post('http://127.0.0.1:8080/api/jobs',
           json={'job': 'Testing API'}).json())

print(post('http://127.0.0.1:8080/api/jobs',
           json={'job': 'Testing API',
                 "team_leader": "2",
                 "work_size": 120,
                 "collaborators": "1, 2",
                 "is_finished": False,
                 "author": 2}).json())
