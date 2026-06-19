

def get_server(headers):
    for nome in headers:                 
        if nome.lower()=="server":
            return headers[nome]
    return None  

def get_powered_by(headers):
    for nome in headers:
        if nome .lower()== "x-powered-by":
           return headers[nome]
    return None