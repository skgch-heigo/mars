from requests import put, get

print(put('http://127.0.0.1:8080/api/jobs/4').json())
# нет json


print(put('http://127.0.0.1:8080/api/jobs',
          json={'job': 'Testing API'}).json())
# нет id

print(put('http://127.0.0.1:8080/api/jobs/999',
          json={'job': 'Testing API edit',
                "work_size": 5,
                "is_finished": True}).json())
# такого id нет

print(put('http://127.0.0.1:8080/api/jobs/4',
          json={'job': 'Testing API edit',
                "work_size": 5,
                "is_finished": True}).json())

print(get('http://127.0.0.1:8080/api/jobs').json())
