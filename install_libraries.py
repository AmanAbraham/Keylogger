# Run this file to import all the necessary libraries using pip

import sys

def install_required_libraries():
    try:
        import pynput
        import cryptography
        import keyboard
        import schedule
    except ImportError:
        print("Required libraries not found. Installing...")
        try:
            import pip
            pip.main(['install', 'cryptography', 'keyboard', 'schedule', 'pynput'])
        except ImportError:
            print("pip not found. Please install the required libraries manually.")
        else:
            print("Libraries installed successfully.")

if __name__ == "__main__":
    install_required_libraries()