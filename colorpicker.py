import tkinter as tk
from PIL import ImageGrab
from pynput import mouse
import ctypes
import pyperclip  # For clipboard functionality

class ColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instant Color Picker")
        self.is_picking = False
        self.current_color = None  # Initialize current_color as None

        # Set the initial size of the window
        self.root.geometry("500x400")

        # Create a frame to hold the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Start and Stop buttons next to each other
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_picking)
        self.start_button.grid(row=0, column=0, padx=5)  # Add padding between buttons

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_picking)
        self.stop_button.grid(row=0, column=1, padx=5)  # Add padding between buttons

        self.status_label = tk.Label(root, text="Color picking stopped", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.color_display_label = tk.Label(root, text="Color:", font=("Arial", 14))
        self.color_display_label.pack(pady=10)

        self.color_label = tk.Label(root, text="", font=("Arial", 14), width=20, height=2, bg="white")
        self.color_label.pack(pady=5)

        self.rgb_label = tk.Label(root, text="RGB: N/A", font=("Arial", 14))
        self.rgb_label.pack(pady=5)

        self.hex_label = tk.Label(root, text="Hex: N/A", font=("Arial", 14))
        self.hex_label.pack(pady=5)

        # Buttons for copying RGB and Hex codes
        self.copy_rgb_button = tk.Button(root, text="Copy RGB", command=self.copy_rgb)
        self.copy_rgb_button.pack(pady=5)

        self.copy_hex_button = tk.Button(root, text="Copy Hex", command=self.copy_hex)
        self.copy_hex_button.pack(pady=5)

        # Mouse listener to capture clicks globally
        self.listener = mouse.Listener(on_click=self.get_color)
        self.listener.start()

    def start_picking(self):
        self.is_picking = True
        self.status_label.config(text="Click anywhere to pick a color")
        self.set_cursor("cross")  # Change the cursor globally to crosshair

    def stop_picking(self):
        self.is_picking = False
        self.status_label.config(text="Color picking stopped")
        self.set_cursor("arrow")  # Revert the cursor globally to the default arrow
        
        # Reset color and codes
        self.current_color = None
        self.color_label.config(bg="white")  # Reset color preview
        self.rgb_label.config(text="RGB: N/A")  # Reset RGB label
        self.hex_label.config(text="Hex: N/A")  # Reset Hex label

    def set_cursor(self, cursor_name):
        # Set cursor globally using ctypes for Windows
        user32 = ctypes.windll.user32
        if cursor_name == "cross":
            user32.SystemParametersInfoW(0x0057, 0, user32.LoadCursorW(0, 32515), 0)
        elif cursor_name == "arrow":
            user32.SystemParametersInfoW(0x0057, 0, user32.LoadCursorW(0, 32512), 0)

    def get_color(self, x, y, button, pressed):
        if not self.is_picking:
            return
        
        # Check if the click is within the bounds of the buttons to avoid picking color
        widget = self.root.winfo_containing(x, y)
        if widget in [self.start_button, self.stop_button, self.copy_rgb_button, self.copy_hex_button]:
            return
        
        if pressed:
            screen = ImageGrab.grab()  # Capture the screen
            color = screen.getpixel((x, y))  # Get the color of the pixel at the mouse position
            self.current_color = color  # Store the color for copying purposes
            hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'.upper()  # Convert RGB to Hex
            rgb_color = f"rgb({color[0]}, {color[1]}, {color[2]})"  # Convert RGB to CSS format

            self.color_label.config(bg=hex_color)  # Only the color is displayed as background
            self.rgb_label.config(text=f"RGB: {rgb_color}")  # Display the RGB code in CSS format
            self.hex_label.config(text=f"Hex: {hex_color}")  # Display the Hex code below

    def copy_rgb(self):
        if self.current_color:
            rgb_color = f"rgb({self.current_color[0]}, {self.current_color[1]}, {self.current_color[2]})"
            pyperclip.copy(rgb_color)
            print(f"Copied to clipboard: {rgb_color}")

    def copy_hex(self):
        if self.current_color:
            hex_color = f'#{self.current_color[0]:02x}{self.current_color[1]:02x}{self.current_color[2]:02x}'.upper()
            pyperclip.copy(hex_color)
            print(f"Copied to clipboard: {hex_color}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPickerApp(root)
    root.mainloop()
