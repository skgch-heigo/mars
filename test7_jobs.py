from requests import put, get, post, delete

print(get('http://127.0.0.1:8080/api/v2/jobs').json())

print(get('http://127.0.0.1:8080/api/v2/jobs/2').json())

print(get('http://127.0.0.1:8080/api/v2/jobs/168').json())
# нет такого id

print(post('http://127.0.0.1:8080/api/v2/jobs',
           json={'job': "testing"}).json())
# недостаточно данных

print(post('http://127.0.0.1:8080/api/v2/jobs',
           json={'job': 'Testing API 2',
                 "team_leader": "3",
                 "work_size": 1,
                 "collaborators": "1, 2",
                 "is_finished": False,
                 "author": 3}).json())

print(delete('http://127.0.0.1:8080/api/v2/jobs/5').json())

print(delete('http://127.0.0.1:8080/api/v2/jobs/999').json())
# нет такого id

print(put('http://127.0.0.1:8080/api/v2/jobs/178',
          json={'work_size': 27}).json())
# нет такого id

print(put('http://127.0.0.1:8080/api/v2/jobs/1',
          json={'work_size': 34}).json())
