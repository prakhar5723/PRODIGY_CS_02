import cv2
import os
from cryptography.fernet import Fernet


def encode_start(x, y, img):
    """
    Encodes the starting position (x, y) into the first few pixels of an image.

    Parameters:
        x (int): The starting row for the encoding.
        y (int): The starting column for the encoding.
        img (numpy.ndarray): The image array in which the position is to be encoded.

    Returns:
        numpy.ndarray: The modified image with the starting position encoded.
    """
    end = "##"
    index = 0
    mid = "$"
    offset = f"{x}{mid}{y}{end}"
    binary_offset = ''.join(format(ord(i), '08b') for i in offset)
    for i in range(0, 4):  # iterate through first 4 rows of the image pixels to encode the offset values
        for j in range(img.shape[1]):  # iterate through the columns of image pixels
            for color in range(3):  # iterate through the color channels
                if index < len(binary_offset):
                    img[i, j, color] = img[i, j, color] & ~1 | int(binary_offset[index])  # Replacing the LSB with
                    # the binary value of the offset
                    index += 1
                else:
                    break
    return img


class Encoding:
    """
    Handles encoding of text into an image using steganography and Fernet encryption.

    Attributes:
        image_path (str): Path of the image file.
        text (str): Text to be encoded.
        key (str): Fernet key for encryption.
        start_row (int): Starting row for encoding.
        start_col (int): Starting column for encoding.
    """

    def __init__(self, image_path, text, key, start_row, start_col):
        """
        Initializes the Encoding class with the required attributes for encoding text into an image.

        Parameters:
            image_path (str): Path of the image file.
            text (str): Text to be encoded.
            key (str): Fernet key for encryption.
            start_row (int): Starting row for encoding.
            start_col (int): Starting column for encoding.
        """
        self.image_path = image_path
        self.text = text
        self.key = key
        self.start_row = start_row
        self.start_col = start_col

    def encryption(self):
        """
        Encrypts the text using Fernet encryption.

        Returns:
            bytes: The encrypted text.
        """
        cipher_key = Fernet(self.key)
        cipher_text = cipher_key.encrypt(self.text.encode())
        return cipher_text

    def encoder(self):
        """
        Encodes the encrypted text into the image starting at the specified row and column.

        Returns:
            tuple: A tuple containing the result message (str) and the path to the new encoded image (str).
        """
        if not self.image_path.lower().endswith('.png'):
            return "Error: This program only supports PNG files.", ''
        img = cv2.imread(self.image_path)
        encrypted_text = self.encryption()
        img_offset = encode_start(self.start_row, self.start_col, img)  # store the offset in the first 5 rows of the
        # image pixels
        capacity = calculate_capacity(self.image_path, self.start_row, self.start_col)
        binary = ''.join(format(byte, '08b') for byte in encrypted_text)
        binary += '1111111111111110'  # End delimiter
        if len(binary) > capacity * 8:
            return "Error: Text size exceeds image capacity. Please enter a shorter text.", ''
        index = 0
        for i in range(self.start_row, img.shape[0]):  # iterate through the rows of image pixels
            for j in range(self.start_col, img.shape[1]):  # iterate through the columns of image pixel
                for color in range(3):  # iterate through the color channels
                    if index < len(binary):
                        img_offset[i, j, color] = img_offset[i, j, color] & ~1 | int(binary[index])
                        index += 1
                    else:
                        break
        new_img_name = f"{os.path.splitext(self.image_path)[0]}_encoded.png"  # save the file with '_encoded at the end'
        cv2.imwrite(new_img_name, img_offset)
        return "Text encoded successfully!", new_img_name


def calculate_capacity(img_path, start_row, start_col):
    """
    Calculates the capacity of the image to hold encoded text based on its dimensions and the start position.

    Parameters:
        img_path (str): Path of the image file.
        start_row (int): Starting row for encoding.
        start_col (int): Starting column for encoding.

    Returns:
        int: The maximum number of bytes that can be encoded into the image.
    """
    image = cv2.imread(img_path)
    end = '1111111111111110'  # End delimiter
    capacity = (((image.shape[0] - start_row - 5) * image.shape[1] * 3) - len(end) * 8 - start_col * 3) // 8
    return capacity
