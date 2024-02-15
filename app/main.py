# Uncomment this to pass the first stage
import socket
import threading

def response(status_code, content_type, body):
    response = "HTTP/1.1 " + status_code + "\r\n"
    response += "Content-Type: " + content_type + "\r\n"
    response += "Content-Length: " + str(len(body)) + "\r\n"
    response += "\r\n"
    response += body
    return response


def handle_request(client_socket):
    data = client_socket.recv(1024)
    if not data:
        client_socket.close()
        return
    stringData = data.decode("ascii")
    lines = stringData.split("\r\n")
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
            #server_socket.send(f"HTTP/1.1 200 OK\r\n\r\n{path[6:]}".encode("ascii"))
            client_socket.send(response("200 OK", "text/plain", path[6:]).encode("ascii"))
        elif path.startswith("/user-agent"):
            client_socket.send(response("200 OK", "text/plain", headers["User-Agent"]).encode("ascii"))
        else:
            client_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode("ascii"))
    # server_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode("ascii"))
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
    main()
