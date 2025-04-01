import requests

# URL для получения токена и создания пользователей
ADMIN_TOKEN_URL = "http://192.168.49.2:30001/realms/master/protocol/openid-connect/token"
KEYCLOAK_URL = "http://192.168.49.2:30001/admin/realms/myrealm/users"

try:
    # Получение токена
    response = requests.post(ADMIN_TOKEN_URL, data={
        "client_id": "admin-cli",
        "username": "admin",
        "password": "admin",
        "grant_type": "password"
    })
    response.raise_for_status()
    token = response.json().get("access_token")
    print("Admin Token:", token)

    # Создание пользователей
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    for i in range(1, 101):
        user_data = {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "enabled": True,
            "credentials": [{"type": "password", "value": f"password{i}", "temporary": False}]
        }
        response = requests.post(KEYCLOAK_URL, headers=headers, json=user_data)
        if response.status_code == 201:
            print(f"User user{i} created successfully.")
        else:
            print(f"Failed to create user user{i}: {response.text}")
except requests.exceptions.RequestException as e:
    print("Error:", e)