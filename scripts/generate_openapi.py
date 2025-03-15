import requests

def fetch_openapi_schema():
    response = requests.get("http://127.0.0.1:8000/openapi.json")
    with open("./openapi.json", "w") as file:
        file.write(response.text)

if __name__ == "__main__":
    fetch_openapi_schema()