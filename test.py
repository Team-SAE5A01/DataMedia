import requests

# Define the base URL of the FastAPI app
BASE_URL = "http://127.0.0.1:8000"

# 1. Make a GET request
def make_get_request():
    response = requests.get(f"{BASE_URL}/items/42", params={"q": "example"})
    print("GET Response:")
    print(response.status_code, response.json())

# 2. Make a POST request
def make_post_request():
    data = {"name": "Test Item", "value": 123}
    response = requests.post(f"{BASE_URL}/endpoint", json=data)
    print("POST Response:")
    print(response.status_code, response.json())

if __name__ == "__main__":
    make_get_request()
    make_post_request()
