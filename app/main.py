# Uncomment this to pass the first stage
import socket
import threading
import argparse
import gzip

global_args = {}

def create_response(status_code, content_type, body, handles_gzip=False):
    response = "HTTP/1.1 " + status_code + "\r\n"
    if handles_gzip:
        response += "Content-Encoding: gzip\r\n"
    response += "Content-Type: " + content_type + "\r\n"
    response += "Content-Length: " + str(len(body)) + "\r\n"
    response += "\r\n"
    response = response.encode("ascii")
    if handles_gzip:
        response += gzip.compress(body.encode("ascii"))
    elif isinstance(body, str):
        response += body.encode("ascii")
    else:
        response += body
    return response


def response_404():
    return "HTTP/1.1 404 Not Found\r\n\r\n".encode("ascii")


def handle_request(client_socket):
    data = client_socket.recv(1024)
    if not data:
        client_socket.close()
        return

    headerData, bodyData = data.split(b"\r\n\r\n")
    lines = headerData.decode("ascii").split("\r\n")
    verb, path, protocol = lines[0].split(" ")
    headers = {}
    for line in lines[1:]:
        if line:
            key, value = line.split(": ")
            headers[key] = value

    handlesGzip = False
    if "Accept-Encoding" in headers:
        if "gzip" in headers["Accept-Encoding"]:
            handlesGzip = True

    response = None
    if verb == "GET":
        if path == "/":
            response = create_response("200 OK", "text/html", "<h1>Hello, World!</h1>", handlesGzip)
        elif path.startswith("/echo"):
            response = create_response("200 OK", "text/plain", path[6:], handlesGzip)
        elif path.startswith("/user-agent"):
            response = create_response("200 OK", "text/plain", headers["User-Agent"], handlesGzip)
        elif path.startswith("/files"):
            try:
                filename = path[len("/files"):]
                with open(global_args.directory + filename, "rb") as file:
                    response = create_response("200 OK", "application/octet-stream", file.read())
            except FileNotFoundError:
                response = response_404()
        else:
            response = response_404()
    elif verb == "POST":
        if path.startswith("/files"):
            filename = path[len("/files"):]
            with open(global_args.directory + filename, "wb") as file:
                file.write(bodyData)
            response = "HTTP/1.1 201 Created\r\n\r\n".encode("ascii")
    else:
        response = response_404()

    client_socket.send(response)
    client_socket.close()
    


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server = socket.create_server(("localhost", 4221), reuse_port=True)
    server.listen()
    # server_socket.accept() # wait for client


    while True:
        client_socket, config = server.accept()
        threading.Thread(target=handle_request, args=(client_socket,)).start()
        
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Toy HTTP server")
    parser.add_argument("--directory", type=str, help="Directory to serve static files from", default="/tmp/")
    args = parser.parse_args()
    global_args = args

    main()
