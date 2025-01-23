from smartcard.System import readers
from smartcard.util import toHexString

def connect_to_card():
    """
    Connects to the first available smartcard reader and retrieves the card.
    """
    available_readers = readers()
    if not available_readers:
        print("No smartcard readers found.")
        return None, None

    print("Available readers:")
    for idx, reader in enumerate(available_readers):
        print(f"{idx + 1}: {reader}")

    # Use the first reader
    reader = available_readers[0]
    print(f"\nUsing reader: {reader}")

    connection = reader.createConnection()
    connection.connect()
    print("Smartcard connected.")
    return connection, reader

def authenticate_with_smartcard(connection):
    """
    Sends a command to authenticate using the smartcard.
    This example checks for a basic PIN authentication command.
    """
    # Example APDU for PIN verification (depends on the card's application)
    # CLA, INS, P1, P2, Lc (PIN length), [PIN bytes]
    pin = input("Enter your PIN: ").strip()
    pin_bytes = bytes(pin, 'utf-8')
    apdu = [0x00, 0x20, 0x00, 0x01, len(pin_bytes)] + list(pin_bytes)

    print(f"Sending APDU: {toHexString(apdu)}")
    response, sw1, sw2 = connection.transmit(apdu)

    if sw1 == 0x90 and sw2 == 0x00:  # Success status code
        print("Authentication successful!")
        return True
    else:
        print(f"Authentication failed. Status: {hex(sw1)} {hex(sw2)}")
        return False

def main():
    """
    CLI app main function that authenticates the user via a smartcard.
    """
    print("Smartcard Authentication CLI App")
    connection, reader = connect_to_card()
    if not connection:
        return

    authenticated = authenticate_with_smartcard(connection)
    if authenticated:
        print("\nAccess granted. Welcome!")
        # Proceed with the CLI app's main functionality
    else:
        print("\nAccess denied. Please try again.")

if __name__ == "__main__":
    main()
