from requests import delete, get


print(delete('http://127.0.0.1:8080/api/jobs/999').json())
# новости с id = 999 нет в базе

print(delete('http://127.0.0.1:8080/api/jobs/q').json())
# q - неправильный запрос

print(delete('http://127.0.0.1:8080/api/jobs').json())
# нет аргументов

print(delete('http://127.0.0.1:8080/api/jobs/4').json())

print(get('http://127.0.0.1:8080/api/jobs').json())
