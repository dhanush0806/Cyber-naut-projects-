
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("900x700")

        self.image_list = []
        self.current_index = 0
        self.tk_img = None  # To hold the image reference

        # Image display label
        self.image_label = tk.Label(root, bg="gray", relief=tk.SUNKEN)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Button Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.prev_btn = tk.Button(btn_frame, text="Previous", command=self.show_previous)
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.next_btn = tk.Button(btn_frame, text="Next", command=self.show_next)
        self.next_btn.grid(row=0, column=1, padx=10)

        self.load_btn = tk.Button(btn_frame, text="Load Images", command=self.load_images)
        self.load_btn.grid(row=0, column=2, padx=10)

        # Fix: Proper exit button using `root.quit()`
        self.exit_btn = tk.Button(btn_frame, text="Exit", command=self.exit_app)
        self.exit_btn.grid(row=0, column=3, padx=10)
    def load_images(self):
        folder_path = filedialog.askdirectory(title="Select Folder Containing Images")
        if not folder_path:
            return

        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        self.image_list = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(supported_formats)
        ]

        if not self.image_list:
            messagebox.showerror("Error", "No supported image files found in the selected folder.")
            return

        self.current_index = 0
        self.display_image(self.image_list[self.current_index])

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)

            # Resize to fit the display window
            w, h = self.root.winfo_width(), self.root.winfo_height() - 100
            img.thumbnail((w, h))
            
            self.tk_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_img)
            self.root.title(f"Image Viewer - {os.path.basename(image_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image:\n{str(e)}")

    def show_next(self):
        if not self.image_list:
            return
        self.current_index = (self.current_index + 1) % len(self.image_list)
        self.display_image(self.image_list[self.current_index])

    def show_previous(self):
        if not self.image_list:
            return
        self.current_index = (self.current_index - 1) % len(self.image_list)
        self.display_image(self.image_list[self.current_index])

    def exit_app(self):
        self.root.quit()  # Quit the Tkinter event loop and close the window

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
 
