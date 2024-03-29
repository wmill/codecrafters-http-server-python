import socket
import threading
import argparse

global_args = {}

def response(status_code, content_type, body):
    response = "HTTP/1.1 " + status_code + "\r\n"
    response += "Content-Type: " + content_type + "\r\n"
    response += "Content-Length: " + str(len(body)) + "\r\n"
    response += "\r\n"
    response = response.encode("ascii")
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

    if verb == "GET":
        if path == "/":
            client_socket.send("HTTP/1.1 200 OK\r\n\r\nHello, World!".encode("ascii"))
        elif path.startswith("/echo"):
            client_socket.send(response("200 OK", "text/plain", path[6:].encode("ascii")))
        elif path.startswith("/user-agent"):
            client_socket.send(response("200 OK", "text/plain", headers["User-Agent"].encode("ascii")))
        elif path.startswith("/files"):
            try:
                filename = path[len("/files"):]
                with open(global_args.directory + filename, "rb") as file:
                    client_socket.send(response("200 OK", "application/octet-stream", file.read()))
            except FileNotFoundError:
                client_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode("ascii"))
        else:
            client_socket.send(response_404())
    elif verb == "POST":
        if path.startswith("/files"):
            filename = path[len("/files"):]
            with open(global_args.directory + filename, "wb") as file:
                file.write(bodyData)
            client_socket.send("HTTP/1.1 201 OK\r\n\r\n".encode("ascii"))
    else:
        client_socket.send(response_404())

    client_socket.close()
    


def main():
    server = socket.create_server(("localhost", 4221), reuse_port=True)
    server.listen()

    while True:
        client_socket, config = server.accept()
        threading.Thread(target=handle_request, args=(client_socket,)).start()
        
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Toy HTTP server")
    parser.add_argument("--directory", type=str, help="Directory to serve static files from", default="./files")
    args = parser.parse_args()
    global_args = args

    main()
