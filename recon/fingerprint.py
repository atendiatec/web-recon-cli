

def get_server(headers):
    for nome in headers:                 
        if nome.lower()=="server":
            return headers[nome]
    return None