import socket
from views import *

PATHS = {
    '/': index,
    '/blog': blog
}


def parse_request(request: str) -> list:
    """
        Parse request
        get from request method and url

        Parametrs
        ----------
        request: str
            request from client

        Returns
        ----------
        list:
            method: str, url: str
    """
    parsed = request.split()
    method = parsed[0]
    url = parsed[1]

    return method, url


def generate_headers(method: str, url: str) -> list:
    """ 
        Parametrs
        ----------
        method: str
            HTTP method
        
        url: str
            URL from client request
        
        Returns
        ----------
        list:
            header: str, status_code: int

    """
    if not method == 'GET':
        return 'HTTP/1.1 405 Method Not Allowed\n\n', 405

    if not url in PATHS:
        return 'HTTP/1.1 404 Not Found\n\n', 404
    
    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(code: int, url: str) -> str:
    """
        Return HTML content for client response
        
        Parametrs
        ----------
        code: int
            status_code from headers
        url: str
            url from request
    """
    if code == 404:
        return "<h1>404</h1><p style='color: red;'>Page Not Found</p>"
    if code == 405:
        return "<h1>405</h1><p style='color: red;'>Method Not Allowed</p>"
    
    return PATHS[url]()

def generate_response(request: str) -> str:
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()


def run():
    """ 
        Create socket server and listen port 5000
    """
    socket_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # set options reuse address
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # set host and port 
    socket_server.bind(('localhost', 5000))
    # listen
    socket_server.listen()

    while True:
        client_scoket, addr = socket_server.accept()
        request = client_scoket.recv(1024)
        print(f"request {request.decode('utf-8')}, address: {addr}")

        response = generate_response(request.decode('utf-8'))

        client_scoket.sendall(response)
        client_scoket.close()


if __name__ == "__main__":
    run()