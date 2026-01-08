import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import struct
import os
from PIL import Image, ImageTk
import zlib


class CookedSuite:
    def __init__(self, root):
        self.root = root
        self.root.title(".cooked Software Suite")
        self.root.geometry("800x700")

        self.style = ttk.Style()
        self.style.configure("TNotebook", background="#121212")

        self.notebook = ttk.Notebook(root)

        self.tab_create = tk.Frame(self.notebook, bg="#2c3e50")
        self.tab_viewer = tk.Frame(self.notebook, bg="#1a1a1a")

        self.notebook.add(self.tab_create, text="  Create Image  ")
        self.notebook.add(self.tab_viewer, text="  View  Image")
        self.notebook.pack(expand=True, fill="both")

        self.png_2_cooked()
        self.image_viewer()

    def png_2_cooked(self):
        tk.Label(
            self.tab_create,
            text="PNG TO .COOKED",
            fg="white",
            bg="#2c3e50",
            font=("Arial", 20, "bold"),
        ).pack(pady=30)

        btn = tk.Button(
            self.tab_create,
            text="CHOOSE PNG",
            command=self.create_image,
            bg="#e67e22",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
        )
        btn.pack(pady=20)

        self.create_status = tk.Label(
            self.tab_create, text="Ready to create...", fg="#bdc3c7", bg="#2c3e50"
        )
        self.create_status.pack()

    def create_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if not path:
            return

        try:
            with Image.open(path) as img:
                has_alpha = img.mode == "RGBA" or "transparency" in img.info
                mode_flag = 1 if has_alpha else 0
                img = img.convert("RGBA" if has_alpha else "RGB")
                width, height = img.size
                pixel_data = img.tobytes()

            compressed_data = zlib.compress(pixel_data, wbits=15)
            header = struct.pack("<4sIIB", b"COOK", width, height, mode_flag)

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            out_name = os.path.splitext(os.path.basename(path))[0] + ".cooked"
            out_path = os.path.join(desktop, out_name)

            with open(out_path, "wb") as f:
                f.write(header)
                f.write(compressed_data)

            raw_size = len(pixel_data) + 13
            new_size = len(compressed_data) + 13
            ratio = (1 - (new_size / raw_size)) * 100

            messagebox.showinfo("Chef", f"Created New Image! \nOriginal: {raw_size/1024:.1f}KB\nNew: {new_size/1024:.1f}KB\nSaved {ratio:.1f}% space!")
        except Exception as e:
            messagebox.showerror("Error", f"Image creation failed: {e}")

    def image_viewer(self):
        tk.Label(
            self.tab_viewer,
            text=".COOKED VIEWER",
            fg="#4CAF50",
            bg="#1a1a1a",
            font=("Arial", 18),
        ).pack(pady=10)

        tk.Button(
            self.tab_viewer,
            text="OPEN .COOKED",
            command=self.show_image,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
        ).pack(pady=10)

        self.canvas = tk.Canvas(
            self.tab_viewer, width=600, height=450, bg="#222", highlightthickness=0
        )
        self.canvas.pack(pady=10)

    def show_image(self):
        path = filedialog.askopenfilename(filetypes=[("Cooked Files", "*.cooked")])
        if not path:
            return

        try:
            with open(path, "rb") as f:
                header = f.read(13)
                magic, w, h, mode = struct.unpack("<4sIIB", header)

                if magic != b"COOK":
                    raise ValueError("Not a .cooked file")

                raw_data = zlib.decompress(f.read())
                mode_str = "RGBA" if mode == 1 else "RGB"

                img = Image.frombytes(mode_str, (w, h), raw_data)

                img.thumbnail((600, 450))
                self.tk_img = ImageTk.PhotoImage(img)
                self.canvas.delete("all")
                self.canvas.create_image(300, 225, image=self.tk_img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#121212")
    app = CookedSuite(root)
    root.mainloop()
