import argparse
import sys
import platform

# Attempt to import tkinter to check availability
try:
    import tkinter as tk
    tkinter_available = True
except ImportError:
    tkinter_available = False

import CLI
from CLI import SteganographyAppCLI

if tkinter_available:
    # Import GUI module only if tkinter is available
    from GUI import SteganographyAppGUI


def main():
    """
    Main function to parse command line arguments and launch the application in either CLI or GUI mode.
    It allows the user to encode or decode messages using a command-line interface or a graphical user interface.
    """
    parser = argparse.ArgumentParser(description='Steganography Application: Encode, Decode, or GUI mode.')
    parser.add_argument('-e', '--encode', action='store_true', help='Run the application in encode mode (CLI).')
    parser.add_argument('-d', '--decode', action='store_true', help='Run the application in decode mode (CLI).')
    parser.add_argument('-g', '--gui', action='store_true', help='Run the application in GUI mode.')

    args = parser.parse_args()

    if args.encode:
        print("Entering Encode Mode...")
        CLI.encode_cli()
    elif args.decode:
        print("Entering Decode Mode...")
        CLI.decode_cli()
    elif args.gui:
        if tkinter_available:
            print("Starting GUI...")
            start_gui()
        else:
            os_specific_instructions()
    else:
        # No CLI argument provided, prompt user for mode
        mode_prompt()


def os_specific_instructions():
    """
    Provides OS-specific instructions for installing tkinter if it's not available.
    """
    name = platform.system()
    if name == "Linux":
        print("GUI mode is not available because tkinter is not installed. For Linux, try running: 'sudo apt-get "
              "install python3-tk'")
    elif name == "Darwin":
        print("GUI mode is not available because tkinter is not installed. For macOS, tkinter should come with Python "
              "installed from python.org. If missing, reinstall Python.")
    elif name == "Windows":
        print("GUI mode is not available because tkinter is not installed. For Windows, tkinter should come with "
              "Python installed from python.org. If missing, reinstall Python.")
    else:
        print("Unknown operating system. tkinter installation instructions may vary.")
    sys.exit("Please run the application in CLI mode after installing tkinter if needed.")


def mode_prompt():
    print('''
 ____  _                                                     _              _                
/ ___|| |_ ___  __ _  __ _ _ __   ___   __ _ _ __ __ _ _ __ | |__  _   _   / \   _ __  _ __  
\___ \| __/ _ \/ _` |/ _` | '_ \ / _ \ / _` | '__/ _` | '_ \| '_ \| | | | / _ \ | '_ \| '_ \ 
 ___) | ||  __/ (_| | (_| | | | | (_) | (_| | | | (_| | |_) | | | | |_| |/ ___ \| |_) | |_) |
|____/ \__\___|\__, |\__,_|_| |_|\___/ \__, |_|  \__,_| .__/|_| |_|\__, /_/   \_\ .__/| .__/ 
               |___/                   |___/          |_|          |___/        |_|   |_|    
''')
    user_choice = input("Enter 1 for CLI and 2 for GUI: ")
    if user_choice == '1':
        app = SteganographyAppCLI()
        app.run()
    elif user_choice == '2':
        if tkinter_available:
            start_gui()
        else:
            os_specific_instructions()
    else:
        print("Invalid choice. Exiting.")
        sys.exit()


def start_gui():
    """
    Initializes and runs the GUI for the steganography application.
    """
    if tkinter_available:
        root = tk.Tk()
        root.attributes('-topmost', True, '-fullscreen', True)
        root.focus_force()
        app = SteganographyAppGUI(root)
        app.home_page()
        root.mainloop()
    else:
        print("tkinter is not available. Cannot start GUI.")
        sys.exit()


if __name__ == "__main__":
    main()
