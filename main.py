import requests
import os
import json
from time import sleep
from recon.http_client import send_requests ## aqui pega o arquivo http_client.py e importa a função
import re


def main():
    with open("urls.txt", "r", encoding="utf-8") as f:
        urls = f.read().splitlines()
    for url in urls:
        send_requests("GET", url, None)

main()
