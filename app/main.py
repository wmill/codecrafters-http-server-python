# Uncomment this to pass the first stage
import socket

def response(status_code, content_type, body):
    response = "HTTP/1.1 " + status_code + "\r\n"
    response += "Content-Type: " + content_type + "\r\n"
    response += "Content-Length: " + str(len(body)) + "\r\n"
    response += "\r\n"
    response += body
    return response


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server = socket.create_server(("localhost", 4221), reuse_port=True)
    server.listen()
    # server_socket.accept() # wait for client

    while True:
        server_socket, config = server.accept()
        
        data = server_socket.recv(1024)
        if not data:
            break
        stringData = data.decode("ascii")
        lines = stringData.split("\r\n")
        verb, path, protocol = lines[0].split(" ")
        if verb == "GET":
            if path == "/":
                server_socket.send("HTTP/1.1 200 OK\r\n\r\nHello, World!".encode("ascii"))
            elif path.startswith("/echo"):
                #server_socket.send(f"HTTP/1.1 200 OK\r\n\r\n{path[6:]}".encode("ascii"))
                server_socket.send(response("200 OK", "text/plain", path[6:]).encode("ascii"))
            else:
                server_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode("ascii"))
        # server_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode("ascii"))
        server_socket.close()


if __name__ == "__main__":
    main()
