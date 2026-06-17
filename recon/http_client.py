import requests ## Documentaçao https://requests.readthedocs.io/en/latest/user/quickstart/

def send_requests(method, url, payload):
    if method == "GET":
        r = requests.get(url, timeout=5)
    elif method == "POST":
        r = requests.post(url, data=payload, timeout=5)
    elif method == "PUT":
        r = requests.put(url, data=payload, timeout=5)
    elif method == "DELETE":
        r = requests.delete(url, timeout=5)
    elif method == "OPTIONS":
        r = requests.options(url, timeout=5)
    elif method == "HEAD":
        r = requests.head(url, timeout=5)
    else:
        raise ValueError("Invalid HTTP method")

    return r
