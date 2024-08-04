import requests as req
from os import system

# url = "https://step.liara.run/api/v1/accounts/login/"
url = "https://step.liara.run/api/v1/owner/history/?week=1"

header = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNjIzNjI1LCJpYXQiOjE3MjI3NTk2MjUsImp0aSI6ImQzYzlmOWEyODViNTRmZmM4MDM4YjE3YjkwMjY5MzczIiwidXNlcl9pZCI6MX0.lomPa4Fv5fFBzASL7UQZNToc-uU2W50BZxcfwy96dg4"
}

data = {
    "username": "admin",
    "password": "123456"
}

response = req.get(url, headers=header)
system("cls")
if response.status_code == 200:
    print(response.json())
else:
    print(response.text)
