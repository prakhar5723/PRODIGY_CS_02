import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import sys
from Encoding import Encoding, calculate_capacity
from Decoding import Decoding
import random
from cryptography.fernet import Fernet


FONT_BUTTONS = ('Helvetica', 16, 'bold')
FONT_LABEL = ('Helvetica', 14, 'bold')
FONT_HEADING = ('Helvetica', 24, 'bold')
FONT_ENTRY = ('Helvetica', 14)


def exit_program():
    """
    Exits the program.
    """
    sys.exit()


class SteganographyAppGUI:
    """
    Graphical User Interface for the steganography application.
    Allows encoding and decoding of text within images through a user-friendly interface.
    """

    def __init__(self, master):
        """
        Initializes the GUI application.

        Parameters:
            master (tk.Tk): The root window of the application.
        """
        self.master = master
        self.master.title("Steganography App")
        self.current_page = None
        self.generated_key = None
        self.encoded_image_label = None
        self.original_image_label = None
        self.original_image_text = None
        self.encoded_image_text = None
        self.capacity_label = None
        self.start_row = None
        self.start_col = None
        self.decoded_text_label = None
        self.capacity = None

    def home_page(self):
        """
        Displays the home page of the GUI application.
        Provides options to navigate to encoding, decoding, or exit the application.
        """
        if self.current_page:
            self.current_page.destroy()
        self.current_page = tk.Frame(self.master)
        self.current_page.pack(fill='both', expand=True)
        self.background_image = tk.PhotoImage(file='Images/background.png')
        background_label = tk.Label(self.current_page, text="Steganography App", image=self.background_image)
        background_label.place(relwidth=1, relheight=1)
        heading_label = tk.Label(self.current_page, text="Steganography App", font=FONT_HEADING, bg='black', fg='white')
        heading_label.pack(pady=50)
        button_config = {'font': FONT_BUTTONS, 'width': 30, 'height': 2, 'bd': 5, 'bg': '#e0ffeb'}
        button_frame = tk.Frame(self.current_page, bg='black')
        button_frame.pack()
        encode_button = tk.Button(button_frame, text="Encode", command=self.encode_page, **button_config)
        encode_button.grid(row=0, column=0, padx=10, pady=20)
        decode_button = tk.Button(button_frame, text="Decode", command=self.decode_page, **button_config)
        decode_button.grid(row=0, column=1, padx=10, pady=20)
        exit_button = tk.Button(button_frame, text="Exit", command=exit_program, **button_config)
        exit_button.grid(row=0, column=2, padx=10, pady=20)
        button_frame.place(relx=0.5, rely=0.5, anchor='center')

    def show_image(self, image_path, label_text='', side=tk.LEFT):
        """
        Displays an image on the current page of the GUI.

        Parameters:
            image_path (str): The path to the image file to display.
            label_text (str): Text to label the image with.
            side (tk.SIDE): The side of the page to pack the image widget on.
        """
        img = cv2.imread(image_path)
        img_resized = cv2.resize(img, (300, 300))
        img = tk.PhotoImage(data=cv2.imencode('.png', img_resized)[1].tobytes())
        if label_text == 'Original Image:':
            if self.original_image_label:
                self.original_image_label.destroy()
            if self.original_image_text:
                self.original_image_text.destroy()
            self.original_image_text = tk.Label(self.current_page, text=label_text)
            self.original_image_text.pack(pady=5, side=side, padx=10)
            self.original_image_label = tk.Label(self.current_page, image=img)
            self.original_image_label.image = img
            self.original_image_label.pack(pady=5, side=side, padx=10)
        if label_text == 'Encoded Image:':
            if self.encoded_image_label:
                self.encoded_image_label.destroy()
            if self.encoded_image_text:
                self.encoded_image_text.destroy()
            self.encoded_image_text = tk.Label(self.current_page, text=label_text)
            self.encoded_image_text.pack(pady=5, side=side, padx=10)
            self.encoded_image_label = tk.Label(self.current_page, image=img)
            self.encoded_image_label.image = img
            self.encoded_image_label.pack(pady=5, side=side, padx=10)

    def encode_page(self):
        """
        Displays the encoding page where users can choose an image and enter text to encode.
        """
        if self.current_page:
            self.current_page.destroy()
        self.current_page = tk.Frame(self.master)
        self.current_page.pack()
        heading_label = tk.Label(self.current_page, text="Encode Page", font=FONT_HEADING)
        heading_label.pack()
        label_config = {'font': FONT_LABEL, 'anchor': 'w'}
        entry_config = {'font': FONT_ENTRY, 'width': 40}
        button_config = {'font': FONT_BUTTONS, 'width': 10, 'height': 1, 'bd': 5}
        top_frame = tk.Frame(self.current_page)
        top_frame.pack(fill='x', padx=10, pady=10)
        path_label = tk.Label(top_frame, text="Image Path or Open File:", **label_config)
        path_label.grid(row=0, column=0, sticky='w')
        self.image_entry = tk.Entry(top_frame, **entry_config, state='disabled')
        self.image_entry.grid(row=0, column=1, sticky='we')
        open_button = tk.Button(top_frame, text="Open File", command=self.open_file_encode, **button_config)
        open_button.grid(row=0, column=2, padx=10)
        text_label = tk.Label(top_frame, text="Enter text to Encode:", **label_config)
        text_label.grid(row=1, column=0, sticky='w')
        self.text_entry = tk.Entry(top_frame, **entry_config)
        self.text_entry.grid(row=1, column=1, sticky='we')
        key_label = tk.Label(top_frame, text="Enter or Generate Fernet Key:", **label_config)
        key_label.grid(row=2, column=0, sticky='w')
        self.key_entry = tk.Entry(top_frame, **entry_config)
        self.key_entry.grid(row=2, column=1, sticky='we')
        generate_key_button = tk.Button(top_frame, text="Generate Key", command=self.generate_key, **button_config)
        generate_key_button.grid(row=2, column=2, padx=5)
        encode_button = tk.Button(top_frame, text="Encode", command=self.encode_text, **button_config)
        encode_button.grid(row=3, column=1, padx=10, pady=5)
        back_button = tk.Button(top_frame, text="Back", command=self.home_page, **button_config)
        back_button.grid(row=4, column=1, padx=10, pady=5)
        self.encoded_image_label = tk.Label(top_frame, text="", font=FONT_LABEL)
        self.encoded_image_label.grid(row=5, column=1, sticky='w', pady=5)
        self.key_used_label = tk.Label(top_frame, text="", font=FONT_LABEL)
        self.key_used_label.grid(row=6, column=1, sticky='w', pady=5)
        # Set the window to zoomed state

    def open_file_encode(self):
        """
        Opens a dialog for the user to select an image file for encoding.
        """
        self.image_entry.config(state='normal')
        self.image_entry.delete(0, tk.END)
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            if not file_path.lower().endswith('.png'):
                messagebox.showerror("Error", "Please select a valid PNG image.")
                return
            self.image_entry.insert(0, file_path)
            self.image_entry.config(state='disabled')
            img = cv2.imread(file_path)
            self.start_row = random.randint(5, img.shape[0] - 1)
            self.start_col = random.randint(0, img.shape[1] - 1)
            self.capacity = calculate_capacity(file_path, self.start_row, self.start_col)
            if self.capacity_label:
                self.capacity_label.destroy()
            self.capacity_label = tk.Label(self.current_page, text=f"Maximum Capacity: {self.capacity} characters",
                                           font=FONT_LABEL)
            self.capacity_label.pack(pady=5)
            self.show_image(file_path, "Original Image:")

    def encode_text(self):
        """
        Encodes the provided text into the selected image using the provided Fernet key.
        """
        image_path = self.image_entry.get()
        if not image_path.lower().endswith('.png'):
            messagebox.showerror("Error", "Please select a valid PNG image.")
            return
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Could not read the image. Please check the image path.")
            return
        if self.start_row is None or self.start_col is None:
            self.start_row = random.randint(5, img.shape[0] - 1)
            self.start_col = random.randint(0, img.shape[1] - 1)
        if self.capacity is None:
            self.capacity = calculate_capacity(image_path, self.start_row, self.start_col)
            if self.capacity_label:
                self.capacity_label.destroy()
            self.capacity_label = tk.Label(self.current_page, text=f"Maximum Capacity: {self.capacity} characters",
                                           font=FONT_LABEL)
            self.capacity_label.pack(pady=5)
        text = self.text_entry.get()
        key = self.key_entry.get()
        try:
            Fernet(key)  # Validate key format
        except Exception as e:
            messagebox.showerror("Error", "Invalid Fernet Key. Please enter a valid key.")
            return
        encoder = Encoding(image_path, text, key, self.start_row, self.start_col)
        result, encoded_image_path = encoder.encoder()
        if "Error:" in result:
            messagebox.showerror("Error", result)
            return
        if self.encoded_image_label:
            self.encoded_image_label.config(text=f"Encoded Image Path: {encoded_image_path}")
        else:
            self.encoded_image_label = tk.Label(self.current_page, text=f"Encoded Image Path: {encoded_image_path}",
                                                font=FONT_LABEL)
            self.encoded_image_label.pack(pady=5)
        self.show_result_message("Encoding successful", result, key)
        self.show_image(encoded_image_path, "Encoded Image:")

    def generate_key(self):
        """
        Generates a new Fernet key, displays it in the key entry field, and copies it to the clipboard.
        """
        self.generated_key = Fernet.generate_key().decode()
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, self.generated_key)

    def show_result_message(self, title, result, key_info):
        """
        Displays a result message box after encoding or decoding operation.

        Parameters:
            title (str): The title for the message box.
            result (str): The message to display.
            key_info (str): Additional information about the Fernet key used.
        """
        messagebox.showinfo(title, f"{result}")
        if self.key_used_label:
            self.key_used_label.config(text=f"Key used: {key_info}", font=FONT_LABEL)

    def open_file_decode(self):
        """
        Opens a dialog for the user to select an encoded image file for decoding.
        """
        self.image_entry.config(state='normal')
        self.image_entry.delete(0, tk.END)
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image_entry.insert(0, file_path)
            self.image_entry.config(state='disabled')
            self.show_image(file_path, "Encoded Image:")

    def decode_text(self):
        """
        Decodes text from the selected encoded image using the provided Fernet key.
        """
        image_path = self.image_entry.get()
        if not image_path.lower().endswith('.png'):
            messagebox.showerror("Error", "Please select a valid PNG image.")
            return
        key = self.key_entry.get()
        try:
            Fernet(key)  # Validate key format
        except Exception as e:
            messagebox.showerror("Error", "Invalid Fernet Key. Please enter a valid key.")
            return
        decoder = Decoding(image_path, key)
        result, decoded_text = decoder.decoder()
        if self.decoded_text_label:
            self.decoded_text_label.config(text=f"Decoded Text: {decoded_text}")
        else:
            self.decoded_text_label = tk.Label(self.current_page, text=f"Decoded Text: {decoded_text}", font=FONT_LABEL)
            self.decoded_text_label.pack(pady=5)
        self.show_result_message("Decoding result", result, key)

    def decode_page(self):
        """
        Displays the decoding page where users can choose an encoded image and enter a Fernet key to decode text.
        """
        if self.current_page:
            self.current_page.destroy()
        self.current_page = tk.Frame(self.master)
        self.current_page.pack()
        heading_label = tk.Label(self.current_page, text="Decode Page", font=FONT_HEADING)
        heading_label.pack()
        label_config = {'font': FONT_LABEL, 'anchor': 'w'}
        entry_config = {'font': FONT_ENTRY, 'width': 40}
        button_config = {'font': FONT_BUTTONS, 'width': 20, 'height': 2, 'bd': 5}
        top_frame = tk.Frame(self.current_page)
        top_frame.pack(fill='x', padx=10, pady=10)
        image_path_label = tk.Label(top_frame, text="Encoded Image Path:", **label_config)
        image_path_label.grid(row=0, column=0, sticky='w')
        self.image_entry = tk.Entry(top_frame, **entry_config, state='disabled')
        self.image_entry.grid(row=0, column=1, sticky='we')
        open_file_button = tk.Button(top_frame, text="Open File", command=self.open_file_decode, **button_config)
        open_file_button.grid(row=0, column=2, padx=10)
        key_label = tk.Label(top_frame, text="Enter Fernet Key:", **label_config)
        key_label.grid(row=1, column=0, sticky='w')
        self.key_entry = tk.Entry(top_frame, **entry_config)
        self.key_entry.grid(row=1, column=1, sticky='we')
        decode_button = tk.Button(top_frame, text="Decode", command=self.decode_text, **button_config)
        decode_button.grid(row=2, column=1, padx=10, pady=5)
        back_button = tk.Button(top_frame, text="Back", command=self.home_page, **button_config)
        back_button.grid(row=3, column=1, padx=10, pady=5)
        self.decoded_text_label = tk.Label(top_frame, text="", font=FONT_LABEL)
        self.decoded_text_label.grid(row=4, column=1, sticky='w', pady=5)
        self.key_used_label = tk.Label(top_frame, text="", font=FONT_LABEL)
        self.key_used_label.grid(row=5, column=1, sticky='w', pady=5)
