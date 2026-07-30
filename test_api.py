import requests

url = "https://ai-resume-analyzer-eta-olive.vercel.app/api/auth/register"
payload = {
    "email": "test501@example.com",
    "password": "TestPass123!",
    "full_name": "Test User"
}
try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
