import requests

data = {
  'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6InVzZXIiLCJleHAiOjE1MTIzNDQ3MTQsImVtYWlsIjoiIn0.xZknHx188JkKYarUn0SIrQoPtnfalwEFKStBdRzbHgc'
}
r = requests.post('http://127.0.0.1:8000/api-token-verify/',
                  data=data)

print(r.json())
