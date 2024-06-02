import tkinter as tk
import cv2
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk

class CannyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        
        # Set the window geometry to cover the whole screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        self.images = []
        self.processed_images = []
        
        # Create a canvas for the red rectangle
        self.canvas = tk.Canvas(self.root, width=200, height=screen_height, bg="white")
        self.canvas.place(x=0, y=0)  # Place the canvas at the left side of the window
        
        self.canvas.create_rectangle(0, 0, 200, screen_height, fill="lightblue")  # Red rectangle
        
        # Create buttons
        self.select_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        self.select_button.place(x=10, y=10)  # Adjust the coordinates as needed
        
        self.process_button = tk.Button(self.root, text="Process Images", command=self.process_images, state=tk.DISABLED)
        self.process_button.place(x=10, y=60)  # Adjust the coordinates as needed
        
        # Morphological operations parameters
        self.kernel_size = tk.IntVar(value=5)
        self.kernel_label = tk.Label(self.root, text="Kernel Size:")
        self.kernel_label.place(x=10, y=110)  # Adjust the coordinates as needed
        
        self.kernel_slider = tk.Scale(self.root, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.kernel_size, length=150, command=self.update_images)
        self.kernel_slider.place(x=10, y=140)  # Adjust the coordinates as needed
        
        # Display area for images
        self.image_canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.image_canvas.place(x=220, y=10)  # Adjust the coordinates as needed
        
        # Image labels
        self.image_labels = []
        
    def select_images(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            self.images = [cv2.imread(file) for file in file_paths]
            self.show_images(self.images)
            self.process_button.config(state=tk.NORMAL)
            
    def show_images(self, images):
        self.clear_canvas()
        self.image_labels = []
        for i, img in enumerate(images):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            label = tk.Label(self.image_canvas, image=img)
            label.image = img
            label.grid(row=0, column=i)
            self.image_labels.append(label)
    
    def clear_canvas(self):
        for label in self.image_labels:
            label.grid_forget()
        self.image_labels = []
    
    def process_images(self):
        if self.images:
            self.processed_images = []
            for img in self.images:
                processed_img = self.apply_morphological_operations(img)
                self.processed_images.append(processed_img)
            self.show_images(self.processed_images)
    
    def update_images(self, event=None):
        if self.images:
            self.processed_images = []
            for img in self.images:
                processed_img = self.apply_morphological_operations(img)
                self.processed_images.append(processed_img)
            self.show_images(self.processed_images)
        
    def apply_morphological_operations(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        kernel_size = self.kernel_size.get()
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        processed_image = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        return processed_image


root = tk.Tk()
app = CannyApp(root)
root.mainloop()
