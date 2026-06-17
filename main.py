import requests
import os
import json
from time import sleep
from recon.http_client import send_requests ## aqui pega o arquivo http_client.py e importa a função
import re

from recon.fingerprint import get_server


def http_client():
    resultados = []
    with open("urls.txt", encoding="utf-8", errors="ignore") as f:
        urls = f.read().splitlines()
    for item in urls:
        try:
            r = send_requests("GET", item, None)
        except Exception as e:
            print(f"Error occurred while processing {item}: {e}")
            r = None

        if r is not None:
            resultados.append({
                "url": item,   # str
                "method": "GET",                # str
                "status_code": r.status_code,             # int
                "headers": r.headers,               # dict (requests.structures.CaseInsensitiveDict)
                "text": r.text             # str (HTML inteiro)
            })

    return resultados

def main():
    resultados = http_client()
    for r in resultados:
        print(r["url"], r["status_code"], get_server(r["headers"]))
       

if __name__ == "__main__":
    main()

