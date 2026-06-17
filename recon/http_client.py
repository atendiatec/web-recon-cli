import requests ## Documentaçao https://requests.readthedocs.io/en/latest/user/quickstart/

def send_requests(method, url, payload):
    if method == "GET":
        r = requests.get(url)
    elif method == "POST":
        r = requests.post(url, data=payload)
    elif method == "PUT":
        r = requests.put(url, data=payload)
    elif method == "DELETE":
        r = requests.delete(url)
    elif method == "OPTIONS":
        r = requests.options(url)
    elif method == "HEAD":
        r = requests.head(url)
    else:
        raise ValueError("Invalid HTTP method")

    print(f"Status Code: {r.status_code}", f"URL: {r.url}")
