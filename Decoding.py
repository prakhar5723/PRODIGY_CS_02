import cv2
import cryptography
from cryptography.fernet import Fernet


def decode_start(img):
    """
    Decodes the starting position from the first few pixels of an image.

    Parameters:
        img (numpy.ndarray): The image array from which the position is to be decoded.

    Returns:
        tuple: A tuple containing the starting row (int) and column (int) decoded from the image.
    """
    binary = ''
    found = False
    for i in range(0, 4):  # iterate through the first 5 rows of image pixel to retrieve the starting offset
        if found:
            break
        for j in range(img.shape[1]):  # iterate through the columns of image pixels
            if found:
                break
            for color in range(3):  # iterate through the color channels
                binary += str(img[i, j, color] & 1)
                if binary.endswith("0010001100100011"):  # Checks for the end delimiter in binary
                    found = True
                    break
    binary_chunks = [binary[i: i + 8] for i in range(0, len(binary), 8)]
    result_string = ''.join(chr(int(chunk, 2)) for chunk in binary_chunks)
    split_result = result_string.split("$")
    return int(split_result[0]), int(split_result[1][:-2])


class Decoding:
    """
    Handles decoding of text from an image using steganography and Fernet decryption.

    Attributes:
        image_path (str): Path of the image file.
        key (str): Fernet key for decryption.
    """

    def __init__(self, image_path, key):
        """
        Initializes the Decoding object with the specified image path and encryption key.

        Parameters:
            image_path (str): The file path of the image that contains the encoded text.
            key (str): The Fernet key used for decrypting the encoded text extracted from the image.
        """
        self.image_path = image_path
        self.key = key

    def decryption(self, cipher_text):
        """
        Decrypts the text using Fernet decryption.
        Parameters:
            cipher_text (bytes): The encrypted text to decrypt.

        Returns:
            tuple: A tuple containing the decrypted text (str) or None and an error message (str) if applicable.
        """
        try:
            cipher_key = Fernet(self.key)
            text = cipher_key.decrypt(cipher_text).decode()
            return text, None
        except cryptography.fernet.InvalidToken:
            return None, "Error! Invalid Key"

    def decoder(self):
        """
        Decodes the text from the image using the provided Fernet key.
        Returns:
            tuple: A tuple containing the result message (str) and the decoded text (str) or None.
        """
        if not self.image_path.lower().endswith('.png'):
            return "Error: This function only supports PNG files.", None
        img = cv2.imread(self.image_path)
        start_row, start_col = decode_start(img)
        binary = ''
        delimiter_found = False
        for i in range(start_row, img.shape[0]):  # iterate through the rows of image pixels
            if delimiter_found:
                break
            for j in range(start_col, img.shape[1]):  # iterate through the columns of image pixels
                for color in range(3):  # iterate through the color channels
                    binary += str(img[i, j, color] & 1)
                    if binary.endswith('1111111111111110'):  # Checks for the end delimiter in binary
                        delimiter_found = True
                        break
        if not binary:
            return "Error: No encoded message found in the image.", None
        delimiter_index = binary.find('1111111111111110')
        binary = binary[:delimiter_index]
        cipher_text = int(binary, 2).to_bytes((len(binary) + 7) // 8, 'big')
        decrypted_text, error = self.decryption(cipher_text)
        if error:
            return f"Decryption failed with error: {error}", None
        if decrypted_text == "":
            return f"Text decoded successfully.\nThere was no text encoded in the Image.\nKey used to decode: {self.key}", decrypted_text
        else:
            return f"Text decoded successfully. \nKey used to decode: {self.key}", decrypted_text
