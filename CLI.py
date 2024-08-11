import random
import sys
import cv2
from cryptography.fernet import Fernet
import os
from Encoding import Encoding, calculate_capacity
from Decoding import Decoding


def encode_cli():
    """
    Command-line interface for encoding text into an image.
    Prompts the user for image path, text, and Fernet key, then encodes the text into the image.
    """
    while True:
        path = input("Enter the path of the PNG image: ")
        if os.path.exists(path):
            if not path.lower().endswith('.png'):
                print("Error: Program only supports PNG image.")
                return
            else:
                break
        else:
            print("Error: File not found. Please enter a valid path.")
            return
    img = cv2.imread(path)
    start_row = random.randint(5, img.shape[0] - 1)  # Randomly select start row
    start_col = random.randint(0, img.shape[1] - 1)  # Randomly select start column
    capacity = calculate_capacity(path, start_row, start_col)  # Calculate image capacity
    print(f"The image can hold up to {capacity} characters.")
    text = input("Enter text to encode within the character limit given above: ")
    while True:
        key = input("Enter Fernet Key or Press (Enter) to generate a key: ")
        if not key:
            key = Fernet.generate_key().decode()  # Generate Fernet key if none provided
            print(f"Generated Key: {key}\nReminder: Copy this key for decoding. ")
        try:
            Fernet(key)  # Validate key format
        except ValueError:
            print("Error! Invalid key. Please Enter a valid Fernet key.")
            break
        encoder = Encoding(path, text, key, start_row, start_col)
        result, encoded_image_path = encoder.encoder()
        if "Error" in result:
            print(result)
            return
        else:
            print(result)
            print(f"The key used for Encoding is {key}")
            print(f"The encoded image saved as {encoded_image_path}")
            break


def decode_cli():
    """
    Command-line interface for decoding text from an image.
    Prompts the user for the path of the encoded image and the Fernet key, then decodes the text.
    """

    while True:
        path = input("Enter the path of the PNG image: ")
        if os.path.exists(path):
            if not path.lower().endswith('.png'):
                print("Error: Program only supports PNG image.")
                return
            else:
                break
        else:
            print("Error: File not found. Please enter a valid path.")
            return
    key = input("Enter Fernet Key: ")
    try:
        Fernet(key)  # Validate key format
    except ValueError:
        print("Error: Invalid Fernet Key.")
        return
    decoder = Decoding(path, key)
    result, decoded_text = decoder.decoder()
    print(f"Decode text: {decoded_text}")
    print(result)


class SteganographyAppCLI:
    """
    Command-line interface for the steganography application.
    Provides a menu for encoding or decoding text within an image.
    """

    def __init__(self):
        self.generated_key = None

    def run(self):
        """
        Runs the CLI application.
        Provides options to encode, decode, or exit the application.
        """
        while True:
            print("\nSteganography Menu:")
            print("1. Encode Text")
            print("2. Decode Text")
            print("3. Exit")
            try:
                choice = input("Enter your choice (1, 2, or 3): ")
                if choice == '1':
                    try:
                        encode_cli()
                    except (SystemExit, KeyboardInterrupt):
                        break
                elif choice == '2':
                    try:
                        decode_cli()
                    except (SystemExit, KeyboardInterrupt):
                        break
                elif choice == '3':
                    print("Exiting the program")
                    sys.exit()
                else:
                    print("Invalid choice!! Please enter 1, 2, or 3.")
            except (SystemExit, KeyboardInterrupt):
                break
