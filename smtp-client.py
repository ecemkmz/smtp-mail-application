import ssl
from socket import socket, AF_INET, SOCK_STREAM
import base64
import os
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
sender_application_password = os.getenv("SENDER_APPLICATION_PASSWORD")

encoded_email = base64.b64encode(sender_email.encode()).decode()
encoded_password = base64.b64encode(sender_application_password.encode()).decode()

smtp_server = "smtp.gmail.com"
smtp_port = 465

try:
    context = ssl.create_default_context()
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        secure_socket = context.wrap_socket(client_socket, server_hostname=smtp_server)
        secure_socket.connect((smtp_server, smtp_port))
        response = secure_socket.recv(1024).decode()
        print(response)

        secure_socket.send(b'EHLO localhost\r\n')
        response = secure_socket.recv(1024).decode()
        print(response)

        secure_socket.send(b'AUTH LOGIN\r\n')
        response = secure_socket.recv(1024).decode()
        print(response)

        secure_socket.send(encoded_email.encode() + b'\r\n')
        response = secure_socket.recv(1024).decode()
        print(response)

        secure_socket.send(encoded_password.encode() + b'\r\n')
        response = secure_socket.recv(1024).decode()
        print(response)

        secure_socket.send(f'MAIL FROM: <{sender_email}>\r\n'.encode())
        response = secure_socket.recv(1024).decode()
        print(response)

        recipient_email = os.getenv("RECIPIENT_EMAIL")
        secure_socket.send(f'RCPT TO: <{recipient_email}>\r\n'.encode())
        response = secure_socket.recv(1024).decode()
        print(response)

        secure_socket.send(b'DATA\r\n')
        response = secure_socket.recv(1024).decode()
        print(response)

        secure_socket.send(b'Subject: System Prog. Third Week\r\n')
        message = "Burada mailin gövde mesajı gönderilmektedir."
        secure_socket.send(message.encode('utf-8') + b'\r\n')
        secure_socket.send(b'.\r\n') 
        response = secure_socket.recv(1024).decode()
        print(response)

        secure_socket.send(b'QUIT\r\n')
        response = secure_socket.recv(1024).decode()
        print(response)

except Exception as e:
    print("Bir hata oluştu:", e)