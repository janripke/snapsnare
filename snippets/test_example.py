import json

f = open('example.json')
data = json.load(f)
print(data.get('names','niet gevonden'))
print(data)

data = {
    "name": "haas"
}

print(data.get('name'))