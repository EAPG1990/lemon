import requests

response = requests.post(
    'http://localhost:5000/api/v1/chat',
    json={'message': '¿Cómo activo mi tarjeta Lemon?'}
)

print("Status Code:", response.status_code)
print("Response:", response.json())