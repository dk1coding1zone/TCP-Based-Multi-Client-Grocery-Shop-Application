import socket

# Define the server's host and port
HOST = '127.0.0.1'  # Localhost
PORT = 65432

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    try:
        while True:
            # Receive data from the server
            server_message = client.recv(1024).decode()
            print(server_message)

            # If the server message is a prompt for a choice or input, send a response
            if "Please enter your name:" in server_message:
                name = input("Enter your name: ")
                client.sendall(name.encode())
            elif "Select a category:" in server_message:
                choice = input("Enter your choice: ")
                client.sendall(choice.encode())
            elif "Enter quantity" in server_message:
                quantity = input("Enter quantity: ")
                client.sendall(quantity.encode())
            elif "Would you like to continue shopping?" in server_message:
                continue_choice = input("Enter yes or no: ")
                client.sendall(continue_choice.encode())
                if continue_choice.lower() == 'no':
                    break
    finally:
        client.close()

if __name__ == "__main__":
    main()
