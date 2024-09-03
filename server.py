import socket
import threading

# Define the server's host and port
HOST = '127.0.0.1'  # Localhost
PORT = 65432

# Define available products and prices
products = {
    'Fruits': {
        'Apples': 1.2,
        'Avocados': 1.5,
        'Bananas': 0.5,
        'Berries': 2.0,
        'Cherries': 3.0
    },
    'Vegetables': {
        'Asparagus': 2.5,
        'Beets': 1.0,
        'Broccoli': 1.8,
        'Cabbage': 1.2,
        'Cauliflower': 1.5
    },
    'Dairy': {
        'Butter': 4.0,
        'Cheddar cheese': 5.0,
        'Cream cheese': 3.0,
        'Eggs': 2.5
    }
}

# Store client information
client_info = {}

def handle_client(client_socket, client_id):
    try:
        # Ask for client name
        client_socket.sendall("Welcome to the Grocery Shop! Please enter your name: ".encode())
        client_name = client_socket.recv(1024).decode().strip()
        client_info[client_id] = {'name': client_name, 'purchases': {}}
        client_socket.sendall(f"Hello {client_name}, nice to meet you!\n".encode())
        
        while True:
            # Send options to the client
            options = "\nSelect a category:\na) Fruits\nb) Vegetables\nc) Dairy\n"
            client_socket.sendall(options.encode())

            # Receive the client's choice
            category_choice = client_socket.recv(1024).decode().strip().lower()

            # Determine which category was chosen
            if category_choice == 'a':
                category = 'Fruits'
            elif category_choice == 'b':
                category = 'Vegetables'
            elif category_choice == 'c':
                category = 'Dairy'
            else:
                client_socket.sendall("Invalid option, please try again.\n".encode())
                continue

            # Show products in the chosen category
            products_list = f"Available {category}:\n"
            for item, price in products[category].items():
                products_list += f"{item} - ${price:.2f} each\n"
            client_socket.sendall(products_list.encode())

            # Ask for quantities for each product
            total_cost = 0
            for item in products[category]:
                client_socket.sendall(f"Enter quantity for {item} (or '0' to skip): ".encode())
                quantity = client_socket.recv(1024).decode().strip()

                if quantity.isdigit():
                    quantity = int(quantity)
                    if quantity > 0:
                        total_cost += quantity * products[category][item]
                        # Store purchase information
                        if item in client_info[client_id]['purchases']:
                            client_info[client_id]['purchases'][item] += quantity
                        else:
                            client_info[client_id]['purchases'][item] = quantity
                else:
                    client_socket.sendall("Invalid input, please enter a number.\n".encode())

            # Finalize the purchase and thank the client
            client_socket.sendall(f"Total cost: ${total_cost:.2f}. Cash on delivery.\n".encode())
            client_socket.sendall("Thank you for your purchase! Would you like to continue shopping? (yes/no) ".encode())

            # Check if the client wants to continue
            continue_choice = client_socket.recv(1024).decode().strip().lower()
            if continue_choice == 'no':
                client_socket.sendall("Thank you! Have a great day!\n".encode())
                break
    finally:
        client_socket.close()
        print(f"Client {client_id} ({client_info[client_id]['name']}) has disconnected. Purchase information: {client_info[client_id]['purchases']}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")

    client_id = 0
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_id += 1
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_handler.start()

if __name__ == "__main__":
    main()
