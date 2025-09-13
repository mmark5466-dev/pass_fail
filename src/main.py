#!/usr/bin/env python3
"""
PASS // FAIL - Hash Verification GUI Application

A simple graphical interface for testing password strength by checking if hashes 
can be found in common password dictionaries.

What this program does:
- Takes a hash (encrypted password) as input
- Checks if it matches common passwords from wordlists
- Shows results with a fun animated progress indicator

Perfect for:
- Learning about password security
- Testing if your passwords are too common
- Understanding how hash verification works
"""

# Import the modules we need
import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD
from gui import HashVerifierGUI

# Special code to make the app look better on Windows high-DPI screens
if sys.platform.startswith('win'):
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass  # If this fails, just continue without high-DPI support


def setup_main_window():
    """
    Creates and configures the main application window.
    
    Returns:
        tk.Tk: The configured main window
    """
    # Create the main window
    root = TkinterDnD.Tk()
    root.title("PASS // FAIL")
    
    # Set window size and position it in the center of the screen
    # Start at 1200px width with minimum locked at 1200px, but allow expansion beyond that
    window_width = 1200   # Start at preferred width
    window_height = 730
    root.minsize(1200, window_height)  # Minimum size - lock both width and height at preferred sizes
    root.maxsize(9999, window_height)  # Maximum size - lock height but allow width expansion
    
    # Calculate position to center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Force window to appear in front and get focus
    root.lift()                    # Bring window to front
    root.attributes('-topmost', True)  # Make window stay on top temporarily
    root.after(100, lambda: root.attributes('-topmost', False))  # Remove topmost after 100ms
    root.focus_force()             # Force focus to this window
    
    # Try to set an icon for the window (optional)
    try:
        icon_path = "src/images/image01.png"
        if os.path.exists(icon_path):
            root.iconphoto(True, tk.PhotoImage(file=icon_path))
    except Exception:
        pass  # If icon loading fails, just continue without it
    
    return root


def main():
    """
    The main function that starts the application.
    This is what runs when you start the program.
    """
    try:
        # Create the main window
        root = setup_main_window()
        
        # Create the GUI application
        app = HashVerifierGUI(root)
        
        # Handle what happens when user clicks the X button to close
        def handle_window_close():
            """Called when user tries to close the window"""
            # Check if a verification is currently running
            if (hasattr(app, '_worker_thread') and 
                app._worker_thread and 
                app._worker_thread.is_alive()):
                
                # Ask user if they really want to quit during verification
                if messagebox.askokcancel("Quit", 
                    "A verification operation is in progress.\nDo you want to quit?"):
                    
                    # Stop the verification process
                    if app._stop_event:
                        app._stop_event.set()
                    
                    # Give it a moment to clean up, then close
                    root.after(100, root.destroy)
            else:
                # No verification running, safe to close immediately
                root.destroy()
        
        # Tell tkinter to call our function when window is closed
        root.protocol("WM_DELETE_WINDOW", handle_window_close)
        
        # Start the GUI event loop (this keeps the program running)
        root.mainloop()
        
    except Exception as error:
        # If something goes wrong, show an error message
        messagebox.showerror("Error", 
            f"An unexpected error occurred:\n{str(error)}\n\n"
            "Please check that all files are in the correct location.")
        sys.exit(1)


# This special line means "only run main() if this file is run directly"
# (not if it's imported by another file)
if __name__ == "__main__":
    main()