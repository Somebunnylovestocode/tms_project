#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import QApplication

try:
    # Ensure the package directory is in the Python path
    package_dir = os.path.dirname(os.path.abspath(__file__))
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)
    
    # Import the GUI class
    from src.gui import CapacitanceCalculatorGUI
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure all required packages are installed and the file structure is correct.")
    sys.exit(1)

def main():
    try:
        # Create the QApplication instance
        app = QApplication(sys.argv)
        
        # Create and show the main window
        window = CapacitanceCalculatorGUI()
        window.show()
        
        # Start the event loop
        return app.exec_()
    except Exception as e:
        print(f"Error starting application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())